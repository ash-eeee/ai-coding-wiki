"""topic-slides 各檢查腳本共用：解析 brief、sources、卡片、大綱、逐頁稿。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, han_count, split_frontmatter  # noqa: E402,F401

TOPIC = ROOT / "topic" / "ai-era-coding"
SECTIONS = ["①", "②", "③", "④", "⑤", "⑥"]
TAG_RE = re.compile(r"\s*〔([^〕]*)〕\s*$")
NUM_RE = re.compile(r"(?<![A-Za-z\d.,])\d+(?:[.,]\d+)*(?![A-Za-z\d])")  # CS50、GPT4 這類名稱裡的數字不算


def parse_brief() -> tuple[dict[str, str], list[str]]:
    """回傳 ({段落符號: 問題}, [⑥ 子題])。"""
    text = (TOPIC / "brief.md").read_text(encoding="utf-8")
    sections: dict[str, str] = {}
    for line in text.splitlines():
        m = re.match(r"\|\s*([①-⑥])[^|]*\|\s*\d+\s*\|\s*([^|]*)\|", line)
        if m:
            sections[m.group(1)] = m.group(2).strip()
    subs: list[str] = []
    m = re.search(r"^### ⑥ 子題\s*\n((?:- .*\n?)+)", text, re.M)
    if m:
        subs = [l[2:].strip() for l in m.group(1).splitlines() if l.startswith("- ")]
    return sections, subs


def parse_sources() -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """回傳 ({段落: [wiki 路徑]}, {⑥ 子題: [wiki 路徑]})。"""
    text = (TOPIC / "sources.md").read_text(encoding="utf-8")
    sec: dict[str, list[str]] = {}
    sub: dict[str, list[str]] = {}
    cur_sec = cur_sub = None
    for line in text.splitlines():
        m2 = re.match(r"^###\s*⑥\s*(.+)$", line)
        m1 = re.match(r"^##\s*([①-⑥])", line)
        if m2:
            cur_sec, cur_sub = "⑥", m2.group(1).strip()
            sub.setdefault(cur_sub, [])
            continue
        if m1:
            cur_sec, cur_sub = m1.group(1), None
            sec.setdefault(cur_sec, [])
            continue
        m = re.match(r"^-\s*(wiki/[^\s]+\.md)", line)
        if m and cur_sec:
            sec.setdefault(cur_sec, []).append(m.group(1))
            if cur_sub:
                sub[cur_sub].append(m.group(1))
    return sec, sub


def parse_list_field(v: str) -> list[str]:
    v = v.strip()
    if not (v.startswith("[") and v.endswith("]")):
        return [v] if v else []
    return [x.strip().strip("\"'") for x in re.findall(r'"[^"]*"|\'[^\']*\'|[^,\[\]]+', v[1:-1]) if x.strip()]


def load_cards() -> dict[str, dict]:
    cards = {}
    for p in sorted((TOPIC / "cards").glob("C*.md")):
        fm, _ = split_frontmatter(p.read_text(encoding="utf-8"))
        fm["_file"] = p.name
        fm["numbers_list"] = parse_list_field(fm.get("numbers", "[]"))
        q = fm.get("quote", "").strip()
        if len(q) >= 2 and q[0] == q[-1] and q[0] in "\"'":
            q = q[1:-1]
        fm["quote_text"] = q
        fm["keep_list"] = parse_list_field(fm.get("keep", "[]"))
        cards[fm.get("id", p.stem)] = fm
    return cards


def parse_outline() -> dict[str, list[str]]:
    """回傳 {slide-03: [C03, C04]}。"""
    out: dict[str, list[str]] = {}
    cur = None
    for line in (TOPIC / "outline.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s*(slide-\d+)", line)
        if m:
            cur = m.group(1)
            out[cur] = []
            continue
        m = re.match(r"^-\s*卡片[:：]\s*(.*)$", line)
        if m and cur:
            out[cur] = re.findall(r"C\d+", m.group(1))
    return out


def parse_draft(p: Path) -> dict:
    title, bullets, source_line, cards = "", [], "", []
    bullet_cards: list[list[str]] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("# ") and not title:
            title = s[2:].strip()
        elif s.startswith("- "):
            b = s[2:].strip()
            m = TAG_RE.search(b)  # v2：每個重點結尾標 〔C01, C02〕
            bullet_cards.append(re.findall(r"C\d+", m.group(1)) if m else [])
            bullets.append(TAG_RE.sub("", b).strip())
        elif re.match(r"^出處[:：]", s):
            source_line = re.sub(r"^出處[:：]\s*", "", s)
        elif re.match(r"^卡片[:：]", s):
            cards = re.findall(r"C\d+", s)
    return {"title": title, "bullets": bullets, "bullet_cards": bullet_cards, "source": source_line, "cards": cards}


def draft_files() -> list[Path]:
    return sorted((TOPIC / "drafts").glob("slide-*.md"))


def number_tokens(s: str) -> set[str]:
    return {t.replace(",", "") for t in NUM_RE.findall(s)}
