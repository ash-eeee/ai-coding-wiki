"""檢查腳本的自我測試（workflow v2，B0 階段執行）。

v1 執行時，check_cards／check_drafts 的 6 次失敗中有 3 次是腳本自己的 bug
（行尾連字號、CS50 被當數字、修法不完整又抓到「0」）。
v2 把這類問題往前移到 B0：先用已知的正反例測試共用函式，全部通過才開始跑 graph。
用法：python3 scripts/selftest.py（全部通過 exit 0）
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_drafts import ABSOLUTE_RE  # noqa: E402
from common import find_quote, normalize, parse_cites  # noqa: E402
from topic_common import TAG_RE, number_tokens  # noqa: E402

CASES = []


def case(name, got, want):
    CASES.append((name, got == want, got, want))


# 正規化與引文比對
page = "For example, this mini-\ntask could be a Parsons problem. AI aver-\nage speed\nﬁnd “bad” ones"
case("行尾斷字接回", find_quote("AI average speed", [page]), 1)
case("本來有連字號的複合字斷在行尾", find_quote("this mini-task could be", [page]), 1)
case("連字 ﬁ 與彎引號", find_quote('find "bad" ones', [page]), 1)
case("改一個字要找不到", find_quote("this maxi-task could be", [page]), None)
case("空白差異不影響", normalize("a  b\nc"), normalize("abc"))

# 數字擷取
case("CS50 不算數字", number_tokens("CS50 助教"), set())
case("GPT-4o 不算數字", number_tokens("GPT-4o"), set())
case("來源代號 S2 不算數字", number_tokens("S2 研究"), set())
case("範圍與百分比", number_tokens("22–25 歲 65%–86%"), {"22", "25", "65", "86"})
case("小數", number_tokens("1.8 倍"), {"1.8"})
case("一般數字", number_tokens("每 3 分鐘回 1 顆"), {"3", "1"})

# 出處解析
case("出處多來源", parse_cites("(S2, p.5–7; S3, p.8)"), [("S2", 5, 7), ("S3", 8, 8)])

# 絕對化用語
case("抓到「才用」", bool(ABSOLUTE_RE.search("能看出錯，才用得好")), True)
case("「不是因果證明」不算", bool(ABSOLUTE_RE.search("不是因果證明")), False)

# 重點卡片標籤
m = TAG_RE.search("差最多的是除錯題 〔C11, C12〕")
case("卡片標籤解析", m.group(1) if m else None, "C11, C12")


def main() -> int:
    bad = [c for c in CASES if not c[1]]
    for name, ok, got, want in CASES:
        print(("  ✓ " if ok else "  ✗ ") + name + ("" if ok else f"：得到 {got!r}，應為 {want!r}"))
    if bad:
        print(f"selftest 失敗：{len(bad)}/{len(CASES)}")
        return 1
    print(f"selftest 通過：{len(CASES)} 項")
    return 0


if __name__ == "__main__":
    sys.exit(main())
