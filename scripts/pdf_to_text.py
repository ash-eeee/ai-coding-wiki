"""把 raw/*.pdf 轉成 raw/text/<同檔名>.txt。

使用 pypdf 一般（plain）模式擷取，每頁之間插入換頁符號 \f，讓後續腳本能依頁碼比對。

為什麼不用 HOMEWORK_GUIDE 建議的 `pdftotext -layout`：
1. 本機一開始沒有 pdftotext（Homebrew 安裝中）。
2. layout 模式保留版面，雙欄論文（S3、S5、S6）的左右欄會在同一行交錯，
   跨行的英文引用句就無法逐字比對；plain 模式依閱讀順序輸出，比對較可靠。
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
OUT = RAW / "text"


def convert_pypdf(pdf: Path, txt: Path) -> int:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf))
    pages = [(p.extract_text() or "") for p in reader.pages]
    txt.write_text("\f".join(pages), encoding="utf-8")
    return len(pages)


def main() -> int:
    OUT.mkdir(exist_ok=True)
    print("轉換工具：pypdf（plain 模式）")
    for pdf in sorted(RAW.glob("*.pdf")):
        txt = OUT / (pdf.stem + ".txt")
        n = convert_pypdf(pdf, txt)
        print(f"{pdf.name} → text/{txt.name}（{n} 頁）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
