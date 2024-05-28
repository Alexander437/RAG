"""
Используются для разбиения файла на chunk'и
! Для кириллицы убрать строку `text = text.encode("ascii", errors="ignore").decode("ascii")`

API:
```python
import asyncio
from backend.rag.parsers.parser import get_parser_for_extension

parser = get_parser_for_extension(".pdf", parsers_map=dict())
# Или parser = get_parser_for_extension(".pdf", parsers_map={".pdf": "PdfParserFast"})
res = parser.get_chunks("data/Постановление Правительства РФ от 16.03.2009 N 228.pdf", metadata=dict())
doc = asyncio.run(res)
```
"""
from backend.rag.parsers.parser import register_parser
from backend.rag.parsers.modules.codeparser import CodeParser
from backend.rag.parsers.modules.textparser import TextParser
from backend.rag.parsers.modules.markdownparser import MarkdownParser
from backend.rag.parsers.modules.tablepdfparser import PdfTableParser
from backend.rag.parsers.modules.pdfparser_fast import PdfParserUsingPyMuPDF

# The order of registry defines the order of precedence
register_parser("MarkdownParser", MarkdownParser)
register_parser("TextParser", TextParser)
register_parser("PdfParserFast", PdfParserUsingPyMuPDF)
register_parser("PdfTableParser", PdfTableParser)
register_parser("CodeParser", CodeParser)
