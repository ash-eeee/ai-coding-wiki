---
name: topic-slides
description: 以本專案 wiki 為唯一知識來源，依 graph（N0→N6）產生教學型 HTML 簡報，每個節點內是有次數上限的小 loop，每關都有腳本或獨立 subagent 檢查。使用者輸入 /topic-slides 時觸發。
---

# topic-slides：從 Wiki 產生教學 HTML 簡報

> 版本：**v2**（2026-11-18）。v1 → v2 改了什麼、為什麼，見 `process/workflow-changes.md`。
> 一律使用台灣繁體中文與台灣用詞。

## 目標

用 `wiki/` 當**唯一知識來源**，產出一份給大學生的教學 HTML 簡報 `slides/index.html`，主題「AI 時代，程式該學到什麼程度？該怎麼學？」，每頁都能追溯到 wiki 頁與原始資料（Sx, p.y）。

## 限制

- 只能用 wiki 與 `raw/text/` 裡有的內容；**wiki 找不到的不准用模型自身知識補**，資料不足就停下回報。
- 每個節點只能看、只能改下表規定的東西。
- 簡報只放教學內容，不放製作流程（流程說明在 README）。
- 每過一個節點就 git commit：`[節點代號] 說明`。
- 檢查一律用 `scripts/` 的腳本實際執行；AI 審查一律開**新的** `faithfulness-reviewer` subagent，只給成品與來源，不給製作過程。

## 觸發方式

使用者輸入 `/topic-slides`：
- `topic/ai-era-coding/` 是空的 → 從 N0 開始。
- 已有部分產出 → 列出已完成的節點，詢問使用者要從哪個節點重跑。

## 狀態全部是檔案

```
topic/ai-era-coding/
├── brief.md          N0
├── sources.md        N1
├── cards/C01.md…     N2
├── outline.md        N3
├── drafts/slide-01.md…  N4
├── review/round-N.md  G3；review/coverage-N.txt、cards-N.txt、drafts-N.txt、render-N.txt 為腳本輸出
├── review/screens/   G4 截圖
└── report.md         N6
slides/index.html     N5
```

## Graph

```
B0 腳本自我測試［selftest.py］── 失敗 → 先修腳本，不准開始跑（v2 新增）
 ↓
N0 簡報規格 brief.md
 ↓
N1 檢索 wiki → sources.md
 ↓
G1 覆蓋率關卡［check_coverage.py］── 不足 → 停下回報（不硬湊）
 ↓
N2 證據卡 cards/*.md      ⟲ 寫卡 → check_cards.py → 修（最多 2 輪）
 ↓
N3 大綱 outline.md
 ↓
H1【使用者確認大綱】── 退回 → 修 N3；缺證據 → 回 N1
 ↓
N4 逐頁稿 drafts/slide-XX.md   ⟲ 寫 → check_drafts.py → 修（最多 2 輪）
 ↓
G3 忠實度審查［faithfulness-reviewer subagent］
     ── 某頁講反／過度推論 → 只退回那頁到 N4
     ── 證據卡本身錯 → 退回 N2 重抽那張卡
 ↓
N5 渲染 slides/index.html   ⟲ 產生 → 截圖 → 修版面（最多 2 輪）
 ↓
G4 渲染檢查［check_render.py］── 溢出 → 退回 N4 縮短該頁（不准縮小字體）
 ↓
N6 交件 report.md
```

**全域剎車**：同一個關卡累計退回 3 次仍未通過，停下交給使用者判斷。
**小 loop 上限**：節點內修正最多 2 輪；第 2 輪仍失敗 → 停下回報。

## 每個節點能看什麼、能改什麼

