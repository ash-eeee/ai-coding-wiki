# G3 忠實度審查 round-3（workflow v2）

> 新開的 faithfulness-reviewer subagent（第 3 個實例）。輸入：v2 的 drafts（含 〔Cxx〕 標籤）、含 scope/keep 的 cards、對應 wiki 頁、raw/text、brief.md。

## 結果：11／13 PASS；退回 N4：slide-01、slide-04；退回 N2：C12

| 頁 | 判定 | 類型 | 問題 | 原文依據 | 建議退回 |
|---|---|---|---|---|---|
| slide-01 | FAIL | 遺漏重要條件 | 「資深工程師用 AI，完成時間反而多 19%」寫成通則，沒寫「熟悉的大型成熟專案」 | S1 p.12 "We caution readers against overgeneralizing…" | N4 |
| slide-02、03、05–08、11–13 | PASS | — | — | — | — |
| slide-04 | FAIL | 遺漏重要條件（近乎講錯） | 「沒寫過程式的中小學生」：原文是沒寫過**文字**程式，69 人中 64 人用過 Scratch／Code.org；且同頁第 5 點的「基礎」正是 Scratch 前測，自相矛盾 | S3 p.2、p.6、p.11 | N4（＋C12） |
| slide-09 | PASS（附註） | — | 「或範例」在卡片與原文找不到，輕微添加 | S3 p.13；S6 p.22 | — |
| slide-10 | PASS（附註） | — | 「學習模式」沒標未實測，與同頁其他點不一致 | S2 p.20 | — |

## 卡片問題
- **C12（退回 N2）**：`keep: ["沒寫過程式", "中小學生"]` 錯誤，與 scope「沒寫過文字程式」不一致；keep 會強制稿子寫出錯誤的「沒寫過程式」。
- C13（輕微）：scope 未寫「一週後保留測驗」「Scratch 前測」。
- C06、C16、C17（輕微）：quote 未含 claim 的全部數字，但數字在原文同頁正確。
- 其餘卡片 scope 正確。

## 覆蓋率
brief 所有問題都有被回答。

## 本輪觀察（記錄用）
- slide-04 的錯字是 G3 round-1 退回後我修改時引入的（「新手」→「沒寫過程式的中小學生」），v2 又把同一個錯誤寫進 C12 的 keep，等於用腳本把錯誤「鎖住」。
- slide-01 在 round-1、round-2 都只列為附註（PASS），round-3 判為 FAIL；slide-04 的同一用詞在 round-2 被列為「輕微」。不同審查實例的嚴格程度不一致。
