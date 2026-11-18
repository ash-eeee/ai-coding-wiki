# 作業執行說明（給 Claude Code）

> 你是這個專案的執行者。請完整讀完本檔與 `llm-wiki.md` 後再開始動作。
> 所有對話、檔案內容一律使用**台灣繁體中文與台灣用詞**（例：程式碼、檔案、資訊、預設、專案、螢幕；不要用代碼、文件、信息、默認、項目、屏幕）。
> 遇到標示【停下等使用者】的地方，一定要停下來等使用者回覆，不可自行往下做。

---

## 0. 作業概要

- 課程：生成式 AI，第 10 週「把你的工作拆成 AI 能做的流程」
- 作業：先建立一個 LLM Wiki，再以 Wiki 為唯一知識來源，產出一份**教學型 HTML 簡報**；並說明 loop / graph 設計、附實際執行與檢查紀錄、寫反思。
- 主題：**AI 時代，程式該學到什麼程度？該怎麼學？**
- 繳交期限：2026/11/23 23:59
- Repo：`ai-coding-wiki`（GitHub public repo，已 clone 到本地，就是目前這個資料夾）
- 設計原則：**Graph 為主、Loop 為輔**——graph 決定大流程，每一個節點內部是有次數上限的小 loop。

評分重點（請隨時對照）：
1. Wiki 資料與簡報內容有明確對應（每頁簡報都能追溯到 wiki 頁與原始資料）
2. loop / graph 設計合理且說明清楚
3. 有實際執行與檢查紀錄
4. 反思：哪個節點最常出錯、檢查往前移到哪裡
5. 簡報有清楚的教學結構

---

## 1. 必須遵守的規則

1. **LLM Wiki 的做法一律依照 `llm-wiki.md`**（Karpathy 的 LLM Wiki 構想）：三層架構（raw / wiki / schema）、三種操作（ingest / query / lint）、`index.md` 與 `log.md` 的用法。本檔只補充這份作業特有的設定，兩者衝突時以本檔為準。
2. **規則書只維護一份**：主要內容寫在 `AGENTS.md`；`CLAUDE.md` 只寫一行 `@AGENTS.md`。`AGENTS.md` 控制在 12,000 字元以內，細節（例如簡報流程）拆到 skill。
3. **`raw/` 不可修改**，只能讀。
4. **論文 PDF 不可推上 GitHub**（版權考量）：`.gitignore` 排除 `raw/*.pdf` 與 `raw/text/`（PDF 轉出的純文字）。另建 `raw/sources.md` 列出每篇的標題、作者、年份、原始連結，這份要推上去。
5. **不放任何個資或機密**。
6. **「檢查一下」不算驗證**：凡是能用程式檢查的，一律寫成 `scripts/` 裡的 Python 腳本並實際執行；AI 審查一律交給**新的 subagent**，只給它成品與來源，不給它製作過程。
7. **每過一個節點就 git commit**，commit 訊息用格式：`[節點代號] 說明`，例如 `[N2] 產生證據卡 12 張，check_cards 通過`。
8. **不准硬湊**：wiki 裡找不到的內容，不得用模型自身知識補進簡報。資料不足就停下回報。
9. **不要捏造執行紀錄或反思**：report 與反思只能根據實際發生的檢查結果撰寫。

---

## 2. 目標資料夾結構

```
ai-coding-wiki/
├── CLAUDE.md                  # 只有一行：@AGENTS.md
├── AGENTS.md                  # Wiki 規則書（訪談後才生成）
├── llm-wiki.md                # Karpathy 原文（使用者提供，不修改）
├── HOMEWORK_GUIDE.md          # 本檔
├── README.md                  # 繳交總覽頁（最後產生）
├── .gitignore
├── raw/
│   ├── sources.md             # 推上 GitHub
│   ├── *.pdf                  # 不推
│   └── text/*.txt             # PDF 轉純文字，給腳本比對用，不推
├── wiki/
│   ├── index.md
│   ├── log.md
│   └── …（摘要頁、概念頁、比較頁等，依訪談結果決定）
├── process/
│   ├── interview.md           # 「先討論」訪談紀錄（問題、回答、需求摘要）
│   └── workflow-changes.md    # workflow 修改紀錄（反思用）
├── scripts/
│   ├── lint_wiki.py
│   ├── check_coverage.py
│   ├── check_cards.py
│   ├── check_drafts.py
│   └── check_render.py
├── .claude/
│   ├── skills/topic-slides/SKILL.md      # 簡報 graph 的完整規格
│   └── agents/faithfulness-reviewer.md   # 忠實度審查 subagent
├── topic/ai-era-coding/       # 簡報流程每一關的產出（狀態都是檔案）
│   ├── brief.md
│   ├── sources.md
│   ├── cards/
│   ├── outline.md
│   ├── drafts/
│   ├── review/
│   └── report.md
└── slides/
    └── index.html             # 最終簡報（GitHub Pages 會提供網址）
```