| 節點 | 能看 | 產出 | 不能做 |
|---|---|---|---|
| N0 規格 | 本檔「簡報規格」 | `brief.md` | 加入規格外的段落 |
| N1 檢索 | `wiki/`（從 `index.md` 開始） | `sources.md` | 讀 `raw/`、上網 |
| G1 | `brief.md`、`sources.md`、`wiki/` | `review/coverage-N.txt` | 修改任何產出 |
| N2 證據卡 | `sources.md` 列出的 wiki 頁、`raw/text/` | `cards/C01.md`… | 混用其他來源、用模型自身知識 |
| N3 大綱 | `brief.md`、`cards/` | `outline.md` | 新增沒有卡片支撐的論點 |
| H1 | `outline.md` | 使用者決定 | — |
| N4 逐頁稿 | `outline.md`＋該頁指定的卡片 | `drafts/slide-XX.md` | 引用指定卡片以外的內容 |
| G3 | `drafts/`、`cards/`、對應 wiki 頁、`raw/text/` | `review/round-N.md` | 修改成品；看到製作過程 |
| N5 渲染 | 已通過 G3 的 `drafts/` | `slides/index.html` | 改任何一個字 |
| G4 | `slides/index.html`、`drafts/` | `review/render-N.txt`、`review/screens/` | 修改成品 |
| N6 交件 | 所有 review 輸出、git log | `report.md` | 寫沒發生過的事 |

## 簡報規格（N0 寫進 brief.md）

- 語言：台灣繁體中文
- 聽眾：有一點資訊背景、看得懂程式但不會自己實際應用的大學生
- 簡單、有邏輯架構；每頁 3–5 個重點，句子短
- 頁數 13 頁左右（容許 12–15）
- 每頁底部標出處（wiki 頁名＋原始資料代號）
- 只放教學內容

| 段落 | 頁數 | 要回答的問題 | 主要來源 |
|---|---|---|---|
| 封面＋開場問題 | 1 | — | — |
| ① 為什麼還要學 | 1 | AI 會寫程式了，學程式還有意義嗎？ | S4 |
| ② AI 真的讓人變快嗎 | 1 | 感覺變快＝實際變快嗎？ | S1 |
| ③ 用 AI 學得會嗎 | 1 | 初學者用 AI 會學得更好還是更差？ | S3、S2 |
| ④ 差別在怎麼用 | 2 | 哪些用法有學到、哪些沒有？ | S2、S6 |
| ⑤ 學校怎麼教 | 1 | AI 當助教、不當槍手是什麼意思？ | S5 |
| ⑥ 該學到哪、怎麼學 | 5 | 必備能力、學習階段、具體練習方法、用 AI 的守則、自我檢查清單 | S2、S3、S5、S6 |
| 總結 | 1 | 一句話帶走什麼？ | — |

## 各節點細節與檔案格式

### N0 `brief.md`
段落表格必須是上方格式（`| 段落 | 頁數 | 要回答的問題 | 主要來源 |`），⑥ 另列 `### ⑥ 子題` 清單（每行 `- 必備能力` 等），供 G1 解析。

### N1 `sources.md`
```
## ① 為什麼還要學
- wiki/topics/why-learn.md — 一句說明為什麼相關
```
⑥ 的每個子題用 `### ⑥ 必備能力` 等子標題各自列頁面。封面與總結不用列。

### G1 `check_coverage.py`
- 每段（封面、總結除外）至少 2 個 wiki 頁；列出的頁面都存在；⑥ 每個子題至少 1 頁。
- 不足 → 輸出缺口清單、exit 1、停下回報。

### N2 證據卡 `cards/Cxx.md`（一張卡＝一個論點）
```
---
id: C07
section: ④
claim: （中文，一句話的論點）
numbers: ["50%", "67%"]
wiki: wiki/xxx.md
source: S2
page: 5
scope: （v2 必填）對象、情境、是否顯著、作者保留語氣，例如「10–17 歲新手；探索性分析」
keep: ["可能", "未實測"]   # v2 選填：稿子引用此卡時，同一頁至少要出現其中一個詞
quote: "（英文原文短句，25 個英文字以內，必須逐字出現在原文）"
---
```
寫卡時就把「會被濃縮掉的條件」寫進 `scope`，並把一定要留在投影片上的條件詞放進 `keep`。
`check_cards.py`：必填欄位、wiki 頁存在、source 在 `raw/sources.md`、quote ≤ 25 字且能在 `raw/text/` 該頁找到（正規化空白、換行、連字號斷字）、numbers 每個都出現在 quote 或原文該頁。

