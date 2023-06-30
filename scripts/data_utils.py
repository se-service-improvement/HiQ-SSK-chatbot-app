"""Data utilities for index preparation."""
import ast
import html
import json
import os
import re
from abc import ABC, abstractmethod
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from functools import partial
from typing import List, Dict, Optional, Generator, Tuple

import markdown
import tiktoken
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from bs4 import BeautifulSoup
from langchain.text_splitter import MarkdownTextSplitter, RecursiveCharacterTextSplitter, PythonCodeTextSplitter
from tqdm import tqdm

FILE_FORMAT_DICT = {
***REMOVED***"md": "markdown",
***REMOVED***"txt": "text",
***REMOVED***"html": "html",
***REMOVED***"shtml": "html",
***REMOVED***"htm": "html",
***REMOVED***"py": "python",
***REMOVED***"pdf": "pdf"
***REMOVED***

SENTENCE_ENDINGS = [".", "!", "?"]
WORDS_BREAKS = list(reversed([",", ";", ":", " ", "(", ")", "[", "]", "{", "}", "\t", "\n"]))

PDF_HEADERS = {
***REMOVED***"title": "h1",
***REMOVED***"sectionHeading": "h2"
}

@dataclass
class Document(object):
***REMOVED***"""A data class for storing documents

***REMOVED***Attributes:
***REMOVED***content (str): The content of the document.
***REMOVED***id (Optional[str]): The id of the document.
***REMOVED***title (Optional[str]): The title of the document.
***REMOVED***filepath (Optional[str]): The filepath of the document.
***REMOVED***url (Optional[str]): The url of the document.
***REMOVED***metadata (Optional[Dict]): The metadata of the document.***REMOVED***
***REMOVED***"""

***REMOVED***content: str
***REMOVED***id: Optional[str] = None
***REMOVED***title: Optional[str] = None
***REMOVED***filepath: Optional[str] = None
***REMOVED***url: Optional[str] = None
***REMOVED***metadata: Optional[Dict] = None

def cleanup_content(content: str) -> str:
***REMOVED***"""Cleans up the given content using regexes
***REMOVED***Args:
***REMOVED***content (str): The content to clean up.
***REMOVED***Returns:
***REMOVED***str: The cleaned up content.
***REMOVED***"""
***REMOVED***output = re.sub(r"\n{2,}", "\n", content)
***REMOVED***output = re.sub(r"[^\S\n]{2,}", " ", output)
***REMOVED***output = re.sub(r"-{2,}", "--", output)

***REMOVED***return output.strip()

class BaseParser(ABC):
***REMOVED***"""A parser parses content to produce a document."""

***REMOVED***@abstractmethod
***REMOVED***def parse(self, content: str, file_name: Optional[str] = None) -> Document:
***REMOVED***"""Parses the given content.
***REMOVED***Args:
***REMOVED******REMOVED***content (str): The content to parse.
***REMOVED******REMOVED***file_name (str): The file name associated with the content.
***REMOVED***Returns:
***REMOVED******REMOVED***Document: The parsed document.
***REMOVED***"""
***REMOVED***pass

***REMOVED***def parse_file(self, file_path: str) -> Document:
***REMOVED***"""Parses the given file.
***REMOVED***Args:
***REMOVED******REMOVED***file_path (str): The file to parse.
***REMOVED***Returns:
***REMOVED******REMOVED***Document: The parsed document.
***REMOVED***"""
***REMOVED***with open(file_path, "r") as f:
***REMOVED******REMOVED***return self.parse(f.read(), os.path.basename(file_path))

***REMOVED***def parse_directory(self, directory_path: str) -> List[Document]:
***REMOVED***"""Parses the given directory.
***REMOVED***Args:
***REMOVED******REMOVED***directory_path (str): The directory to parse.
***REMOVED***Returns:
***REMOVED******REMOVED***List[Document]: List of parsed documents.
***REMOVED***"""
***REMOVED***documents = []
***REMOVED***for file_name in os.listdir(directory_path):
***REMOVED******REMOVED***file_path = os.path.join(directory_path, file_name)
***REMOVED******REMOVED***if os.path.isfile(file_path):
***REMOVED******REMOVED***documents.append(self.parse_file(file_path))
***REMOVED***return documents

class MarkdownParser(BaseParser):
***REMOVED***"""Parses Markdown content."""

***REMOVED***def __init__(self) -> None:
***REMOVED***super().__init__()
***REMOVED***self._html_parser = HTMLParser()

***REMOVED***def parse(self, content: str, file_name: Optional[str] = None) -> Document:
***REMOVED***"""Parses the given content.
***REMOVED***Args:
***REMOVED******REMOVED***content (str): The content to parse.
***REMOVED******REMOVED***file_name (str): The file name associated with the content.
***REMOVED***Returns:
***REMOVED******REMOVED***Document: The parsed document.
***REMOVED***"""
***REMOVED***html_content = markdown.markdown(content, extensions=['fenced_code', 'toc', 'tables', 'sane_lists'])

***REMOVED***return self._html_parser.parse(html_content, file_name)


class HTMLParser(BaseParser):
***REMOVED***"""Parses HTML content."""
***REMOVED***TITLE_MAX_TOKENS = 128
***REMOVED***NEWLINE_TEMPL = "<NEWLINE_TEXT>"

***REMOVED***def __init__(self) -> None:
***REMOVED***super().__init__()
***REMOVED***self.token_estimator = TokenEstimator()

***REMOVED***def parse(self, content: str, file_name: Optional[str] = None) -> Document:
***REMOVED***"""Parses the given content.
***REMOVED***Args:
***REMOVED******REMOVED***content (str): The content to parse.
***REMOVED******REMOVED***file_name (str): The file name associated with the content.
***REMOVED***Returns:
***REMOVED******REMOVED***Document: The parsed document.
***REMOVED***"""
***REMOVED***soup = BeautifulSoup(content, 'html.parser')

***REMOVED***# Extract the title
***REMOVED***title = ''
***REMOVED***if soup.title and soup.title.string:
***REMOVED******REMOVED***title = soup.title.string
***REMOVED***else:
***REMOVED******REMOVED***# Try to find the first <h1> tag
***REMOVED******REMOVED***h1_tag = soup.find('h1')
***REMOVED******REMOVED***if h1_tag:
***REMOVED******REMOVED***title = h1_tag.get_text(strip=True)
***REMOVED******REMOVED***else:
***REMOVED******REMOVED***h2_tag = soup.find('h2')
***REMOVED******REMOVED***if h2_tag:
***REMOVED******REMOVED******REMOVED***title = h2_tag.get_text(strip=True)
***REMOVED***if title is None or title == '':
***REMOVED******REMOVED***# if title is still not found, guess using the next string
***REMOVED******REMOVED***try:
***REMOVED******REMOVED***title = next(soup.stripped_strings)
***REMOVED******REMOVED***title = self.token_estimator.construct_tokens_with_size(title, self.TITLE_MAX_TOKENS)

***REMOVED******REMOVED***except StopIteration:
***REMOVED******REMOVED***title = file_name

***REMOVED******REMOVED***# Helper function to process text nodes

***REMOVED***# Parse the content as it is without any formatting changes
***REMOVED***result = content
***REMOVED***if title is None:
***REMOVED******REMOVED***title = '' # ensure no 'None' type title

***REMOVED***return Document(content=cleanup_content(result), title=str(title))

class TextParser(BaseParser):
***REMOVED***"""Parses text content."""

***REMOVED***def __init__(self) -> None:
***REMOVED***super().__init__()

***REMOVED***def _get_first_alphanum_line(self, content: str) -> Optional[str]:
***REMOVED***title = None
***REMOVED***for line in content.splitlines():
***REMOVED******REMOVED***if any([c.isalnum() for c in line]):
***REMOVED******REMOVED***title = line.strip()
***REMOVED******REMOVED***break
***REMOVED***return title

***REMOVED***def _get_first_line_with_property(
***REMOVED***self, content: str, property: str = "title: "
***REMOVED***) -> Optional[str]:
***REMOVED***title = None
***REMOVED***for line in content.splitlines():
***REMOVED******REMOVED***if line.startswith(property):
***REMOVED******REMOVED***title = line[len(property) :].strip()
***REMOVED******REMOVED***break
***REMOVED***return title

***REMOVED***def parse(self, content: str, file_name: Optional[str] = None) -> Document:
***REMOVED***"""Parses the given content.
***REMOVED***Args:
***REMOVED******REMOVED***content (str): The content to parse.
***REMOVED******REMOVED***file_name (str): The file name associated with the content.
***REMOVED***Returns:
***REMOVED******REMOVED***Document: The parsed document.
***REMOVED***"""
***REMOVED***title = self._get_first_line_with_property(
***REMOVED******REMOVED***content
***REMOVED***) or self._get_first_alphanum_line(content)

***REMOVED***return Document(content=cleanup_content(content), title=title or file_name)


class PythonParser(BaseParser):
***REMOVED***def _get_topdocstring(self, text):
***REMOVED***tree = ast.parse(text)
***REMOVED***docstring = ast.get_docstring(tree)  # returns top docstring
***REMOVED***return docstring

***REMOVED***def parse(self, content: str, file_name: Optional[str] = None) -> Document:
***REMOVED***"""Parses the given content.
***REMOVED***Args:
***REMOVED******REMOVED***content (str): The content to parse.
***REMOVED******REMOVED***file_name (str): The file name associated with the content.
***REMOVED***Returns:
***REMOVED******REMOVED***Document: The parsed document.
***REMOVED***"""
***REMOVED***docstring = self._get_topdocstring(content)
***REMOVED***if docstring:
***REMOVED******REMOVED***title = f"{file_name}: {docstring}"
***REMOVED***else:
***REMOVED******REMOVED***title = file_name
***REMOVED***return Document(content=content, title=title)

***REMOVED***def __init__(self) -> None:
***REMOVED***super().__init__()

class ParserFactory:
***REMOVED***def __init__(self):
***REMOVED***self._parsers = {
***REMOVED******REMOVED***"html": HTMLParser(),
***REMOVED******REMOVED***"text": TextParser(),
***REMOVED******REMOVED***"markdown": MarkdownParser(),
***REMOVED******REMOVED***"python": PythonParser()
***REMOVED***

***REMOVED***@property
***REMOVED***def supported_formats(self) -> List[str]:
***REMOVED***"Returns a list of supported formats"
***REMOVED***return list(self._parsers.keys())

***REMOVED***def __call__(self, file_format: str) -> BaseParser:
***REMOVED***parser = self._parsers.get(file_format, None)
***REMOVED***if parser is None:
***REMOVED******REMOVED***raise UnsupportedFormatError(f"{file_format} is not supported")

***REMOVED***return parser

class TokenEstimator(object):
***REMOVED***GPT2_TOKENIZER = tiktoken.get_encoding("gpt2")

***REMOVED***def estimate_tokens(self, text: str) -> int:
***REMOVED***return len(self.GPT2_TOKENIZER.encode(text))

***REMOVED***def construct_tokens_with_size(self, tokens: str, numofTokens: int) -> str:
***REMOVED***newTokens = self.GPT2_TOKENIZER.decode(
***REMOVED******REMOVED***self.GPT2_TOKENIZER.encode(tokens)[:numofTokens]
***REMOVED***)
***REMOVED***return newTokens

parser_factory = ParserFactory()
TOKEN_ESTIMATOR = TokenEstimator()

class UnsupportedFormatError(Exception):
***REMOVED***"""Exception raised when a format is not supported by a parser."""

***REMOVED***pass

@dataclass
class ChunkingResult:
***REMOVED***"""Data model for chunking result

***REMOVED***Attributes:
***REMOVED***chunks (List[Document]): List of chunks.
***REMOVED***total_files (int): Total number of files.
***REMOVED***num_unsupported_format_files (int): Number of files with unsupported format.
***REMOVED***num_files_with_errors (int): Number of files with errors.
***REMOVED***skipped_chunks (int): Number of chunks skipped.
***REMOVED***"""
***REMOVED***chunks: List[Document]
***REMOVED***total_files: int
***REMOVED***num_unsupported_format_files: int = 0
***REMOVED***num_files_with_errors: int = 0
***REMOVED***# some chunks might be skipped to small number of tokens
***REMOVED***skipped_chunks: int = 0

def get_files_recursively(directory_path: str) -> List[str]:
***REMOVED***"""Gets all files in the given directory recursively.
***REMOVED***Args:
***REMOVED***directory_path (str): The directory to get files from.
***REMOVED***Returns:
***REMOVED***List[str]: List of file paths.
***REMOVED***"""
***REMOVED***file_paths = []
***REMOVED***for dirpath, _, files in os.walk(directory_path):
***REMOVED***for file_name in files:
***REMOVED******REMOVED***file_path = os.path.join(dirpath, file_name)
***REMOVED******REMOVED***file_paths.append(file_path)
***REMOVED***return file_paths

def convert_escaped_to_posix(escaped_path):
***REMOVED***windows_path = escaped_path.replace("\\\\", "\\")
***REMOVED***posix_path = windows_path.replace("\\", "/")
***REMOVED***return posix_path

def _get_file_format(file_name: str, extensions_to_process: List[str]) -> Optional[str]:
***REMOVED***"""Gets the file format from the file name.
***REMOVED***Returns None if the file format is not supported.
***REMOVED***Args:
***REMOVED***file_name (str): The file name.
***REMOVED***extensions_to_process (List[str]): List of extensions to process.
***REMOVED***Returns:
***REMOVED***str: The file format.
***REMOVED***"""

***REMOVED***# in case the caller gives us a file path
***REMOVED***file_name = os.path.basename(file_name)
***REMOVED***file_extension = file_name.split(".")[-1]
***REMOVED***if file_extension not in extensions_to_process:
***REMOVED***return None
***REMOVED***return FILE_FORMAT_DICT.get(file_extension, None)

def table_to_html(table):
***REMOVED***table_html = "<table>"
***REMOVED***rows = [sorted([cell for cell in table.cells if cell.row_index == i], key=lambda cell: cell.column_index) for i in range(table.row_count)]
***REMOVED***for row_cells in rows:
***REMOVED***table_html += "<tr>"
***REMOVED***for cell in row_cells:
***REMOVED******REMOVED***tag = "th" if (cell.kind == "columnHeader" or cell.kind == "rowHeader") else "td"
***REMOVED******REMOVED***cell_spans = ""
***REMOVED******REMOVED***if cell.column_span > 1: cell_spans += f" colSpan={cell.column_span}"
***REMOVED******REMOVED***if cell.row_span > 1: cell_spans += f" rowSpan={cell.row_span}"
***REMOVED******REMOVED***table_html += f"<{tag}{cell_spans}>{html.escape(cell.content)}</{tag}>"
***REMOVED***table_html +="</tr>"
***REMOVED***table_html += "</table>"
***REMOVED***return table_html

def extract_pdf_content(file_path, form_recognizer_client, use_layout=False): 
***REMOVED***offset = 0
***REMOVED***page_map = []
***REMOVED***model = "prebuilt-layout" if use_layout else "prebuilt-read"
***REMOVED***with open(file_path, "rb") as f:
***REMOVED***poller = form_recognizer_client.begin_analyze_document(model, document = f)
***REMOVED***form_recognizer_results = poller.result()

***REMOVED***# (if using layout) mark all the positions of headers
***REMOVED***roles_start = {}
***REMOVED***roles_end = {}
***REMOVED***for paragraph in form_recognizer_results.paragraphs:
***REMOVED***if paragraph.role!=None:
***REMOVED******REMOVED***para_start = paragraph.spans[0].offset
***REMOVED******REMOVED***para_end = paragraph.spans[0].offset + paragraph.spans[0].length
***REMOVED******REMOVED***roles_start[para_start] = paragraph.role
***REMOVED******REMOVED***roles_end[para_end] = paragraph.role

***REMOVED***for page_num, page in enumerate(form_recognizer_results.pages):
***REMOVED***tables_on_page = [table for table in form_recognizer_results.tables if table.bounding_regions[0].page_number == page_num + 1]

***REMOVED***# (if using layout) mark all positions of the table spans in the page
***REMOVED***page_offset = page.spans[0].offset
***REMOVED***page_length = page.spans[0].length
***REMOVED***table_chars = [-1]*page_length
***REMOVED***for table_id, table in enumerate(tables_on_page):
***REMOVED******REMOVED***for span in table.spans:
***REMOVED******REMOVED***# replace all table spans with "table_id" in table_chars array
***REMOVED******REMOVED***for i in range(span.length):
***REMOVED******REMOVED******REMOVED***idx = span.offset - page_offset + i
***REMOVED******REMOVED******REMOVED***if idx >=0 and idx < page_length:
***REMOVED******REMOVED******REMOVED***table_chars[idx] = table_id

***REMOVED***# build page text by replacing charcters in table spans with table html and replace the characters corresponding to headers with html headers, if using layout
***REMOVED***page_text = ""
***REMOVED***added_tables = set()
***REMOVED***for idx, table_id in enumerate(table_chars):
***REMOVED******REMOVED***if table_id == -1:
***REMOVED******REMOVED***position = page_offset + idx
***REMOVED******REMOVED***if position in roles_start.keys():
***REMOVED******REMOVED******REMOVED***role = roles_start[position]
***REMOVED******REMOVED******REMOVED***page_text += f"<{PDF_HEADERS[role]}>"
***REMOVED******REMOVED***if position in roles_end.keys():
***REMOVED******REMOVED******REMOVED***role = roles_end[position]
***REMOVED******REMOVED******REMOVED***page_text += f"</{PDF_HEADERS[role]}>"
***REMOVED******REMOVED***
***REMOVED******REMOVED***page_text += form_recognizer_results.content[page_offset + idx]
***REMOVED******REMOVED***
***REMOVED******REMOVED***elif not table_id in added_tables:
***REMOVED******REMOVED***page_text += table_to_html(tables_on_page[table_id])
***REMOVED******REMOVED***added_tables.add(table_id)

***REMOVED***page_text += " "
***REMOVED***page_map.append((page_num, offset, page_text))
***REMOVED***offset += len(page_text)

***REMOVED***full_text = "".join([page_text for _, _, page_text in page_map])
***REMOVED***return full_text

def merge_chunks_serially(chunked_content_list: List[str], num_tokens: int) -> Generator[Tuple[str, int], None, None]:
***REMOVED***# TODO: solve for token overlap
***REMOVED***current_chunk = ""
***REMOVED***total_size = 0
***REMOVED***for chunked_content in chunked_content_list:
***REMOVED***chunk_size = TOKEN_ESTIMATOR.estimate_tokens(chunked_content)
***REMOVED***if total_size > 0:
***REMOVED******REMOVED***new_size = total_size + chunk_size
***REMOVED******REMOVED***if new_size > num_tokens:
***REMOVED******REMOVED***yield current_chunk, total_size
***REMOVED******REMOVED***current_chunk = ""
***REMOVED******REMOVED***total_size = 0
***REMOVED***total_size += chunk_size
***REMOVED***current_chunk += chunked_content
***REMOVED***if total_size > 0:
***REMOVED***yield current_chunk, total_size


def chunk_content_helper(
***REMOVED***content: str, file_format: str, file_name: Optional[str],
***REMOVED***token_overlap: int,
***REMOVED***num_tokens: int = 256
) -> Generator[Tuple[str, int, Document], None, None]:
***REMOVED***if num_tokens is None:
***REMOVED***num_tokens = 1000000000

***REMOVED***parser = parser_factory(file_format)
***REMOVED***doc = parser.parse(content, file_name=file_name)

***REMOVED***# if the original doc after parsing is < num_tokens return as it is
***REMOVED***doc_content_size = TOKEN_ESTIMATOR.estimate_tokens(doc.content)
***REMOVED***if doc_content_size < num_tokens:
***REMOVED***yield doc.content, doc_content_size, doc
***REMOVED***else:
***REMOVED***if file_format == "markdown":
***REMOVED******REMOVED***splitter = MarkdownTextSplitter.from_tiktoken_encoder(
***REMOVED******REMOVED***chunk_size=num_tokens, chunk_overlap=token_overlap)
***REMOVED******REMOVED***chunked_content_list = splitter.split_text(
***REMOVED******REMOVED***content)  # chunk the original content
***REMOVED******REMOVED***for chunked_content, chunk_size in merge_chunks_serially(chunked_content_list, num_tokens):
***REMOVED******REMOVED***chunk_doc = parser.parse(chunked_content, file_name=file_name)
***REMOVED******REMOVED***chunk_doc.title = doc.title
***REMOVED******REMOVED***yield chunk_doc.content, chunk_size, chunk_doc
***REMOVED***else:
***REMOVED******REMOVED***if file_format == "python":
***REMOVED******REMOVED***splitter = PythonCodeTextSplitter.from_tiktoken_encoder(
***REMOVED******REMOVED******REMOVED***chunk_size=num_tokens, chunk_overlap=token_overlap)
***REMOVED******REMOVED***else:
***REMOVED******REMOVED***splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
***REMOVED******REMOVED******REMOVED***separators=SENTENCE_ENDINGS + WORDS_BREAKS,
***REMOVED******REMOVED******REMOVED***chunk_size=num_tokens, chunk_overlap=token_overlap)
***REMOVED******REMOVED***chunked_content_list = splitter.split_text(doc.content)
***REMOVED******REMOVED***for chunked_content in chunked_content_list:
***REMOVED******REMOVED***chunk_size = TOKEN_ESTIMATOR.estimate_tokens(chunked_content)
***REMOVED******REMOVED***yield chunked_content, chunk_size, doc

def chunk_content(
***REMOVED***content: str,
***REMOVED***file_name: Optional[str] = None,
***REMOVED***url: Optional[str] = None,
***REMOVED***ignore_errors: bool = True,
***REMOVED***num_tokens: int = 256,
***REMOVED***min_chunk_size: int = 10,
***REMOVED***token_overlap: int = 0,
***REMOVED***extensions_to_process = FILE_FORMAT_DICT.keys(),
***REMOVED***cracked_pdf = False,
***REMOVED***use_layout = False
) -> ChunkingResult:
***REMOVED***"""Chunks the given content. If ignore_errors is true, returns None
***REMOVED***in case of an error
***REMOVED***Args:
***REMOVED***content (str): The content to chunk.
***REMOVED***file_name (str): The file name. used for title, file format detection.
***REMOVED***url (str): The url. used for title.
***REMOVED***ignore_errors (bool): If true, ignores errors and returns None.
***REMOVED***num_tokens (int): The number of tokens in each chunk.
***REMOVED***min_chunk_size (int): The minimum chunk size below which chunks will be filtered.
***REMOVED***token_overlap (int): The number of tokens to overlap between chunks.
***REMOVED***Returns:
***REMOVED***List[Document]: List of chunked documents.
***REMOVED***"""

***REMOVED***try:
***REMOVED***if file_name is None or (cracked_pdf and not use_layout):
***REMOVED******REMOVED***file_format = "text"
***REMOVED***elif cracked_pdf:
***REMOVED******REMOVED***file_format = "html"
***REMOVED***else:
***REMOVED******REMOVED***file_format = _get_file_format(file_name, extensions_to_process)
***REMOVED******REMOVED***if file_format is None:
***REMOVED******REMOVED***raise Exception(
***REMOVED******REMOVED******REMOVED***f"{file_name} is not supported")

***REMOVED***chunked_context = chunk_content_helper(
***REMOVED******REMOVED***content=content,
***REMOVED******REMOVED***file_name=file_name,
***REMOVED******REMOVED***file_format=file_format,
***REMOVED******REMOVED***num_tokens=num_tokens,
***REMOVED******REMOVED***token_overlap=token_overlap
***REMOVED***)
***REMOVED***chunks = []
***REMOVED***skipped_chunks = 0
***REMOVED***for chunk, chunk_size, doc in chunked_context:
***REMOVED******REMOVED***if chunk_size >= min_chunk_size:
***REMOVED******REMOVED***chunks.append(
***REMOVED******REMOVED******REMOVED***Document(
***REMOVED******REMOVED******REMOVED***content=chunk,
***REMOVED******REMOVED******REMOVED***title=doc.title,
***REMOVED******REMOVED******REMOVED***url=url,
***REMOVED******REMOVED******REMOVED***)
***REMOVED******REMOVED***)
***REMOVED******REMOVED***else:
***REMOVED******REMOVED***skipped_chunks += 1

***REMOVED***except UnsupportedFormatError as e:
***REMOVED***if ignore_errors:
***REMOVED******REMOVED***return ChunkingResult(
***REMOVED******REMOVED***chunks=[], total_files=1, num_unsupported_format_files=1
***REMOVED******REMOVED***)
***REMOVED***else:
***REMOVED******REMOVED***raise e
***REMOVED***except Exception as e:
***REMOVED***if ignore_errors:
***REMOVED******REMOVED***return ChunkingResult(chunks=[], total_files=1, num_files_with_errors=1)
***REMOVED***else:
***REMOVED******REMOVED***raise e
***REMOVED***return ChunkingResult(
***REMOVED***chunks=chunks,
***REMOVED***total_files=1,
***REMOVED***skipped_chunks=skipped_chunks,
***REMOVED***)

def chunk_file(
***REMOVED***file_path: str,
***REMOVED***ignore_errors: bool = True,
***REMOVED***num_tokens=256,
***REMOVED***min_chunk_size=10,
***REMOVED***url = None,
***REMOVED***token_overlap: int = 0,
***REMOVED***extensions_to_process = FILE_FORMAT_DICT.keys(),
***REMOVED***form_recognizer_client = None,
***REMOVED***use_layout = False
) -> ChunkingResult:
***REMOVED***"""Chunks the given file.
***REMOVED***Args:
***REMOVED***file_path (str): The file to chunk.
***REMOVED***Returns:
***REMOVED***List[Document]: List of chunked documents.
***REMOVED***"""
***REMOVED***file_name = os.path.basename(file_path)
***REMOVED***file_format = _get_file_format(file_name, extensions_to_process)
***REMOVED***if not file_format:
***REMOVED***if ignore_errors:
***REMOVED******REMOVED***return ChunkingResult(
***REMOVED******REMOVED***chunks=[], total_files=1, num_unsupported_format_files=1
***REMOVED******REMOVED***)
***REMOVED***else:
***REMOVED******REMOVED***raise UnsupportedFormatError(f"{file_name} is not supported")

***REMOVED***cracked_pdf = False
***REMOVED***if file_format == "pdf":
***REMOVED***if form_recognizer_client is None:
***REMOVED******REMOVED***raise UnsupportedFormatError("form_recognizer_client is required for pdf files")
***REMOVED***content = extract_pdf_content(file_path, form_recognizer_client, use_layout=use_layout)
***REMOVED***cracked_pdf = True
***REMOVED***else:
***REMOVED***with open(file_path, "r", encoding="utf8") as f:
***REMOVED******REMOVED***content = f.read()
***REMOVED***return chunk_content(
***REMOVED***content=content,
***REMOVED***file_name=file_name,
***REMOVED***ignore_errors=ignore_errors,
***REMOVED***num_tokens=num_tokens,
***REMOVED***min_chunk_size=min_chunk_size,
***REMOVED***url=url,
***REMOVED***token_overlap=max(0, token_overlap),
***REMOVED***extensions_to_process=extensions_to_process,
***REMOVED***cracked_pdf=cracked_pdf,
***REMOVED***use_layout=use_layout
***REMOVED***)


def process_file(
***REMOVED***file_path: str, # !IMP: Please keep this as the first argument
***REMOVED***directory_path: str,
***REMOVED***ignore_errors: bool = True,
***REMOVED***num_tokens: int = 1024,
***REMOVED***min_chunk_size: int = 10,
***REMOVED***url_prefix = None,
***REMOVED***token_overlap: int = 0,
***REMOVED***extensions_to_process: List[str] = FILE_FORMAT_DICT.keys(),
***REMOVED***form_recognizer_client = None,
***REMOVED***use_layout = False
***REMOVED***):

***REMOVED***if not form_recognizer_client:
***REMOVED***form_recognizer_client = SingletonFormRecognizerClient()

***REMOVED***is_error = False
***REMOVED***try:
***REMOVED***url_path = None
***REMOVED***rel_file_path = os.path.relpath(file_path, directory_path)
***REMOVED***if url_prefix:
***REMOVED******REMOVED***url_path = url_prefix + rel_file_path
***REMOVED******REMOVED***url_path = convert_escaped_to_posix(url_path)

***REMOVED***result = chunk_file(
***REMOVED******REMOVED***file_path,
***REMOVED******REMOVED***ignore_errors=ignore_errors,
***REMOVED******REMOVED***num_tokens=num_tokens,
***REMOVED******REMOVED***min_chunk_size=min_chunk_size,
***REMOVED******REMOVED***url=url_path,
***REMOVED******REMOVED***token_overlap=token_overlap,
***REMOVED******REMOVED***extensions_to_process=extensions_to_process,
***REMOVED******REMOVED***form_recognizer_client=form_recognizer_client,
***REMOVED******REMOVED***use_layout=use_layout
***REMOVED***)
***REMOVED***for chunk_idx, chunk_doc in enumerate(result.chunks):
***REMOVED******REMOVED***chunk_doc.filepath = rel_file_path
***REMOVED******REMOVED***chunk_doc.metadata = json.dumps({"chunk_id": str(chunk_idx)})
***REMOVED***except Exception as e:
***REMOVED***if not ignore_errors:
***REMOVED******REMOVED***raise
***REMOVED***print(f"File ({file_path}) failed with ", e)
***REMOVED***is_error = True
***REMOVED***result =None
***REMOVED***return result, is_error


def chunk_directory(
***REMOVED***directory_path: str,
***REMOVED***ignore_errors: bool = True,
***REMOVED***num_tokens: int = 1024,
***REMOVED***min_chunk_size: int = 10,
***REMOVED***url_prefix = None,
***REMOVED***token_overlap: int = 0,
***REMOVED***extensions_to_process: List[str] = list(FILE_FORMAT_DICT.keys()),
***REMOVED***form_recognizer_client = None,
***REMOVED***use_layout = False,
***REMOVED***njobs=4
):
***REMOVED***"""
***REMOVED***Chunks the given directory recursively
***REMOVED***Args:
***REMOVED***directory_path (str): The directory to chunk.
***REMOVED***ignore_errors (bool): If true, ignores errors and returns None.
***REMOVED***num_tokens (int): The number of tokens to use for chunking.
***REMOVED***min_chunk_size (int): The minimum chunk size.
***REMOVED***url_prefix (str): The url prefix to use for the files. If None, the url will be None. If not None, the url will be url_prefix + relpath. 
***REMOVED******REMOVED******REMOVED******REMOVED***For example, if the directory path is /home/user/data and the url_prefix is https://example.com/data, 
***REMOVED******REMOVED******REMOVED******REMOVED***then the url for the file /home/user/data/file1.txt will be https://example.com/data/file1.txt
***REMOVED***token_overlap (int): The number of tokens to overlap between chunks.
***REMOVED***extensions_to_process (List[str]): The list of extensions to process. 
***REMOVED***form_recognizer_client: Optional form recognizer client to use for pdf files.
***REMOVED***use_layout (bool): If true, uses Layout model for pdf files. Otherwise, uses Read.

***REMOVED***Returns:
***REMOVED***List[Document]: List of chunked documents.
***REMOVED***"""
***REMOVED***chunks = []
***REMOVED***total_files = 0
***REMOVED***num_unsupported_format_files = 0
***REMOVED***num_files_with_errors = 0
***REMOVED***skipped_chunks = 0

***REMOVED***all_files_directory = get_files_recursively(directory_path)
***REMOVED***files_to_process = [file_path for file_path in all_files_directory if os.path.isfile(file_path)]
***REMOVED***print(f"Total files to process={len(files_to_process)} out of total directory size={len(all_files_directory)}")


***REMOVED***if njobs==1:
***REMOVED***print("Single process to chunk and parse the files. --njobs > 1 can help performance.")
***REMOVED***for file_path in tqdm(files_to_process):
***REMOVED******REMOVED***total_files += 1
***REMOVED******REMOVED***result, is_error = process_file(file_path=file_path,directory_path=directory_path, ignore_errors=ignore_errors,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***   num_tokens=num_tokens,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***   min_chunk_size=min_chunk_size, url_prefix=url_prefix,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***   token_overlap=token_overlap,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***   extensions_to_process=extensions_to_process,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***   form_recognizer_client=form_recognizer_client, use_layout=use_layout)
***REMOVED******REMOVED***if is_error:
***REMOVED******REMOVED***num_files_with_errors += 1
***REMOVED******REMOVED***continue
***REMOVED******REMOVED***chunks.extend(result.chunks)
***REMOVED******REMOVED***num_unsupported_format_files += result.num_unsupported_format_files
***REMOVED******REMOVED***num_files_with_errors += result.num_files_with_errors
***REMOVED******REMOVED***skipped_chunks += result.skipped_chunks
***REMOVED***elif njobs > 1:
***REMOVED***print(f"Multiprocessing with njobs={njobs}")
***REMOVED***process_file_partial = partial(process_file, directory_path=directory_path, ignore_errors=ignore_errors,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***   num_tokens=num_tokens,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***   min_chunk_size=min_chunk_size, url_prefix=url_prefix,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***   token_overlap=token_overlap,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***   extensions_to_process=extensions_to_process,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***   form_recognizer_client=None, use_layout=use_layout)
***REMOVED***with ProcessPoolExecutor(max_workers=njobs) as executor:
***REMOVED******REMOVED***futures = list(tqdm(executor.map(process_file_partial, files_to_process), total=len(files_to_process)))
***REMOVED******REMOVED***for result, is_error in futures:
***REMOVED******REMOVED***total_files += 1
***REMOVED******REMOVED***if is_error:
***REMOVED******REMOVED******REMOVED***num_files_with_errors += 1
***REMOVED******REMOVED******REMOVED***continue
***REMOVED******REMOVED***chunks.extend(result.chunks)
***REMOVED******REMOVED***num_unsupported_format_files += result.num_unsupported_format_files
***REMOVED******REMOVED***num_files_with_errors += result.num_files_with_errors
***REMOVED******REMOVED***skipped_chunks += result.skipped_chunks

***REMOVED***return ChunkingResult(
***REMOVED******REMOVED***chunks=chunks,
***REMOVED******REMOVED***total_files=total_files,
***REMOVED******REMOVED***num_unsupported_format_files=num_unsupported_format_files,
***REMOVED******REMOVED***num_files_with_errors=num_files_with_errors,
***REMOVED******REMOVED***skipped_chunks=skipped_chunks,
***REMOVED***)


class SingletonFormRecognizerClient:
***REMOVED***instance = None
***REMOVED***url = os.getenv("FORM_RECOGNIZER_ENDPOINT")
***REMOVED***key = os.getenv("FORM_RECOGNIZER_KEY")

***REMOVED***def __new__(cls, *args, **kwargs):
***REMOVED***if not cls.instance:
***REMOVED******REMOVED***print("SingletonFormRecognizerClient: Creating instance of Form recognizer per process")
***REMOVED******REMOVED***if cls.url and cls.key:
***REMOVED******REMOVED***cls.instance = DocumentAnalysisClient(endpoint=cls.url, credential=AzureKeyCredential(cls.key))
***REMOVED******REMOVED***else:
***REMOVED******REMOVED***print("SingletonFormRecognizerClient: Skipping since credentials not provided. Assuming NO form recognizer extensions(like .pdf) in directory")
***REMOVED******REMOVED***cls.instance = object() # dummy object
***REMOVED***return cls.instance

***REMOVED***def __getstate__(self):
***REMOVED***return self.url, self.key

***REMOVED***def __setstate__(self, state):
***REMOVED***url, key = state
***REMOVED***self.instance = DocumentAnalysisClient(endpoint=url, credential=AzureKeyCredential(key))
