"""G4 渲染檢查（Playwright，1280×720）。

逐頁檢查：
- 內容容器 .slide-content 沒有溢出（scrollHeight <= clientHeight、scrollWidth <= clientWidth）
- 頁數與 drafts 一致；用鍵盤右鍵翻頁確認可翻
- 可見文字（標題＋重點＋出處列）與 draft 一致（正規化空白後比對）
- 重點字體 >= 24px（以 1280×720、縮放 1 為準）
截圖存到 topic/ai-era-coding/review/screens/slide-XX.png。
通過 exit 0；溢出時列出頁碼（應退回 N4 縮短該頁，不准縮小字體）、exit 1。
首次使用：pip install playwright && python -m playwright install chromium
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from topic_common import ROOT, TOPIC, draft_files, parse_draft  # noqa: E402

HTML = ROOT / "slides" / "index.html"
SCREENS = TOPIC / "review" / "screens"
MIN_FONT = 24


def norm(s: str) -> str:
    return re.sub(r"\s+", "", s)


def main() -> int:
    from playwright.sync_api import sync_playwright

    errors: list[str] = []
    drafts = draft_files()
    SCREENS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.goto(HTML.as_uri())
        n = page.evaluate("document.querySelectorAll('.slide').length")
        if n != len(drafts):
            errors.append(f"HTML 有 {n} 頁，drafts 有 {len(drafts)} 頁")
        for i in range(n):
            if i > 0:
                page.keyboard.press("ArrowRight")
            info = page.evaluate(
                """() => {
                const s = document.querySelector('.slide.active');
                const c = s.querySelector('.slide-content');
                const fonts = [...s.querySelectorAll('li')].map(li => parseFloat(getComputedStyle(li).fontSize));
                return {draft: s.dataset.draft, sh: c.scrollHeight, ch: c.clientHeight,
                        sw: c.scrollWidth, cw: c.clientWidth, text: c.innerText,
                        minFont: fonts.length ? Math.min(...fonts) : null,
                        idx: [...document.querySelectorAll('.slide')].indexOf(s)};
            }"""
            )
            label = f"第 {i + 1} 頁（{info['draft']}）"
            if info["idx"] != i:
                errors.append(f"{label}：按右鍵後停在第 {info['idx'] + 1} 頁，翻頁失敗")
            if info["sh"] > info["ch"] or info["sw"] > info["cw"]:
                errors.append(
                    f"{label}：內容溢出（高 {info['sh']}/{info['ch']}，寬 {info['sw']}/{info['cw']}）→ 退回 N4 縮短"
                )
            if info["minFont"] is not None and info["minFont"] < MIN_FONT:
                errors.append(f"{label}：重點字體 {info['minFont']}px < {MIN_FONT}px")
            if i < len(drafts):
                d = parse_draft(drafts[i])
                expect = norm(d["title"] + "".join(d["bullets"]) + "出處：" + d["source"])
                if norm(info["text"]) != expect:
                    errors.append(f"{label}：可見文字與 {drafts[i].name} 不一致")
            page.screenshot(path=str(SCREENS / f"{info['draft']}.png"))
        browser.close()

    if errors:
        print(f"G4 渲染檢查失敗：{len(errors)} 個問題")
        for e in errors:
            print("  ✗", e)
        return 1
    print(f"G4 渲染檢查通過：{n} 頁，無溢出、文字一致、字體 ≥ {MIN_FONT}px，截圖在 {SCREENS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
