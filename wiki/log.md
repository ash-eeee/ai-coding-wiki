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
