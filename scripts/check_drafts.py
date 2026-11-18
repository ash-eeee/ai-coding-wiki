"""N4 逐頁稿檢查（workflow v2）。

v1 規則：
- 頁數 12–15，且與 outline.md 的頁一一對應
- 每頁有標題、出處列、卡片列
- 引用的卡片都存在，且屬於大綱指定給該頁的卡片
- 出處列要涵蓋所引卡片的 source 代號
- 每頁重點 3–5 個，每個重點不超過 40 個中文字

v2 新增（把 G3 常抓到的問題往前移）：
- 每個重點結尾必須標 〔Cxx〕；只有問句（以「？」結尾）可以不標
- 數字改為逐點比對：每個重點的數字，必須出現在「該重點」標的卡片 numbers
- 條件保留：卡片有 keep 清單時，同一頁引用該卡片的非問句重點中，至少要出現 keep 裡的一個詞
- 絕對化用語：重點不得出現「才能、才會、才用、一定、絕對、必定、保證、證明了」等把相關說成必要條件的詞
- 總結頁（最後一頁）引用的卡片，都必須在前面的頁出現過（總結不得有新論點）
通過 exit 0，否則 exit 1。
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from topic_common import draft_files, han_count, load_cards, number_tokens, parse_draft, parse_outline  # noqa: E402

MIN_PAGES, MAX_PAGES = 12, 15
MIN_B, MAX_B, MAX_HAN = 3, 5, 40
ABSOLUTE_RE = re.compile(r"才(能|會|用|可以|算)|一定|絕對|必定|保證|證明了")


def is_question(b: str) -> bool:
    return b.rstrip().endswith(("？", "?"))


def main() -> int:
    errors: list[str] = []
    cards = load_cards()
    outline = parse_outline()
    files = draft_files()
    n = len(files)
    if not MIN_PAGES <= n <= MAX_PAGES:
        errors.append(f"頁數 {n}，應在 {MIN_PAGES}–{MAX_PAGES}")
    names = {p.stem for p in files}
    for s in outline:
        if s not in names:
            errors.append(f"大綱有 {s} 但 drafts/ 沒有")
    seen_before_last: set[str] = set()
    for idx, p in enumerate(files):
        name = p.stem
        d = parse_draft(p)
        tag = name
        if name not in outline:
            errors.append(f"{tag}：大綱沒有這一頁")
        if not d["title"]:
            errors.append(f"{tag}：缺標題")
        if not d["source"]:
            errors.append(f"{tag}：缺出處列")
        if not d["cards"]:
            errors.append(f"{tag}：缺卡片列")
        allowed = set(outline.get(name, []))
        for cid in d["cards"]:
            if cid not in cards:
                errors.append(f"{tag}：卡片 {cid} 不存在")
                continue
            if cid not in allowed:
                errors.append(f"{tag}：卡片 {cid} 不在大綱指定的 {sorted(allowed)}")
            src = cards[cid].get("source", "")
            if src and src not in d["source"]:
                errors.append(f"{tag}：出處列沒有卡片 {cid} 的來源 {src}")

        # 標題的數字：對全頁卡片比對
        page_nums: set[str] = set()
        for cid in d["cards"]:
            if cid in cards:
                for x in cards[cid]["numbers_list"]:
                    page_nums |= number_tokens(x)
        for token in number_tokens(d["title"]):
            if token not in page_nums:
                errors.append(f"{tag}：標題數字 {token} 不在本頁卡片 numbers")

        nb = len(d["bullets"])
        if not MIN_B <= nb <= MAX_B:
            errors.append(f"{tag}：重點 {nb} 個，應為 {MIN_B}–{MAX_B}")
        keep_hits: dict[str, bool] = {}
        for b, bcards in zip(d["bullets"], d["bullet_cards"]):
            short = b[:18] + "…"
            h = han_count(b)
            if h > MAX_HAN:
                errors.append(f"{tag}：重點超過 {MAX_HAN} 字（{h} 字）：{short}")
            if ABSOLUTE_RE.search(b):
                errors.append(f"{tag}：重點有絕對化用語「{ABSOLUTE_RE.search(b).group(0)}」：{short}")
            if not bcards:
                if not is_question(b):
                    errors.append(f"{tag}：重點沒有標卡片 〔Cxx〕：{short}")
                continue
            nums: set[str] = set()
            for cid in bcards:
                if cid not in d["cards"]:
                    errors.append(f"{tag}：重點標的 {cid} 不在本頁卡片列")
                if cid not in cards:
                    continue
                for x in cards[cid]["numbers_list"]:
                    nums |= number_tokens(x)
                if cards[cid]["keep_list"] and not is_question(b):
                    keep_hits.setdefault(cid, False)
                    if any(k in b for k in cards[cid]["keep_list"]):
                        keep_hits[cid] = True
            for token in number_tokens(b):
                if token not in nums:
                    errors.append(f"{tag}：數字 {token} 不在該重點所標卡片 {bcards} 的 numbers：{short}")
        for cid, hit in keep_hits.items():
            if not hit:
                errors.append(f"{tag}：引用 {cid} 但沒保留條件詞 {cards[cid]['keep_list']}")

        if idx < n - 1:
            seen_before_last |= set(d["cards"])
        else:
            new = [c for c in d["cards"] if c not in seen_before_last]
            if new:
                errors.append(f"{tag}（總結頁）：卡片 {new} 沒在前面的頁出現過，總結不得有新論點")

    if errors:
        print(f"check_drafts 失敗：{len(errors)} 個問題（{n} 頁）")
        for e in errors:
            print("  ✗", e)
        return 1
    print(f"check_drafts 通過：{n} 頁（v2 規則）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