---

## 3. 原始資料（6 篇）

請先嘗試自動下載到 `raw/`；下載失敗的，列出清單請使用者手動下載放進 `raw/`【停下等使用者】。

| 代號 | 檔名建議 | 資料 | 連結 |
|---|---|---|---|
| S1 | `metr-2025-dev-productivity.pdf` | Becker et al. (2025). *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*. METR | https://arxiv.org/abs/2507.09089 |
| S2 | `anthropic-2026-skill-formation.pdf` | Shen & Tamkin (2026). *How AI Impacts Skill Formation*. Anthropic（部落格：https://www.anthropic.com/research/AI-assistance-coding-skills ） | https://arxiv.org/abs/2601.20245 |
| S3 | `kazemitabaar-2023-novices-codex.pdf` | Kazemitabaar et al. (2023). *Studying the effect of AI Code Generators on Supporting Novice Learners in Introductory Programming*. CHI '23 | https://arxiv.org/abs/2302.07427 |
| S4 | `brynjolfsson-2025-canaries.pdf` | Brynjolfsson, Chandar & Chen (2025). *Canaries in the Coal Mine? Six Facts about the Recent Employment Effects of Artificial Intelligence*. Stanford Digital Economy Lab（**請下載最新修訂版**） | https://digitaleconomy.stanford.edu/publications/canaries-in-the-coal-mine/ |
| S5 | `liu-2024-teaching-cs50-with-ai.pdf` | Liu, Zenke, …, Malan (2024). *Teaching CS50 with AI*. SIGCSE 2024 | https://cs.harvard.edu/malan/publications/V1fp0567-liu.pdf |
| S6 | `prather-2024-widening-gap.pdf` | Prather et al. (2024). *The Widening Gap: The Benefits and Harms of Generative AI for Novice Programmers*. ICER 2024 | https://arxiv.org/abs/2405.17739 |

下載後用 `pdftotext -layout` 把每篇轉成 `raw/text/<同檔名>.txt`，並在 `raw/sources.md` 記錄每篇的書目資料與連結。

註：作者名單以 PDF 首頁為準，上表若與 PDF 不符，以 PDF 為準並修正 `raw/sources.md`。

---

## 4. 階段 A：建立 LLM Wiki（先討論、後生成）

### A1. 準備
1. 確認 git、Python 3 可用；建立 `.gitignore`（見規則 4）。
2. 下載資料（第 3 節）。
3. commit：`[A1] 專案初始化與原始資料清單`

### A2. 訪談（先討論）【整段都要等使用者回答】
**先不要建立任何 wiki 檔案或 AGENTS.md。** 請以 `llm-wiki.md` 為基礎，**一次只問一個問題**，共約 8–10 題，幫使用者釐清需求。至少要問到這 8 個面向：

1. 讀者是誰
2. 需要哪些類型的頁面（摘要頁、概念頁、比較頁…）
3. 用什麼語言撰寫
4. 出處要標多細
5. 資料互相矛盾時怎麼處理
6. 一次 ingest 一篇，還是批次
7. 之後要用這個 wiki 產出什麼
8. lint 要檢查什麼

問完後整理成**需求摘要**給使用者確認。使用者確認後，把全部問答與最終需求摘要存成 `process/interview.md`。

### A3. 生成規則書
1. 依需求摘要生成 `AGENTS.md`、`CLAUDE.md`（一行 `@AGENTS.md`）、`wiki/index.md`、`wiki/log.md`。
2. 產出一張「需求摘要 ↔ AGENTS.md 對照表」給使用者逐條檢查【停下等使用者】。
3. commit：`[A3] 依訪談結果生成 AGENTS.md`

### A4. 寫 lint 腳本 `scripts/lint_wiki.py`
至少檢查：
- `[[連結]]` 或 markdown 連結指向的頁面是否存在
- 孤兒頁（沒有任何頁面連入，`index.md` 與 `log.md` 除外）
- `index.md` 是否列出 `wiki/` 內所有頁面
- 每個事實句是否標註出處（格式依 AGENTS.md，例如 `(S2, p.5)`）
- 輸出：通過／失敗清單，失敗時 exit code 非 0

