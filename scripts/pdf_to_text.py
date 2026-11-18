"""把 raw/*.pdf 轉成 raw/text/<同檔名>.txt。

優先使用 pdftotext -layout；若系統沒有 pdftotext，改用 pypdf。
每頁之間插入換頁符號 \f，讓後續腳本能依頁碼比對（與 pdftotext 行為一致）。
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
OUT = RAW / "text"


def convert_pypdf(pdf: Path, txt: Path) -> int:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf))
    pages = [(p.extract_text(extraction_mode="layout") or "") for p in reader.pages]
    txt.write_text("\f".join(pages), encoding="utf-8")
    return len(pages)


def main() -> int:
    OUT.mkdir(exist_ok=True)
    use_pdftotext = shutil.which("pdftotext") is not None
    print(f"轉換工具：{'pdftotext -layout' if use_pdftotext else 'pypdf (layout 模式)'}")
    for pdf in sorted(RAW.glob("*.pdf")):
        txt = OUT / (pdf.stem + ".txt")
        if use_pdftotext:
            subprocess.run(["pdftotext", "-layout", str(pdf), str(txt)], check=True)
            n = txt.read_text(encoding="utf-8").count("\f")
        else:
            n = convert_pypdf(pdf, txt)
        print(f"{pdf.name} → text/{txt.name}（{n} 頁）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
