"""
Используются для разбиения файла на chunk'и
! Для кириллицы убрать строку `text = text.encode("ascii", errors="ignore").decode("ascii")`

API:
```python
import asyncio
from backend.modules.parsers.parser import get_parser_for_extension

parser = get_parser_for_extension(".pdf", parsers_map=dict())
# Или parser = get_parser_for_extension(".pdf", parsers_map={".pdf": "PdfParserFast"})
res = parser.get_chunks("tests/data_example/Постановление Правительства РФ от 16.03.2009 N 228.pdf", metadata=dict())
doc = asyncio.run(res)
```
"""
from backend.modules.parsers.codeparser import CodeParser
from backend.modules.parsers.markdownparser import MarkdownParser
from backend.modules.parsers.parser import register_parser
from backend.modules.parsers.pdfparser_fast import PdfParserUsingPyMuPDF
from backend.modules.parsers.tablepdfparser import PdfTableParser
from backend.modules.parsers.textparser import TextParser

# The order of registry defines the order of precedence
register_parser("MarkdownParser", MarkdownParser)
register_parser("TextParser", TextParser)
register_parser("PdfParserFast", PdfParserUsingPyMuPDF)
register_parser("PdfTableParser", PdfTableParser)
register_parser("CodeParser", CodeParser)