### A5. 逐篇 ingest（每篇一個小 loop）
對 S1–S6 依序執行：
```
讀原文 → 跟使用者討論重點【停下等使用者】→ 寫摘要頁、更新概念頁/比較頁、index、log
      → 執行 lint_wiki.py → 未通過就修（最多 2 輪；仍失敗就停下回報）→ commit
```
- commit：`[A5] ingest S2 Anthropic 技能養成研究，lint 通過`
- 特別注意標出**來源之間的矛盾或條件差異**（例如 S3 初學者表現變好 vs S2 理解程度下降；兩者受試者、測驗方式不同）。
- 數字一律以原文為準；二手報導的數字常彼此不一致，**不採用二手報導**。

### A6. 完成後執行一次全 wiki lint，commit：`[A6] wiki 完成 6 篇 ingest，全站 lint 通過`

---

## 5. 階段 B：用 Wiki 產生教學 HTML 簡報（Graph + 小 Loop）

### B0. 先把流程寫成可重複執行的規格
1. 把本節完整流程寫進 `.claude/skills/topic-slides/SKILL.md`（目標、限制、完成標準、停止條件、觸發方式、每個節點能看什麼／能改什麼、退回路線）。
2. 建立 `.claude/agents/faithfulness-reviewer.md`：只開放讀取工具；輸入只有 `drafts/`、`cards/`、對應的 `wiki/` 頁面與 `raw/text/`；不能修改任何檔案。
3. 寫好 `scripts/` 的四支檢查腳本（見下方各關卡）。
4. commit：`[B0] 建立 topic-slides 流程規格、審查 subagent 與檢查腳本`

### 簡報規格（寫進 brief.md）
- 語言：台灣繁體中文
- 聽眾：有一點資訊背景、看得懂程式但不會自己實際應用的大學生
- 要求：簡單、有邏輯架構；每頁 3–5 個重點，句子短
- 頁數：13 頁左右（容許 12–15 頁）
- 每頁底部標出處（wiki 頁名＋原始資料代號）
- 簡報只放教學內容，**不放製作流程說明**（流程說明放 README）

結構（前段精簡、⑥ 加重）：

| 段落 | 頁數 | 要回答的問題 | 主要來源 |
|---|---|---|---|
| 封面＋開場問題 | 1 | — | — |
| ① 為什麼還要學 | 1 | AI 會寫程式了，學程式還有意義嗎？ | S4 |
| ② AI 真的讓人變快嗎 | 1 | 感覺變快＝實際變快嗎？ | S1 |
| ③ 用 AI 學得會嗎 | 1 | 初學者用 AI 會學得更好還是更差？ | S3、S2 |
| ④ 差別在怎麼用 | 2 | 哪些用法有學到、哪些沒有？ | S2、S6 |
| ⑤ 學校怎麼教 | 1 | AI 當助教、不當槍手是什麼意思？ | S5 |
| ⑥ 該學到哪、怎麼學 | 5 | 必備能力（讀懂、除錯、撰寫、觀念）、學習階段、具體練習方法、用 AI 的守則、自我檢查清單 | S2、S3、S5、S6（＋其他 wiki 頁） |
| 總結 | 1 | 一句話帶走什麼？ | — |

### Graph 全貌

```
N0 簡報規格 brief.md
 ↓
N1 檢索 wiki → sources.md
 ↓
G1 覆蓋率關卡［腳本 check_coverage.py］── 不足 → 停下回報（不硬湊）
 ↓
N2 證據卡 cards/*.md      ⟲ 小 loop：寫卡 → check_cards.py → 修（最多 2 輪）
 ↓
N3 大綱 outline.md
 ↓
H1【使用者確認大綱】── 退回 → 修 N3；缺證據 → 回 N1 補檢索
 ↓
N4 逐頁稿 drafts/slide-XX.md   ⟲ 小 loop：寫 → check_drafts.py → 修（最多 2 輪）
 ↓
G3 忠實度審查［AI：faithfulness-reviewer subagent］
     ── 某頁講反／過度推論 → 只退回那一頁到 N4
     ── 證據卡本身錯 → 退回 N2 重抽那張卡
 ↓
N5 渲染 slides/index.html   ⟲ 小 loop：產生 → 截圖 → 修版面（最多 2 輪）
 ↓
G4 渲染檢查［腳本 check_render.py］── 字太多造成溢出 → 退回 N4 縮短（不准縮小字體）
 ↓
N6 交件 report.md
```

