import os
import uuid
from typing import ClassVar

from app.schemas.rag import Document


class DocumentLoader:
    """Loads documents from files, directories, and raw text."""

    SUPPORTED_EXTENSIONS: ClassVar[set[str]] = {".txt", ".md", ".pdf", ".docx", ".html"}

    def load_text(self, text: str, metadata: dict | None = None) -> Document:
        """Load a document from raw text."""
        return Document(
            content=text,
            metadata=metadata or {},
            doc_id=str(uuid.uuid4()),
        )

    def load_file(self, file_path: str, metadata: dict | None = None) -> Document:
        """Load a single file as a document.

        TODO: Implement real file parsing for PDF, DOCX, HTML, etc.
        Currently only supports plain text files.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {ext}")

        # TODO: Add proper parsers per file type
        # - PDF: use PyPDF2 or pdfplumber
        # - DOCX: use python-docx
        # - HTML: use BeautifulSoup
        if ext in {".pdf", ".docx", ".html"}:
            raise NotImplementedError(
                f"Parsing for {ext} files not yet implemented. "
                "Integrate PyPDF2, python-docx, or BeautifulSoup."
            )

        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        meta = {**(metadata or {}), "source": file_path, "file_type": ext}
        return Document(content=content, metadata=meta, doc_id=str(uuid.uuid4()))

    def load_directory(
        self, directory_path: str, metadata: dict | None = None
    ) -> list[Document]:
        """Load all supported files from a directory.

        TODO: Add recursive option, glob patterns, file filtering.
        """
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Not a directory: {directory_path}")

        documents = []
        for root, _dirs, files in os.walk(directory_path):
            for file in sorted(files):
                ext = os.path.splitext(file)[1].lower()
                if ext in self.SUPPORTED_EXTENSIONS:
                    file_path = os.path.join(root, file)
                    try:
                        doc = self.load_file(file_path, metadata)
                        documents.append(doc)
                    except (NotImplementedError, ValueError):
                        continue  # Skip unsupported types silently
        return documents
