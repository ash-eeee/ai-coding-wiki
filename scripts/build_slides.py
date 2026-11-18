"""N5 渲染：把 drafts/slide-XX.md 逐字轉成單一 HTML 檔 slides/index.html。

文字一個字都不改：標題、重點、出處列原樣放入（只做 HTML 跳脫），〔Cxx〕 標籤會去掉。
v2.1：每頁的「視覺：」規格畫成內嵌 SVG（長條圖、範圍圖、大數字、人數圖、環圖、圖示清單、流程、檢查清單）；
圖上的數字與文字全部來自規格，規格的數字由 check_drafts.py 對卡片檢查。
版面：16:9、1280×720 基準、內文 28px、左右鍵翻頁、右下頁碼；不依賴外部 CDN。
用法：python3 scripts/build_slides.py
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from topic_common import ROOT, draft_files, parse_draft, parse_visual  # noqa: E402

OUT = ROOT / "slides" / "index.html"
W, H = 420, 440  # 視覺區大小
ACCENT, WARN, MUTED, INK, SOFT = "#2f6f5e", "#b5523b", "#8a8f98", "#1f2328", "#e6efe9"
FONT = 'font-family="PingFang TC, Noto Sans TC, Microsoft JhengHei, sans-serif"'

CSS = """
:root { --bg:#fbfaf7; --ink:#1f2328; --muted:#5b6470; --accent:#2f6f5e; --rule:#e3e0d8; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; overflow: hidden; background: #2b2b2b; font-family: "PingFang TC", "Noto Sans TC", "Microsoft JhengHei", system-ui, sans-serif; }
.deck { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; }
/* flex: none：視窗比 1280 窄時投影片不准被壓扁，維持 16:9，只靠 scale 等比縮放 */
.slide { display: none; flex: none; width: 1280px; height: 720px; background: var(--bg); color: var(--ink);
  padding: 48px 72px 36px; flex-direction: column; transform-origin: center center; position: relative; }
.slide.active { display: flex; }
.slide-content { flex: 1; overflow: hidden; display: flex; flex-direction: column; min-height: 0; }
.slide h1 { font-size: 44px; line-height: 1.3; font-weight: 700; color: var(--ink);
  padding-bottom: 14px; margin-bottom: 22px; border-bottom: 3px solid var(--accent); }
.body { flex: 1; display: flex; gap: 36px; align-items: center; min-height: 0; }
.slide ul { flex: 1; list-style: none; display: flex; flex-direction: column; gap: 16px; }
.slide li { font-size: 28px; line-height: 1.42; padding-left: 32px; position: relative; }
.slide li::before { content: ""; position: absolute; left: 4px; top: 14px; width: 12px; height: 12px;
  border-radius: 50%; background: var(--accent); }
.visual { flex: none; width: 420px; height: 440px; }
.visual svg { display: block; width: 100%; height: 100%; }
.slide .src { margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--rule);
  font-size: 18px; line-height: 1.4; color: var(--muted); }
.slide.cover h1 { font-size: 56px; border: none; margin-top: 30px; }
.pageno { position: absolute; right: 28px; bottom: 12px; font-size: 16px; color: var(--muted); }
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


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def text(x, y, s, size=22, fill=INK, anchor="start", weight=400) -> str:
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" {FONT}>{esc(s)}</text>')


def num(v: str) -> float:
    return float(re.sub(r"[^\d.\-+]", "", v.replace("−", "-")) or 0)


def svg_title(t: str) -> str:
    return text(0, 26, t, 22, MUTED, weight=600) if t else ""


# 圖示：在 36×36 的方框內、以 (0,0) 為中心畫白色線條
GLYPHS = {
    "bug": '<ellipse cx="0" cy="3" rx="8" ry="11"/><circle cx="0" cy="-11" r="4"/>'
           '<path d="M-8 -2 h-7 M8 -2 h7 M-8 6 h-7 M8 6 h7 M-7 12 l-6 5 M7 12 l6 5"/>',
    "eye": '<path d="M-15 0 Q0 -13 15 0 Q0 13 -15 0 Z"/><circle cx="0" cy="0" r="4.5"/>',
    "bulb": '<path d="M-6 8 Q-12 2 -12 -5 A12 12 0 0 1 12 -5 Q12 2 6 8 Z"/><path d="M-5 12 h10 M-3 16 h6"/>',
    "book": '<path d="M0 -10 Q-8 -14 -15 -11 V11 Q-8 8 0 12 Q8 8 15 11 V-11 Q8 -14 0 -10 Z M0 -10 V12"/>',
    "steps": '<path d="M-15 14 h8 v-8 h8 v-8 h8 v-8 h7"/>',
    "flow": '<circle cx="-11" cy="0" r="4"/><circle cx="0" cy="0" r="4"/><circle cx="11" cy="0" r="4"/>'
            '<path d="M-7 0 h3 M4 0 h3"/>',
    "sort": '<path d="M-13 -9 h16 M-13 0 h22 M-13 9 h10"/><path d="M13 -9 v16 m-4 -4 l4 4 l4 -4"/>',
    "think": '<path d="M-6 -6 A6 6 0 1 1 2 0 Q0 2 0 6"/><circle cx="0" cy="12" r="1.5"/>',
    "verify": '<path d="M0 -14 L12 -9 V0 Q12 10 0 15 Q-12 10 -12 0 V-9 Z"/><path d="M-6 0 l4 5 l8 -9"/>',
    "nobug": '<ellipse cx="0" cy="2" rx="7" ry="10"/><path d="M-7 -2 h-6 M7 -2 h6 M-6 7 h-6 M6 7 h6"/>'
             '<path d="M-14 -14 L14 14"/>',
    "alert": '<path d="M0 -14 L15 12 H-15 Z"/><path d="M0 -4 v8"/><circle cx="0" cy="8" r="1.5"/>',
    "up": '<path d="M-14 12 L-5 2 L2 7 L14 -8"/><path d="M6 -8 h8 v8"/>',
    "neq": '<path d="M-11 -4 h22 M-11 5 h22 M6 -13 L-6 14"/>',
    "search": '<circle cx="-3" cy="-3" r="9"/><path d="M4 4 l9 9"/>',
}


