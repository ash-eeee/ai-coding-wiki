"""各檢查腳本共用的工具：讀來源清單、讀原文分頁、正規化文字、解析 frontmatter。"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
WIKI = ROOT / "wiki"

CITE_RE = re.compile(r"\((S\d+,\s*p\.\s*[\d–\-]+(?:\s*;\s*S\d+,\s*p\.\s*[\d–\-]+)*)\)")
ONE_CITE_RE = re.compile(r"(S\d+),\s*p\.\s*(\d+)(?:\s*[–\-]\s*(\d+))?")
QUOTE_RE = re.compile(r'"([^"\n]*[A-Za-z][^"\n]*)"')


def load_sources() -> dict[str, Path]:
    """從 raw/sources.md 的表格讀出 {代號: raw/text/<檔名>.txt}。"""
    out: dict[str, Path] = {}
    for line in (RAW / "sources.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*(S\d+)\s*\|.*`([^`]+\.pdf)`\s*\|\s*$", line)
        if m:
            out[m.group(1)] = RAW / "text" / (Path(m.group(2)).stem + ".txt")
    return out


_page_cache: dict[Path, list[str]] = {}


def load_pages(txt: Path) -> list[str]:
    """回傳各頁文字（index 0 = 第 1 頁）。"""
    if txt not in _page_cache:
        _page_cache[txt] = txt.read_text(encoding="utf-8").split("\f")
    return _page_cache[txt]


def normalize(s: str, keep_line_hyphen: bool = False) -> str:
    """正規化：連字號斷行接回、連字（ﬁ）展開、彎引號轉直引號、去除所有空白、小寫。

    去除所有空白是因為 PDF 擷取常把字黏在一起或多插空白；字元順序仍須完全一致。
    keep_line_hyphen=True 時保留行尾連字號（用於本來就有連字號的複合字，例如 mini-task 剛好斷在行尾）。
    """
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("−", "-")
    if not keep_line_hyphen:
        s = re.sub(r"-\s*\n\s*", "", s)  # 行尾連字號斷字
    s = re.sub(r"\s+", "", s)
    return s.lower()


def parse_cites(text: str) -> list[tuple[str, int, int]]:
    """從文字中取出所有 (代號, 起頁, 迄頁)。"""
    out = []
    for group in CITE_RE.findall(text):
        for code, a, b in ONE_CITE_RE.findall(group):
            out.append((code, int(a), int(b) if b else int(a)))
    return out


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """簡易 YAML frontmatter 解析（只支援 key: value 一行一個）。"""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    fm: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.split("#", 1)[0].strip() if not v.strip().startswith(('"', "'")) else v.strip()
    return fm, text[end + 4 :].lstrip("\n")


def parse_list(v: str) -> list[str]:
    v = v.strip()
    if v.startswith("[") and v.endswith("]"):
        return [x.strip().strip("\"'") for x in v[1:-1].split(",") if x.strip()]
    return [v] if v else []


def han_count(s: str) -> int:
    return len(re.findall(r"[一-鿿]", s))


def find_quote(quote: str, pages: list[str], page_range: range | None = None) -> int | None:
    """在指定頁（1 起算）中找引文，找到回傳頁碼，找不到回傳 None。"""
    q = normalize(quote)
    idxs = page_range if page_range is not None else range(1, len(pages) + 1)
    for p in idxs:
        if 1 <= p <= len(pages):
            t = pages[p - 1]
            if q in normalize(t) or q in normalize(t, keep_line_hyphen=True):
                return p
    return None
