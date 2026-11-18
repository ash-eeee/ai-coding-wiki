"""G1 覆蓋率關卡：brief 的每段都要有足夠的 wiki 頁支撐。

規則：
- ①–⑥ 每段至少 2 個不同的 wiki 頁
- sources.md 列出的頁面都存在
- ⑥ 的每個子題至少 1 個 wiki 頁
通過 exit 0；不足時輸出缺口清單、exit 1（流程應停下回報，不硬湊）。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from topic_common import ROOT, SECTIONS, parse_brief, parse_sources  # noqa: E402


def main() -> int:
    errors = []
    sections, subs = parse_brief()
    sec_pages, sub_pages = parse_sources()

    for s in SECTIONS:
        if s not in sections:
            errors.append(f"brief.md 缺少段落 {s}")
    if not subs:
        errors.append("brief.md 缺少「### ⑥ 子題」清單")

    for s in SECTIONS:
        pages = sec_pages.get(s, [])
        for p in pages:
            if not (ROOT / p).exists():
                errors.append(f"{s}：{p} 不存在")
        uniq = set(pages)
        if len(uniq) < 2:
            errors.append(f"{s}（{sections.get(s, '')}）只有 {len(uniq)} 個 wiki 頁，至少要 2 個")
        else:
            print(f"  ✓ {s}：{len(uniq)} 頁")

    for sub in subs:
        pages = sub_pages.get(sub, [])
        if not pages:
            errors.append(f"⑥ 子題「{sub}」沒有對應 wiki 頁")
        else:
            print(f"  ✓ ⑥ {sub}：{len(set(pages))} 頁")

    if errors:
        print(f"G1 覆蓋率不足：{len(errors)} 個缺口")
        for e in errors:
            print("  ✗", e)
        return 1
    print("G1 覆蓋率通過")
    return 0


if __name__ == "__main__":
    sys.exit(main())