def glyph(name: str, cx: float, cy: float) -> str:
    g = GLYPHS.get(name)
    if not g:
        return ""
    return (f'<g transform="translate({cx:.0f} {cy:.0f})" fill="none" stroke="#fff" stroke-width="2.6" '
            f'stroke-linecap="round" stroke-linejoin="round">{g}</g>')


def v_bar(title, items) -> str:
    """有正負的水平長條圖：0 在中間。"""
    out = [svg_title(title)]
    mx = max(abs(num(v)) for _, v in items) or 1
    cx, half = W / 2, W / 2 - 50
    top = 60
    step = (H - top - 10) / len(items)
    out.append(f'<line x1="{cx}" y1="{top - 6}" x2="{cx}" y2="{H - 10}" stroke="{MUTED}" stroke-width="2"/>')
    for i, (k, v) in enumerate(items):
        y = top + i * step
        n = num(v)
        w = abs(n) / mx * half
        hi = k.startswith("*")  # 標籤前加 * 表示要強調的那一條
        k = k.lstrip("*")
        color = WARN if hi else MUTED
        x = cx if n >= 0 else cx - w
        out.append(text(0, y + 26, k, 22, INK, weight=600))
        out.append(f'<rect x="{x:.1f}" y="{y + 40}" width="{w:.1f}" height="40" rx="6" fill="{color}"/>')
        out.append(text(W, y + 26, v + "%", 26, color, "end", 700))  # 數值放在標籤列右端，不會被裁切
    return "".join(out)


def v_range(title, items) -> str:
    """0–100 的範圍條。"""
    out = [svg_title(title)]
    x0, x1 = 10, W - 10
    sx = lambda p: x0 + (x1 - x0) * p / 100  # noqa: E731
    top = 70
    step = (H - top - 60) / len(items)
    for i, (k, v) in enumerate(items):
        lo, hi = [float(t) for t in re.findall(r"\d+(?:\.\d+)?", v)[:2]]
        y = top + i * step
        color = ACCENT if i == 0 else WARN
        out.append(text(0, y + 24, k, 22, INK, weight=600))
        out.append(f'<rect x="{x0}" y="{y + 40}" width="{x1 - x0}" height="34" rx="6" fill="#efede7"/>')
        out.append(f'<rect x="{sx(lo):.1f}" y="{y + 40}" width="{sx(hi) - sx(lo):.1f}" height="34" rx="6" fill="{color}"/>')
        out.append(text((sx(lo) + sx(hi)) / 2, y + 108, f"{v.replace('-', '–')}%", 28, color, "middle", 700))
    for p, anchor in ((0, "start"), (50, "middle"), (100, "end")):
        out.append(text(sx(p), H - 12, f"{p}%" if p else "0", 18, MUTED, anchor))
    return "".join(out)


def v_bignum(title, items) -> str:
    out = [svg_title(title)]
    top = 40 if title else 10
    step = (H - top) / len(items)
    for i, (v, cap) in enumerate(items):
        y = top + i * step
        color = WARN if i % 2 == 0 else ACCENT
        out.append(f'<rect x="0" y="{y + 8}" width="{W}" height="{step - 20:.0f}" rx="14" fill="{SOFT}"/>')
        out.append(text(W / 2, y + step * 0.5 + 8, v, 76, color, "middle", 800))
        out.append(text(W / 2, y + step * 0.5 + 48, cap, 22, INK, "middle"))
    return "".join(out)


