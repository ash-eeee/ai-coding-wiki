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
