"""N5 渲染：把 drafts/slide-XX.md 逐字轉成單一 HTML 檔 slides/index.html。

文字一個字都不改：標題、重點、出處列原樣放入（只做 HTML 跳脫）。
版面：16:9、1280×720 基準、內文 26px、左右鍵翻頁、右下頁碼；不依賴外部 CDN。
用法：python3 scripts/build_slides.py
"""
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from topic_common import ROOT, draft_files, parse_draft  # noqa: E402

OUT = ROOT / "slides" / "index.html"

CSS = """
:root { --bg:#fbfaf7; --ink:#1f2328; --muted:#5b6470; --accent:#2f6f5e; --rule:#e3e0d8; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; background: #2b2b2b; font-family: "PingFang TC", "Noto Sans TC", "Microsoft JhengHei", system-ui, sans-serif; }
.deck { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; }
.slide { display: none; width: 1280px; height: 720px; background: var(--bg); color: var(--ink);
  padding: 56px 80px 40px; flex-direction: column; transform-origin: center center; position: relative; }
.slide.active { display: flex; }
.slide-content { flex: 1; overflow: hidden; display: flex; flex-direction: column; }
.slide h1 { font-size: 44px; line-height: 1.3; font-weight: 700; color: var(--ink);
  padding-bottom: 18px; margin-bottom: 26px; border-bottom: 3px solid var(--accent); }
.slide ul { list-style: none; display: flex; flex-direction: column; gap: 18px; }
.slide li { font-size: 28px; line-height: 1.45; padding-left: 36px; position: relative; }
.slide li::before { content: ""; position: absolute; left: 6px; top: 15px; width: 12px; height: 12px;
  border-radius: 50%; background: var(--accent); }
.slide .src { margin-top: auto; padding-top: 14px; border-top: 1px solid var(--rule);
  font-size: 18px; line-height: 1.4; color: var(--muted); }
.slide.cover h1 { font-size: 56px; border: none; margin-top: 90px; }
.slide.cover li { font-size: 30px; }
.pageno { position: absolute; right: 28px; bottom: 14px; font-size: 16px; color: var(--muted); }
.hint { position: fixed; left: 12px; bottom: 10px; color: #aaa; font-size: 13px; }
"""

JS = """
const slides = [...document.querySelectorAll('.slide')];
let cur = 0;
function fit() {
  const s = Math.min(window.innerWidth / 1280, window.innerHeight / 720);
  slides.forEach(el => el.style.transform = `scale(${s})`);
}
function goTo(i) {
  cur = Math.max(0, Math.min(slides.length - 1, i));
  slides.forEach((el, k) => el.classList.toggle('active', k === cur));
  history.replaceState(null, '', '#' + (cur + 1));
}
document.addEventListener('keydown', e => {
  if (['ArrowRight', 'PageDown', ' '].includes(e.key)) { e.preventDefault(); goTo(cur + 1); }
  if (['ArrowLeft', 'PageUp'].includes(e.key)) { e.preventDefault(); goTo(cur - 1); }
  if (e.key === 'Home') goTo(0);
  if (e.key === 'End') goTo(slides.length - 1);
});
document.addEventListener('click', e => { goTo(e.clientX > window.innerWidth / 2 ? cur + 1 : cur - 1); });
window.addEventListener('resize', fit);
window.goTo = goTo;
fit();
goTo((parseInt(location.hash.slice(1)) || 1) - 1);
"""


def main() -> int:
    files = draft_files()
    if not files:
        print("drafts/ 沒有任何頁")
        return 1
    n = len(files)
    parts = []
    for i, p in enumerate(files, 1):
        d = parse_draft(p)
        cls = "slide cover" if i == 1 else "slide"
        lis = "\n".join(f"      <li>{html.escape(b)}</li>" for b in d["bullets"])
        parts.append(
            f'  <section class="{cls}" data-draft="{p.stem}">\n'
            f'    <div class="slide-content">\n'
            f"      <h1>{html.escape(d['title'])}</h1>\n"
            f"      <ul>\n{lis}\n      </ul>\n"
            f"      <p class=\"src\">出處：{html.escape(d['source'])}</p>\n"
            f"    </div>\n"
            f'    <div class="pageno">{i} / {n}</div>\n'
            f"  </section>"
        )
    doc = (
        "<!doctype html>\n<html lang=\"zh-Hant-TW\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "<title>AI 時代的程式學習</title>\n"
        f"<style>{CSS}</style>\n</head>\n<body>\n<div class=\"deck\">\n"
        + "\n".join(parts)
        + "\n</div>\n<div class=\"hint\">← → 翻頁</div>\n"
        f"<script>{JS}</script>\n</body>\n</html>\n"
    )
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")
    print(f"已產生 {OUT.relative_to(ROOT)}：{n} 頁")
    return 0


if __name__ == "__main__":
    sys.exit(main())
