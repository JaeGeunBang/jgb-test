import os
from pathlib import Path

from rag_chatbot.exceptions import UnsupportedFormatError

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}


class DocumentLoader:
    def load(self, file_path: str) -> str:
        """
        지원 형식: .txt, .md, .pdf
        오류 시: FileNotFoundError, UnsupportedFormatError 발생
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

        ext = path.suffix.lower()

        if ext not in SUPPORTED_EXTENSIONS:
            raise UnsupportedFormatError(f"지원하지 않는 파일 형식입니다: {ext}")

        if ext in {".txt", ".md"}:
            return path.read_text(encoding="utf-8")

        # PDF
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