**全域剎車**：同一個關卡累計退回 3 次仍未通過，停下交給使用者判斷【停下等使用者】。

### 每個節點能看什麼、能改什麼

| 節點 | 能看 | 產出 | 不能做 |
|---|---|---|---|
| N1 檢索 | `wiki/`（從 `index.md` 開始） | `sources.md`：每個要回答的問題對應哪些 wiki 頁 | 讀 `raw/` 以外的外部資料、上網 |
| N2 證據卡 | `sources.md` 列出的 wiki 頁、`raw/text/` | `cards/C01.md`… | 混用其他來源、用模型自身知識 |
| N3 大綱 | `brief.md`、`cards/` | `outline.md`：每頁標題＋要用的卡片編號 | 新增沒有卡片支撐的論點 |
| N4 逐頁稿 | `outline.md`＋該頁指定的卡片 | `drafts/slide-01.md`… | 引用指定卡片以外的內容 |
| N5 渲染 | 已通過 G3 的 `drafts/` | `slides/index.html` | 改任何一個字（排版時想讓句子更順也不行） |
| G 關卡 | 成品＋來源 | 檢查報告 | 動手修改成品 |

### 各節點細節

**N0 簡報規格**：依上方簡報規格寫 `brief.md`，包含每段要回答的問題與預定頁數。

**N1 檢索**：從 `wiki/index.md` 找頁面，產出 `sources.md`，格式：
```
## ① 為什麼還要學
- wiki/xxx.md — 一句說明為什麼相關
```

**G1 覆蓋率關卡 `check_coverage.py`**：
- 讀 `brief.md` 的段落清單與 `sources.md`
- 規則：每段至少 2 個 wiki 頁、且 `sources.md` 列出的頁面都存在；⑥ 每一頁的主題都要有對應 wiki 頁
- 不足 → 輸出缺口清單並停下回報，不往下做

**N2 證據卡**：一張卡＝一個論點。格式：
```
---
id: C07
section: ④
claim: （中文，一句話的論點）
numbers: ["50%", "67%"]
wiki: wiki/xxx.md
source: S2
page: 5
quote: "（英文原文短句，25 個英文字以內，必須逐字出現在原文）"
---
```

**`check_cards.py`**：
- 必填欄位齊全、`wiki` 頁存在、`source` 代號存在於 `raw/sources.md`
- `quote` 在正規化空白、換行、連字號斷字後，能在 `raw/text/<source>.txt` 中找到
- `numbers` 中每個數字都出現在 `quote` 或原文對應頁
- 失敗列出卡片編號與原因

**N3 大綱**：依簡報結構表，每頁寫標題、教學目標（一句話）、使用卡片編號。完成後【停下等使用者】確認（H1）。

**N4 逐頁稿**：每頁一個 md，含：標題、3–5 個重點、出處列（`wiki 頁名｜S2 p.5`）、使用的卡片編號。

**`check_drafts.py`**：
- 每頁都有出處列；引用的卡片都存在且屬於大綱指定的卡片
- 稿中出現的每個數字都能在該頁引用的卡片 `numbers` 中找到
- 頁數在 12–15 之間
- 每頁重點 3–5 個，每個重點不超過 40 個中文字

**G3 忠實度審查（faithfulness-reviewer subagent）**：
- 每次都開新的 subagent，只給 `drafts/`、`cards/`、對應 wiki 頁、`raw/text/`
- 逐頁判定：PASS／FAIL，FAIL 要標類型（講反、過度推論、無出處、數字錯、遺漏重要條件）與建議退回節點（N4 或 N2）
- 另檢查整體覆蓋率：brief 的每個問題都有被回答嗎？
- 報告存成 `review/round-1.md`、`round-2.md`…
- 只修報告列出的問題，其他頁不動

**N5 渲染**：
- 單一 HTML 檔、不依賴外部 CDN；16:9；鍵盤左右鍵翻頁；顯示頁碼
- 字體大小：內文不小於 24px（以 1280×720 為準）；不得為了塞字縮小字體
- 文字逐字取自通過 G3 的 drafts
- 可用 Playwright 截圖自己檢視版面（小 loop 最多 2 輪）

