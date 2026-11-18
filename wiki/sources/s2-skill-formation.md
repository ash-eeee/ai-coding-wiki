---
type: source
title: S2 Anthropic：用 AI 學新東西，學得會嗎
sources: [S2]
updated: 2026-11-18
---

# S2 Anthropic：用 AI 學新東西，學得會嗎

## 一句話

用 AI 學新的程式庫，測驗分數變低，速度也沒有明顯變快；但**怎麼用**差很多 (S2, p.1)。

## 研究怎麼做

- 52 位有 Python 經驗的程式設計師，第一次學 Trio 這個非同步程式庫，隨機分成用 AI（GPT-4o 助手）和不用 AI 兩組，各 26 人 (S2, p.6–7)。
- 35 分鐘內完成 2 個任務，之後**不准用 AI** 做測驗：除錯、讀程式、觀念三類題目 (S2, p.6–7)。

## 主要發現

- 用 AI 組測驗分數低 17%，約兩個等第 (S2, p.2)。原文："AI use impairs conceptual understanding, code reading, and debugging abilities" (S2, p.1)
- 兩組差最多的是**除錯題** (S2, p.11)。不用 AI 組遇到更多錯誤並自己解決，作者認為這正是學到東西的原因 (S2, p.12)。
- 速度沒有顯著差別；全部交給 AI 的人最快（19.5 分鐘），但只占用 AI 組約 20% (S2, p.19)。
- 6 種用法中，高分組（65–86%）只問觀念、或要求程式碼附解釋；低分組（24–39%）是全交給 AI 或一直叫 AI 除錯 (S2, p.18–19)。

## 限制與適用條件

- 只測 1 小時、1 個程式庫；受試者是專業或接案工程師，不是學生 (S2, p.19)。
- 用的是聊天式 AI；作者推測代理式（agentic）工具卸載更多 (S2, p.19)。

⚠ 與 S3 結論不同，見[S3 vs S2](../comparisons/s3-vs-s2-novice-learning.md)

## 相關頁面

- [認知卸載](../concepts/cognitive-offloading.md)
- [該怎麼學程式](../topics/how-to-learn.md)
- [為什麼還要學程式](../topics/why-learn.md)