### N3 `outline.md`
每頁一節：
```
## slide-03 ② 感覺變快＝實際變快嗎？
- 目標：一句話教學目標
- 卡片：C03, C04
```

### H1
把大綱交給使用者確認；退回 → 修 N3；缺證據 → 回 N1。

### N4 `drafts/slide-XX.md`
```
# 標題
- 重點 1 〔C03〕
- 重點 2 〔C03, C04〕
- 問句形式的重點可以不標？
出處：wiki 頁名｜S1 p.1；wiki 頁名｜S1 p.12
卡片：C03, C04
```
`check_drafts.py`（v2）：每頁有出處列；卡片存在且屬於大綱指定；頁數 12–15；每頁重點 3–5 個、每個 ≤ 40 個中文字。v2 新增：
- 每個重點結尾標 〔Cxx〕（問句除外），數字**逐點**比對該重點標的卡片
- 卡片有 `keep` 時，同頁引用它的重點至少要出現一個 keep 詞（防止丟掉條件）
- 不得出現絕對化用語（才能、才用、一定、絕對、保證、證明了…）
- 總結頁的卡片必須在前面頁出現過（總結不得有新論點）
封面與總結頁也照此格式。`build_slides.py` 會去掉 〔Cxx〕 標籤再渲染。

### G3 忠實度審查
- 每輪開**新的** `faithfulness-reviewer` subagent，只給 drafts/、cards/、對應 wiki 頁、raw/text/ 的路徑。
- 逐頁 PASS／FAIL；FAIL 標類型（講反、過度推論、無出處、數字錯、遺漏重要條件）與建議退回節點（N4 或 N2）；另檢查 brief 每個問題是否有被回答。
- 報告存 `review/round-N.md`。只修報告列出的問題，其他頁不動。

### N5 渲染 `slides/index.html`
- 單一 HTML、不依賴外部 CDN；16:9；左右鍵翻頁；顯示頁碼。
- 內文 ≥ 24px（以 1280×720 為準）；不得為了塞字縮小字體。
- 文字**逐字**取自通過 G3 的 drafts：用 `scripts/build_slides.py` 從 drafts 產生，不手打。
- 可用 Playwright 截圖自己檢視（小 loop 最多 2 輪）。

### G4 `check_render.py`（Playwright，1280×720）
- 每頁內容容器 `scrollHeight <= clientHeight`、`scrollWidth <= clientWidth`
- 頁數與 drafts 一致；每頁可見文字與 draft 一致（正規化空白）
- 內文字體 ≥ 24px
- 截圖存 `review/screens/`；溢出 → 標明頁碼，退回 N4 縮短

### N6 `report.md`
- 總表：每個節點／關卡的執行次數、通過或失敗、失敗原因、退回到哪裡
- 依時間記錄每次退回（含 commit hash）
- 統計：哪個節點失敗最多次
- 只寫實際發生的事

## B0 自我測試（v2 新增）

每次開始跑 graph 前先執行 `python3 scripts/selftest.py`：用已知正反例測試正規化、引文比對、數字擷取、絕對化用語、卡片標籤解析。失敗代表檢查腳本本身有 bug，先修腳本。

## 完成標準

G1、check_cards、check_drafts、G3、G4 全部通過，`report.md` 寫完並 commit。

## 停止條件

- G1 不通過（資料不足）
- 任一小 loop 第 2 輪仍失敗
- 同一關卡累計退回 3 次
- H1 等使用者確認
