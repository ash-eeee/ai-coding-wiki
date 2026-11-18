# G3 忠實度審查 round-4（workflow v2）

> 新開的 faithfulness-reviewer subagent（第 4 個實例）。輸入同 round-3。
> 注意：本輪 prompt 多加一句「FAIL 只用於會讓讀者誤解原文的問題；不影響意思的用詞偏好請列為附註」（重申 agent 定義中「輕微的用詞偏好不算 FAIL」），以降低不同審查實例間的標準差異。

## 結果：13／13 PASS；不需退回 N4；不需退回 N2

| 頁 | 判定 | 附註 |
|---|---|---|
| slide-01 | PASS | A1：「應有水準」省略比較基準，slide-02 有完整寫 |
| slide-02 | PASS | — |
| slide-03 | PASS | A2：「常要大改」原文有支撐（S1 p.11），但 C08 沒涵蓋 |
| slide-04 | PASS | C12「沒寫過文字程式」、C10「有經驗的工程師」皆符合原文 |
| slide-05 | PASS | — |
| slide-06 | PASS | — |
| slide-07 | PASS | A3：88% 可補樣本數 25 則 |
| slide-08 | PASS | — |
| slide-09 | PASS | — |
| slide-10 | PASS | A4：「學習模式」未標未實測，與 C31 scope 不一致 |
| slide-11 | PASS | A5：「要自己驗證」為合理延伸；C20 省略 "appears to be"（slide-08、13），影響輕微 |
| slide-12 | PASS | — |
| slide-13 | PASS | 4 點都在前面頁出現過，無新論點 |

## 卡片問題
無需退回。keep 欄位都與原文一致。建議（非錯誤）：C06 quote 補 24% 那句；C08 claim 補「多數人表示常需大改」。

## 覆蓋率
brief 所有問題都有被回答。
