"""G4 渲染檢查（Playwright）。

以 1280×720 逐頁檢查：
- 內容容器 .slide-content 沒有溢出（scrollHeight <= clientHeight、scrollWidth <= clientWidth）
- 頁數與 drafts 一致；用鍵盤右鍵翻頁確認可翻
- 文字（標題＋重點＋出處列）與 draft 一致（正規化空白、去掉 〔Cxx〕 後比對）
- 重點字體 >= 24px（以 1280×720、縮放 1 為準）
- v2.1：每頁有視覺區，且其 data-spec 與 draft 的「視覺：」逐字一致；視覺區不超出投影片
v2.1 新增（使用者回饋：簡報在窄視窗變成接近正方形，v1 只測 1280×720 沒抓到）：
- 在多種視窗尺寸下，投影片實際顯示的寬高比必須是 16:9（誤差 2%），且整張投影片在視窗內
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
VIEWPORTS = [(1280, 720), (1440, 900), (1920, 1080), (1024, 768), (800, 600), (390, 844)]


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
                const v = s.querySelector('.visual');
                const sr = s.getBoundingClientRect();
                const vr = v ? v.getBoundingClientRect() : null;
                const txt = [s.querySelector('h1').innerText,
                             ...[...s.querySelectorAll('li')].map(li => li.innerText),
                             s.querySelector('.src').innerText].join('');
                return {draft: s.dataset.draft, sh: c.scrollHeight, ch: c.clientHeight,
                        sw: c.scrollWidth, cw: c.clientWidth, text: txt,
                        spec: v ? v.dataset.spec : null,
                        visualInside: vr ? (vr.left >= sr.left - 1 && vr.right <= sr.right + 1 &&
                                            vr.top >= sr.top - 1 && vr.bottom <= sr.bottom + 1) : null,
                        clipped: v ? [...v.querySelectorAll('svg text')].filter(t => {
                            const b = t.getBBox(), vb = t.ownerSVGElement.viewBox.baseVal;
                            return b.x < -0.5 || b.y < -0.5 || b.x + b.width > vb.width + 0.5 || b.y + b.height > vb.height + 0.5;
                          }).map(t => t.textContent) : [],
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
                if d["visual"]:
                    if info["spec"] is None:
                        errors.append(f"{label}：draft 有視覺，HTML 卻沒有視覺區")
                    elif info["spec"] != d["visual"]:
                        errors.append(f"{label}：視覺規格與 draft 不一致")
                    elif not info["visualInside"]:
                        errors.append(f"{label}：視覺區超出投影片")
                    if info["clipped"]:
                        errors.append(f"{label}：圖表文字被裁切 {info['clipped']}")
            page.screenshot(path=str(SCREENS / f"{info['draft']}.png"))

        # v2.1：多種視窗尺寸下的 16:9 與完整顯示
        for w, h in VIEWPORTS:
            p2 = browser.new_page(viewport={"width": w, "height": h})
            p2.goto(HTML.as_uri())
            r = p2.evaluate(
                "(() => { const r = document.querySelector('.slide.active').getBoundingClientRect();"
                " return [r.left, r.top, r.width, r.height]; })()"
            )
            left, top, rw, rh = r
            ratio = rw / rh if rh else 0
            if abs(ratio - 16 / 9) > 16 / 9 * 0.02:
                errors.append(f"視窗 {w}×{h}：投影片顯示比例 {ratio:.2f}，不是 16:9（1.78）")
            if left < -1 or top < -1 or left + rw > w + 1 or top + rh > h + 1:
                errors.append(f"視窗 {w}×{h}：投影片超出視窗")
            p2.close()
        browser.close()

    if errors:
        print(f"G4 渲染檢查失敗：{len(errors)} 個問題")
        for e in errors:
            print("  ✗", e)
        return 1
    sizes = "、".join(f"{w}×{h}" for w, h in VIEWPORTS)
    print(f"G4 渲染檢查通過：{n} 頁，無溢出、文字與視覺規格一致、字體 ≥ {MIN_FONT}px；"
          f"{sizes} 皆為 16:9 且完整顯示；截圖在 {SCREENS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
