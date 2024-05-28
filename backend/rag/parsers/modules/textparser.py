from typing import Optional, List

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from backend.rag.parsers.parser import BaseParser
from backend.rag.parsers.utils import contains_text


class TextParser(BaseParser):
    """
    Парсер для работы с простыми текстовыми файлами
    """

    supported_file_extensions = [".txt"]

    def __init__(self, max_chunk_size: int = 1000, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_chunk_size = max_chunk_size

    async def get_chunks(self,
                         filepath: str,
                         metadata: Optional[dict],
                         *args, **kwargs) -> List[Document]:
        """
        Асинхронно извлекает текст из текстовых файлов и возвращает его в chunk'ах.
        """
        content = None
        with open(filepath, "r") as f:
            content = f.read()
        if not content:
            print("Error reading file: " + filepath)
            return []
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.max_chunk_size)
        texts = text_splitter.split_text(content)

        docs = [
            Document(
                page_content=text,
                metadata={
                    "type": "text",
                },
            )
            for text in texts
            if contains_text(text)
        ]

        return docs
