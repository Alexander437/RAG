import re
from typing import Optional, List

import fitz
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from backend.constants import TEXT_SEPARATORS, STRS_TO_DELETE
from backend.logger import logger
from backend.rag.parsers.parser import BaseParser
from backend.rag.parsers.utils import contains_text


class PdfParserUsingPyMuPDF(BaseParser):
    """
    PdfParserUsingPyMuPDF парсер для извлечения текста из PDF файлов, используя библиотеку PyMuPDF.
    """

    supported_file_extensions = [".pdf"]

    def __init__(self, max_chunk_size: int = 1000, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_chunk_size = max_chunk_size

    async def get_chunks(self,
                         filepath: str,
                         metadata: Optional[dict],
                         *args, **kwargs) -> List[Document]:
        """
        Асинхронное извлечение текста из PDF файла и возвращение его в chunk'ах.
        """
        final_texts = []
        final_tables = []
        try:
            # Open the PDF file using pdfplumber
            doc = fitz.open(filepath)
            for page in doc:
                table = page.find_tables()
                table = list(table)
                for ix, tab in enumerate(table):
                    tab = tab.extract()
                    tab = list(map(lambda x: [str(t) for t in x], tab))
                    tab = list(map("||".join, tab))
                    tab = "\n".join(tab)
                    tab = [
                        Document(
                            page_content=tab,
                            metadata={
                                "page_num": page.number,
                                "type": "table",
                                "table_num": ix,
                            },
                        )
                    ]
                    final_tables.extend(tab)

                text = page.get_text()
                for str_to_delete in STRS_TO_DELETE:
                    text = text.replace(str_to_delete, "")
                # Create a Document object per page with page-specific metadata
                if len(text) > self.max_chunk_size:
                    # Split the text into chunks of size less than or equal to max_chunk_size
                    text_splitter = RecursiveCharacterTextSplitter(
                        separators=TEXT_SEPARATORS,
                        chunk_size=self.max_chunk_size,
                        chunk_overlap=0
                    )
                    text_splits = text_splitter.split_text(text)
                    texts = [
                        Document(
                            page_content=self.clear_text(text_split),
                            metadata={
                                "page_num": page.number,
                                "type": "text",
                            },
                        )
                        for text_split in text_splits
                        if contains_text(text_split)
                    ]
                    final_texts.extend(texts)
                else:
                    if contains_text(text):
                        final_texts.append(
                            Document(
                                page_content=self.clear_text(text),
                                metadata={
                                    "page_num": page.number,
                                    "type": "text",
                                },
                            )
                        )
        except Exception:
            logger.error(f"Error while parsing PDF file at {filepath}")
            # Return an empty list if there was an error during processing
            return []

        return final_texts + final_tables

    @staticmethod
    def clear_text(text: str) -> str:
        # clean up text for any problematic characters
        text = re.sub("\n", " ", text).strip()
        text = re.sub(r"([^\w\s])\1{4,}", " ", text)
        text = re.sub(" +", " ", text).strip()
        return text