**G4 `check_render.py`（Playwright）**：
- 首次使用時安裝：`pip install playwright` 與 `python -m playwright install chromium`
- 以 1280×720 開啟 `slides/index.html`，逐頁檢查：
  - 每頁的內容容器 `scrollHeight <= clientHeight`、`scrollWidth <= clientWidth`（沒有溢出）
  - 頁數與 drafts 一致
  - 每頁可見文字與對應 draft 的文字一致（正規化空白後比對）
- 截圖存到 `topic/ai-era-coding/review/screens/`（可 commit）
- 溢出 → 標明是哪一頁，退回 N4 縮短該頁

**N6 交件 `report.md`**：
- 一張總表：每個節點／關卡的執行次數、通過或失敗、失敗原因、退回到哪裡
- 依時間記錄每次退回（含 commit hash）
- 統計：哪個節點失敗最多次
- 這份是作業「一次實際執行的結果或檢查紀錄」的主要依據

### 觸發方式
使用者輸入 `/topic-slides` 時，依 SKILL.md 從 N0 開始跑；若 `topic/ai-era-coding/` 已有部分產出，詢問使用者要從哪個節點重跑。

---

## 6. 階段 C：反思與 workflow 修正

1. 第一次完整跑完後，根據 `report.md` 整理：
   - 哪個節點最常出錯？
   - 錯誤的根源其實在哪一關？檢查能不能往前移？（例如：G3 常抓到數字錯 → 把數字比對提前到 N2 的 `check_cards.py`）
2. 把分析結果交給使用者討論【停下等使用者】。
3. 使用者決定修改後：更新 `SKILL.md` 與相關腳本，在 `process/workflow-changes.md` 記錄「改了什麼、為什麼、對應哪次失敗」，commit：`[workflow v2] 說明`。
4. 若時間允許，用 v2 再跑一次受影響的節點，並在 `report.md` 追加第二次的紀錄，比較前後差異。
5. 反思文字由使用者確認後才寫入 README。你可以先根據實際紀錄起草，但不得加入沒有發生過的事。

---

## 7. 階段 D：README、推上 GitHub、開 Pages

1. 寫 `README.md`（這是繳交總覽頁），包含：
   - LLM Wiki 主題與簡短介紹
   - Wiki 連結：`https://github.com/<帳號>/ai-coding-wiki/tree/main/wiki`
   - 簡報連結：`https://<帳號>.github.io/ai-coding-wiki/slides/`
   - loop / graph 流程圖：用 **Mermaid**（GitHub 會直接顯示），並附文字說明：
     - 哪些步驟會重複執行（各節點內的小 loop）
     - 哪些地方需要檢查或重新生成（G1、G3、G4、H1 與各退回路線）
     - 為什麼這樣設計（錯誤在離源頭最近的地方抓到；每關權限分開，方便定位錯誤；AI 審查用新 subagent，避免審自己的作品；剎車避免無限迴圈）
   - 一次實際執行的結果：摘要 `report.md`，並連結到完整檔案
   - 反思（第 6 節的結論）
   - 原始資料清單（連到 `raw/sources.md`）
2. 推上 GitHub 前檢查：`git status` 確認沒有任何 PDF 或 `raw/text/` 被加入。
3. `git push`。
4. 提醒使用者到 GitHub repo 的 Settings → Pages，Source 選 `main` branch、`/ (root)`，儲存後等待網址生效；確認 `slides/` 網址可以正常翻頁【停下等使用者】。
5. 最後給使用者一份繳交用的文字，標題格式：`中央 <學號> 資管三 陳少畇 AI時代的程式學習`（學號由使用者自行填入），內容依作業要求的 6 項逐項列出並附連結。

---

## 8. 繳交內容對照表（最後自我檢查）

| 作業要求 | 對應位置 |
|---|---|
| LLM Wiki 主題與簡短介紹 | README 開頭 |
| LLM Wiki 連結或成果 | `wiki/`（GitHub 連結） |
| 教學 HTML 簡報連結 | GitHub Pages `slides/` |
| loop / graph 流程圖或文字說明 | README（Mermaid＋說明）、`.claude/skills/topic-slides/SKILL.md` |
| 一次實際執行的結果或檢查紀錄 | `topic/ai-era-coding/report.md`、`review/`、git log |
| 反思 | README、`process/workflow-changes.md` |
| 「先討論、後生成」的證據 | `process/interview.md` |
| 至少 ingest 5 篇 | `wiki/log.md`（6 篇） |
