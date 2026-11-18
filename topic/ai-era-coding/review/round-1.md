# G3 忠實度審查 round-1

> 新開的 faithfulness-reviewer subagent（只讀工具），只給 drafts/、cards/、對應 wiki 頁、raw/text/、brief.md。以下為報告原文摘錄。

結果：13 頁中 10 頁 PASS，3 頁 FAIL（slide-04、slide-10、slide-13），三頁都退回 N4。沒有卡片需要退回 N2。40 張卡片的 quote 全部在 raw/text 找到原句，頁碼逐一核對一致。

## 逐頁判定
| 頁 | 判定 | 類型 | 問題句（節錄） | 原文依據 | 建議退回 |
|---|---|---|---|---|---|
| slide-01 | PASS | — | （附註）封面「完成時間反而多 19%」未寫熟悉大專案條件；slide-03 已補 | S1 p.1、p.12；S4 p.1 | — |
| slide-02 | PASS | — | 19%、11%、少招人、輔助型持平或上升、描述性，皆相符 | S4 p.1、p.3、p.4 | — |
| slide-03 | PASS | — | （附註）「常要大改」不在 C08 claim，但原文同頁有 major changes | S1 p.1、p.11、p.12 | — |
| slide-04 | FAIL | 遺漏重要條件 | 「另一研究：新手用 AI 練習，事後測驗與對照組相近」未標 S3 對象為 10–17 歲新手、S2 為有經驗工程師 | S3 p.1–2；S2 p.19 | N4 |
| slide-05 | PASS | — | 皆相符 | S2 p.12、p.18、p.19 | — |
| slide-06 | PASS | — | 皆相符 | S6 p.21、p.23；S3 p.11 | — |
| slide-07 | PASS | — | （附註）88% 未寫 2023 夏季、25 則中 22 則；秋季認可率約 39% | S5 p.2、p.4、p.5 | — |
| slide-08 | PASS | — | 皆相符，保留「可能」 | S2 p.6、p.11、p.12；S6 p.21 | — |
| slide-09 | PASS | — | 皆相符 | S3 p.2、p.13；S6 p.22 | — |
| slide-10 | FAIL | 遺漏重要條件 | 「研究者也建議先做排序題（未實測）」少了「用 AI 程式碼之前」「題目由那段程式碼產生」 | S3 p.14 | N4 |
| slide-10 | 同上 | 過度推論（輕微） | 「把題目拆成小步驟，一步一步問」原文只是觀察到部分學生這樣做，效果為推測 | S3 p.12–13 | N4 |
| slide-11 | PASS | — | 皆相符 | S2 p.14；S5 p.5；S6 p.5、p.21 | — |
| slide-12 | PASS | — | 皆相符 | S2 p.7；S6 p.21、p.22 | — |
| slide-13 | FAIL | 過度推論 | 「能看出 AI 哪裡錯，才用得好 AI」用「才」寫成必要條件；原文 "appears to be an important skill" | S6 p.21 | N4 |

## 卡片問題
無。完整度建議（非錯誤）：C06 quote 只摘 20%；C08 可補 major changes；C16/C17 數字緊接在 quote 後。

## 覆蓋率
brief 的 ①–⑥（含 ⑥ 五個子題）與總結皆有被回答；③ 的 S3 對象未標（即 slide-04 FAIL）。

## 總結
PASS 10／13。退回 N4：slide-04、slide-10、slide-13。退回 N2：無。