def v_grid(title, items) -> str:
    """人數圖：例如 9/10。"""
    (frac, cap), = items[:1]
    a, b = [int(t) for t in frac.split("/")]
    out = [svg_title(title)]
    cols = 5
    for i in range(b):
        r, c = divmod(i, cols)
        x, y = 42 + c * 76, 70 + r * 130
        color = WARN if i < a else "#d5d2ca"
        out.append(f'<circle cx="{x}" cy="{y + 18}" r="17" fill="{color}"/>')
        out.append(f'<rect x="{x - 24}" y="{y + 42}" width="48" height="58" rx="20" fill="{color}"/>')
    out.append(text(W / 2, 360, frac.replace("/", " / "), 44, WARN, "middle", 800))
    out.append(text(W / 2, 400, cap, 22, INK, "middle"))
    return "".join(out)


def v_donut(title, items) -> str:
    (v, cap), = items[:1]
    p = num(v)
    r, cx, cy = 130, W / 2, 210
    c = 2 * 3.14159 * r
    out = [svg_title(title),
           f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#e3e0d8" stroke-width="36"/>',
           f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ACCENT}" stroke-width="36" '
           f'stroke-dasharray="{c * p / 100:.1f} {c:.1f}" transform="rotate(-90 {cx} {cy})"/>',
           text(cx, cy + 22, v, 64, ACCENT, "middle", 800),
           text(cx, H - 20, cap, 22, INK, "middle")]
    return "".join(out)


def v_icons(title, items, check=False) -> str:
    """圖示清單：編號圓圈或打勾方框＋短標籤。"""
    out = [svg_title(title)]
    top = 46
    step = min(76, (H - top) / len(items))
    for i, (k, _) in enumerate(items):
        y = top + i * step
        out.append(f'<rect x="0" y="{y}" width="{W}" height="{step - 12:.0f}" rx="12" fill="{SOFT}"/>')
        cy = y + (step - 12) / 2
        if check:
            out.append(f'<rect x="18" y="{cy - 16:.0f}" width="32" height="32" rx="6" fill="#fff" stroke="{ACCENT}" stroke-width="3"/>')
            out.append(f'<path d="M24 {cy:.0f} l7 8 l14 -16" fill="none" stroke="{ACCENT}" stroke-width="4" stroke-linecap="round"/>')
        elif _ in GLYPHS:  # 項目寫成「名稱=圖示名」時畫圖示
            out.append(f'<circle cx="38" cy="{cy:.0f}" r="24" fill="{ACCENT}"/>')
            out.append(glyph(_, 38, cy))
        else:
            out.append(f'<circle cx="34" cy="{cy:.0f}" r="18" fill="{ACCENT}"/>')
            out.append(text(34, cy + 8, str(i + 1), 20, "#fff", "middle", 700))
        out.append(text(76, cy + 8, k, 24, INK, weight=600))
    return "".join(out)


def v_flow(title, items) -> str:
    out = [svg_title(title)]
    n = len(items)
    top = 50
    box = (H - top - (n - 1) * 34) / n
    for i, (k, _) in enumerate(items):
        y = top + i * (box + 34)
        out.append(f'<rect x="40" y="{y:.0f}" width="{W - 80}" height="{box:.0f}" rx="16" fill="{ACCENT if i == 0 else SOFT}"/>')
        out.append(text(W / 2, y + box / 2 + 12, k, 34, "#fff" if i == 0 else ACCENT, "middle", 800))
        if i < n - 1:
            ay = y + box + 4
            out.append(f'<path d="M{W / 2} {ay:.0f} v20 m-10 -10 l10 10 l10 -10" fill="none" stroke="{MUTED}" stroke-width="4" stroke-linecap="round"/>')
    return "".join(out)


def render_visual(spec: str) -> str:
    v = parse_visual(spec)
    k, t, items = v["kind"], v["title"], v["items"]
    body = {
        "bar": lambda: v_bar(t, items),
        "range": lambda: v_range(t, items),
        "bignum": lambda: v_bignum(t, items),
        "grid": lambda: v_grid(t, items),
        "donut": lambda: v_donut(t, items),
        "icons": lambda: v_icons(t, items),
        "checklist": lambda: v_icons(t, items, check=True),
        "flow": lambda: v_flow(t, items),
    }[k]()
    return (f'      <div class="visual" data-spec="{esc(spec)}">'
            f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{esc(t or k)}">{body}</svg></div>\n')


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
        lis = "\n".join(f"        <li>{esc(b)}</li>" for b in d["bullets"])
        vis = render_visual(d["visual"]) if d["visual"] else ""
        parts.append(
            f'  <section class="{cls}" data-draft="{p.stem}">\n'
            f'    <div class="slide-content">\n'
            f"      <h1>{esc(d['title'])}</h1>\n"
            f'      <div class="body">\n'
            f"      <ul>\n{lis}\n      </ul>\n{vis}"
            f"      </div>\n"
            f"      <p class=\"src\">出處：{esc(d['source'])}</p>\n"
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
