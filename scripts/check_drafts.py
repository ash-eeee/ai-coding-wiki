"""N4 逐頁稿檢查。

- 頁數 12–15，且與 outline.md 的頁一一對應
- 每頁有標題、出處列、卡片列
- 引用的卡片都存在，且屬於大綱指定給該頁的卡片
- 出處列要涵蓋所引卡片的 source 代號
- 稿中（標題＋重點）每個數字都出現在所引卡片的 numbers
- 每頁重點 3–5 個，每個重點不超過 40 個中文字
通過 exit 0，否則 exit 1。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from topic_common import draft_files, han_count, load_cards, number_tokens, parse_draft, parse_outline  # noqa: E402

MIN_PAGES, MAX_PAGES = 12, 15
MIN_B, MAX_B, MAX_HAN = 3, 5, 40


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
    for p in files:
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
        nums_allowed: set[str] = set()
        for cid in d["cards"]:
            if cid not in cards:
                errors.append(f"{tag}：卡片 {cid} 不存在")
                continue
            if cid not in allowed:
                errors.append(f"{tag}：卡片 {cid} 不在大綱指定的 {sorted(allowed)}")
            src = cards[cid].get("source", "")
            if src and src not in d["source"]:
                errors.append(f"{tag}：出處列沒有卡片 {cid} 的來源 {src}")
            for x in cards[cid]["numbers_list"]:
                nums_allowed |= number_tokens(x)
        for token in number_tokens(d["title"] + " " + " ".join(d["bullets"])):
            if token not in nums_allowed:
                errors.append(f"{tag}：數字 {token} 不在所引卡片的 numbers {sorted(nums_allowed)}")
        nb = len(d["bullets"])
        if not MIN_B <= nb <= MAX_B:
            errors.append(f"{tag}：重點 {nb} 個，應為 {MIN_B}–{MAX_B}")
        for b in d["bullets"]:
            h = han_count(b)
            if h > MAX_HAN:
                errors.append(f"{tag}：重點超過 {MAX_HAN} 字（{h} 字）：{b[:20]}…")

    if errors:
        print(f"check_drafts 失敗：{len(errors)} 個問題（{n} 頁）")
        for e in errors:
            print("  ✗", e)
        return 1
    print(f"check_drafts 通過：{n} 頁")
    return 0


if __name__ == "__main__":
    sys.exit(main())
