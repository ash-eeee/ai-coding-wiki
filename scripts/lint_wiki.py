"""Wiki lint：依 AGENTS.md §7 檢查 9 個項目。全部通過 exit 0，否則 exit 1。

用法：python3 scripts/lint_wiki.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    QUOTE_RE,
    WIKI,
    find_quote,
    han_count,
    load_pages,
    load_sources,
    parse_cites,
    parse_list,
    split_frontmatter,
)

SPECIAL = {"index.md", "log.md"}
ENTRY = SPECIAL | {"overview.md"}
LIMITS = {  # type: (資料夾, 數量上限, 每頁中文字上限)
    "source": ("sources", 6, 400),
    "concept": ("concepts", 4, 250),
    "comparison": ("comparisons", 2, 300),
    "topic": ("topics", 2, 500),
    "overview": (None, 1, 200),
}
MAX_PAGES = 15
RESULT_WORDS = ("發現", "顯示", "結果", "實驗", "受試", "參與者", "研究")
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
WIKI_LINK = re.compile(r"\[\[([^\]|#]+)")


def rel(p: Path) -> str:
    return p.relative_to(WIKI).as_posix()


def blocks(body: str):
    """把內文切成段落（空行分隔）；條列項目各自算一段；表格每列各自算一段。"""
    in_code = False
    buf: list[str] = []
    for line in body.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        s = line.strip()
        is_item = bool(re.match(r"^([-*]|\d+\.)\s", s)) or s.startswith("|")
        if not s or is_item or s.startswith("#"):
            if buf:
                yield " ".join(buf)
                buf = []
            if s:
                yield s
            continue
        buf.append(s)
    if buf:
        yield " ".join(buf)


def strip_cites_links(s: str) -> str:
    s = re.sub(r"\(S\d+,[^)]*\)", "", s)
    s = re.sub(r"\]\([^)]*\)", "]", s)
    return s


def main() -> int:
    errors: list[str] = []
    sources = load_sources()
    pages = sorted(p for p in WIKI.rglob("*.md"))
    names = {rel(p) for p in pages}
    stems = {p.stem: rel(p) for p in pages}
    inbound: dict[str, set[str]] = {n: set() for n in names}
    content_pages = [p for p in pages if p.name not in SPECIAL or p.parent != WIKI]

    type_counts: dict[str, int] = {}
    for p in pages:
        name = rel(p)
        text = p.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        is_special = name in SPECIAL

        # 8. frontmatter
        if not is_special:
            for k in ("type", "title", "sources", "updated"):
                if k not in fm:
                    errors.append(f"[8 frontmatter] {name}：缺少 `{k}`")
            t = fm.get("type", "")
            if t not in LIMITS:
                errors.append(f"[8 frontmatter] {name}：type `{t}` 不合法")
            else:
                folder = LIMITS[t][0]
                expect_dir = folder if folder else "."
                actual_dir = p.parent.relative_to(WIKI).as_posix() or "."
                if actual_dir != (expect_dir if folder else "."):
                    errors.append(f"[8 frontmatter] {name}：type `{t}` 應放在 wiki/{folder or ''}")
                type_counts[t] = type_counts.get(t, 0) + 1
            if not re.search(r"[一-鿿]", fm.get("title", "")):
                errors.append(f"[8 frontmatter] {name}：title 應為中文")
            if not re.fullmatch(r"[a-z0-9\-]+\.md", p.name):
                errors.append(f"[8 frontmatter] {name}：檔名需為英文小寫加連字號")

        # 1. 連結
        out_links = 0
        for target in MD_LINK.findall(body):
            if re.match(r"^[a-z]+://", target) or target.startswith("#"):
                continue
            t = (p.parent / target.split("#")[0]).resolve()
            try:
                tr = t.relative_to(WIKI.resolve()).as_posix()
            except ValueError:
                errors.append(f"[1 連結] {name}：連到 wiki 以外 `{target}`")
                continue
            if tr not in names:
                errors.append(f"[1 連結] {name}：連結目標不存在 `{target}`")
            else:
                out_links += 1
                if tr != name:
                    inbound[tr].add(name)
        for w in WIKI_LINK.findall(body):
            w = w.strip()
            if w in stems:
                out_links += 1
                inbound[stems[w]].add(name)
            else:
                errors.append(f"[1 連結] {name}：[[{w}]] 找不到頁面")
        if not is_special and out_links == 0:
            errors.append(f"[1 連結] {name}：沒有連到任何其他頁")

        if is_special:
            continue

        # 4／5／6／9. 段落、出處、引文、⚠
        cited_codes: set[str] = set()
        in_related = False
        han_total = 0
        for b in blocks(body):
            if b.startswith("#"):
                in_related = "相關頁面" in b
                continue
            plain = QUOTE_RE.sub("", strip_cites_links(b))
            han_total += han_count(plain)
            cites = parse_cites(b)
            for code, a, z in cites:
                cited_codes.add(code)
                if code not in sources:
                    errors.append(f"[5 出處] {name}：代號 {code} 不在 raw/sources.md")
                    continue
                n = len(load_pages(sources[code]))
                if a < 1 or z > n or a > z:
                    errors.append(f"[5 出處] {name}：{code} p.{a}–{z} 超出範圍（共 {n} 頁）")
            if b.startswith("⚠"):
                links = MD_LINK.findall(b)
                if not any("comparisons/" in l for l in links):
                    errors.append(f"[9 ⚠] {name}：⚠ 行沒有連到 comparisons/ 頁：{b[:40]}")
                continue
            if in_related:
                continue
            if set(b) <= set("|-: "):
                continue
            needs = bool(re.search(r"\d", plain)) or any(w in plain for w in RESULT_WORDS)
            if b.startswith("|") and b.count("|") > 2:
                # 表頭列（下一列是分隔線）不強制；以含數字或結果詞判斷
                pass
            if needs and not cites:
                errors.append(f"[4 出處] {name}：內容段落缺出處：{b[:50]}…")
            for q in QUOTE_RE.findall(b):
                if len(q.split()) < 3:
                    continue
                rngs = [(c, range(a, z + 1)) for c, a, z in cites if c in sources]
                if not rngs:
                    errors.append(f"[6 引文] {name}：引文沒有對應出處：\"{q[:40]}\"")
                    continue
                if not any(find_quote(q, load_pages(sources[c]), r) for c, r in rngs):
                    errors.append(f"[6 引文] {name}：引文在標註頁找不到：\"{q[:50]}\"")

        declared = set(parse_list(fm.get("sources", "")))
        if cited_codes - declared:
            errors.append(f"[8 frontmatter] {name}：內文引用 {sorted(cited_codes - declared)} 但 sources 未列")
        if declared - cited_codes and fm.get("type") != "overview":
            errors.append(f"[8 frontmatter] {name}：sources 列了 {sorted(declared - cited_codes)} 但內文沒引用")

        # 7. 字數
        t = fm.get("type")
        if t in LIMITS and han_total > LIMITS[t][2]:
            errors.append(f"[7 字數] {name}：{han_total} 字，超過 {t} 上限 {LIMITS[t][2]}")

    # 7. 頁數
    for t, cnt in type_counts.items():
        if cnt > LIMITS[t][1]:
            errors.append(f"[7 頁數] type {t} 有 {cnt} 頁，超過上限 {LIMITS[t][1]}")
    n_content = sum(type_counts.values())
    if n_content > MAX_PAGES:
        errors.append(f"[7 頁數] 全站 {n_content} 頁，超過上限 {MAX_PAGES}")

    # 2. 孤兒頁（index.md／log.md 的連結不算連入）
    for n in names:
        if n in ENTRY:
            continue
        real = {s for s in inbound[n] if s not in SPECIAL}
        if not real:
            errors.append(f"[2 孤兒] {n}：沒有其他內容頁連入")

    # 3. index 完整
    index_text = (WIKI / "index.md").read_text(encoding="utf-8")
    listed = {(WIKI / t).resolve().relative_to(WIKI.resolve()).as_posix() for t in MD_LINK.findall(index_text) if not re.match(r"^[a-z]+://", t)}
    for n in names - SPECIAL:
        if n not in listed:
            errors.append(f"[3 index] index.md 沒有列出 {n}")

    checked = len(content_pages)
    if errors:
        print(f"lint 失敗：{len(errors)} 個問題（檢查 {checked} 個檔案）")
        for e in errors:
            print("  ✗", e)
        return 1
    print(f"lint 通過：{checked} 個檔案，9 項檢查全部通過")
    for t in LIMITS:
        print(f"  ✓ {t}: {type_counts.get(t, 0)} 頁")
    return 0


if __name__ == "__main__":
    sys.exit(main())
