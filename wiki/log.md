---
type: log
title: Wiki 紀錄
---

# Wiki 紀錄

> 只追加、不改寫。查最近 5 筆：`grep "^## \[" wiki/log.md | tail -5`

## [2026-11-18] schema | 依訪談結果建立 AGENTS.md
- 依 `process/interview.md` 需求摘要生成 `AGENTS.md`、`CLAUDE.md`、`index.md`、`log.md`。
- 使用者指示訪談後「不用再確認，直接做完」：之後的確認點照常產出內容，但不停下等待。

## [2026-11-18] ingest | S1 METR 資深開發者生產力實驗
- 重點（5 行）：
  1. RCT：16 位資深開源開發者、246 個真實任務，隨機決定可否用 AI
  2. 預估快 24%、自評快 20%，實測慢 19%
  3. 專家也預估快 38–39%
  4. AI 產出接受率 < 44%，約 9% 時間在清理 AI 程式碼；越熟的專案越慢
  5. 作者提醒：只適用熟悉的大型專案；小型新專案或不熟的程式碼可能加速
- 新增頁面：sources/s1-metr-productivity.md、concepts/rct.md、topics/why-learn.md、overview.md
- lint：第 1 輪失敗 2 項（條列編號被誤判為數字；概念頁白話定義被要求出處）→ 修 lint_wiki.py 與 AGENTS.md §4 → 第 2 輪通過
- 重點清單未停下等使用者確認（使用者指示直接做完）

## [2026-11-18] ingest | S2 Anthropic 技能養成研究
- 重點（5 行）：
  1. RCT：52 位有 Python 經驗者學新程式庫 Trio，用 AI（GPT-4o）vs 不用 AI，各 26 人
  2. 事後不用 AI 的測驗：AI 組低 17%；差距最大在除錯題
  3. 速度無顯著差異；全交給 AI 的人最快但只占約 20%
  4. 6 種用法：高分（65–86%）＝只問觀念或要求解釋；低分（24–39%）＝全交給 AI、靠 AI 除錯
  5. 限制：1 小時、1 個程式庫、受試者為專業工程師而非學生
- 新增頁面：sources/s2-skill-formation.md、concepts/cognitive-offloading.md、topics/how-to-learn.md；更新 topics/why-learn.md、overview.md、index.md
- 與 S1 的關係：兩者都沒看到 AI 帶來顯著加速，但 S1 是資深者做熟悉專案、S2 是學新東西，條件不同（不構成矛盾，未建比較頁）
- lint：第 1 輪通過

## [2026-11-18] ingest | S3 初學者用 Codex 學 Python
- 重點（5 行）：
  1. 69 位 10–17 歲、沒寫過文字程式的學生，一半可用 Codex
  2. 45 個寫程式任務，每題後接一個不能用 AI 的改程式任務（use-modify-create）
  3. 練習時正確率 1.8 倍、時間 0.57 倍；改程式能力沒有變差
  4. 一週後保留測驗 Codex 組略高但不顯著；前測高分者受益較多
  5. 與 S2 看似矛盾 → 建比較頁，說明對象、AI 用法、測驗方式不同
- 新增頁面：sources/s3-novices-codex.md、comparisons/s3-vs-s2-novice-learning.md；更新 S2 摘要頁（加 ⚠）、兩個主題頁、overview、index
- lint：第 1 輪失敗 2 項（來源代號「S3」被當成數字，要求出處）→ 修 lint_wiki.py → 第 2 輪通過

## [2026-11-18] ingest | S4 Canaries 就業研究（2026 年 8 月修訂版）
- 重點（5 行）：
  1. ADP 薪資資料、每月 350–500 萬人、到 2026 年 6 月；本 wiki 用最新修訂版
  2. 整體沒有大量取代；高曝險職業 22–25 歲就業比應有水準低 19%，資深者無類似落差
  3. 主要是少招新人；集中在 AI「取代」型職業，「輔助」型持平或上升
  4. 機制推測：AI 取代明文知識、輔助經驗知識（與 S1「AI 不懂默契」呼應）
  5. 作者強調是描述性、非因果；不預測未來
- 新增頁面：sources/s4-canaries-employment.md、concepts/ai-exposure.md；更新 topics/why-learn.md（新增 ①）、overview、index
- lint：第 1 輪通過；但自我檢查發現主題頁「帶走的觀念」寫了 S4 沒說的推論（入門門檻會變高），lint 抓不到無數字、無結果詞的推論句 → 改寫為有出處的句子

## [2026-11-18] ingest | S5 哈佛 CS50 導入 AI 助教
- 重點（5 行）：
  1. 不禁止 AI，改用課程自製、「只引導不給答案」的 AI 工具，限制商用工具
  2. 工具：解釋程式碼、程式風格說明、聊天助教 CS50 Duck；論壇回答由助教把關
  3. 愛心機制限制提問次數，鼓勵想清楚再問
  4. 問卷多為正面（47% 非常有幫助）；課程問題回答 88% 正確
  5. 限制：非匿名問卷，沒有學習成效對照實驗
- 新增頁面：sources/s5-cs50-ai.md；更新 topics/how-to-learn.md（新增 ⑤）、overview、index；why-learn 的「帶走的觀念」補上出處 (S1, p.12)
- lint：第 1 輪通過（另手動把 S5 頁的小標改成 AGENTS.md 規定的骨架名稱，lint 目前不檢查骨架）

## [2026-11-18] ingest | S6 The Widening Gap 初學者與生成式 AI
- 重點（5 行）：
  1. 美國一所大學 CS1 的 21 名學生，可用 Copilot、ChatGPT 解一題，觀察＋訪談＋眼動追蹤
  2. 20/21 完成；加速的學生能忽略錯誤或無用的 AI 建議
  3. 卡住的 10 人中 9 人靠 AI 做出答案，卻多半以為自己懂了（能力錯覺）
  4. 新的後設認知困難：被打斷、被誤導、自以為跟上進度；成績低者較多
  5. 與 S5「像私人家教」的問卷印象對照 → 建第二個比較頁「感覺 vs 實際」
- 新增頁面：sources/s6-widening-gap.md、concepts/metacognition.md、comparisons/feeling-vs-reality.md；更新 S5 摘要頁（加 ⚠）、兩個主題頁（how-to-learn 補齊 ⑥ 五個子題）、overview、index
- 頁數達上限：15/15（source 6、concept 4、comparison 2、topic 2、overview 1）
- lint：第 1 輪通過
