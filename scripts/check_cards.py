"""N2 證據卡檢查。

- 必填欄位：id section claim numbers wiki source page quote
- wiki 頁存在，且該頁 frontmatter 的 sources 含此卡 source
- source 代號存在於 raw/sources.md；page 在範圍內
- quote 不超過 25 個英文字，且（正規化後）出現在 raw/text 該頁
- numbers 每個數字都出現在 quote 或原文該頁
- v2：必填 scope（對象、情境、保留語氣等適用條件）；keep 為選填清單（稿子引用此卡時，同頁至少要出現其中一個詞）
通過 exit 0，否則列出卡片編號與原因、exit 1。
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, find_quote, load_pages, load_sources, normalize, parse_list, split_frontmatter  # noqa: E402
from topic_common import load_cards  # noqa: E402

REQUIRED = ["id", "section", "claim", "scope", "numbers", "wiki", "source", "page", "quote"]  # v2 加 scope


def main() -> int:
    sources = load_sources()
    cards = load_cards()
    errors: list[str] = []
    if not cards:
        errors.append("cards/ 沒有任何卡片")
    for cid, c in cards.items():
        tag = f"{cid}（{c['_file']}）"
        missing = [k for k in REQUIRED if not c.get(k)]
        if missing:
            errors.append(f"{tag}：缺少欄位 {missing}")
            continue
        wiki = ROOT / c["wiki"]
        if not wiki.exists():
            errors.append(f"{tag}：wiki 頁不存在 {c['wiki']}")
        else:
            fm, _ = split_frontmatter(wiki.read_text(encoding="utf-8"))
            if c["source"] not in parse_list(fm.get("sources", "")):
                errors.append(f"{tag}：wiki 頁 {c['wiki']} 沒有引用 {c['source']}")
        if c["source"] not in sources:
            errors.append(f"{tag}：source {c['source']} 不在 raw/sources.md")
            continue
        pages = load_pages(sources[c["source"]])
        try:
            page = int(c["page"])
        except ValueError:
            errors.append(f"{tag}：page 不是數字")
            continue
        if not 1 <= page <= len(pages):
            errors.append(f"{tag}：page {page} 超出範圍（共 {len(pages)} 頁）")
            continue
        q = c["quote_text"]
        if len(q.split()) > 25:
            errors.append(f"{tag}：quote 有 {len(q.split())} 個英文字，超過 25")
        if not find_quote(q, pages, range(page, page + 1)):
            other = find_quote(q, pages)
            hint = f"（在第 {other} 頁找到）" if other else "（全文都找不到）"
            errors.append(f"{tag}：quote 不在 {c['source']} p.{page}{hint}")
        page_norm = normalize(pages[page - 1])
        q_norm = normalize(q)
        for n in c["numbers_list"]:
            core = re.sub(r"[^\d.,%]", "", n) or n
            if normalize(core) not in q_norm and normalize(core) not in page_norm:
                errors.append(f"{tag}：數字 {n} 不在 quote 也不在 {c['source']} p.{page}")

    if errors:
        print(f"check_cards 失敗：{len(errors)} 個問題（{len(cards)} 張卡）")
        for e in errors:
            print("  ✗", e)
        return 1
    print(f"check_cards 通過：{len(cards)} 張卡")
    return 0


if __name__ == "__main__":
    sys.exit(main())
