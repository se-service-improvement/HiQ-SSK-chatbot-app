"""Data utilities for index preparation."""
import ast
import html
import json
import os
import re
import ssl
import subprocess
import tempfile
import time
import urllib.request
from abc import ABC, abstractmethod
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from functools import partial
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Union
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
import fitz
import requests
import base64

import markdown
import requests
import tiktoken
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.text_splitter import TextSplitter, MarkdownTextSplitter, RecursiveCharacterTextSplitter, PythonCodeTextSplitter
from openai import AzureOpenAI
from tqdm import tqdm

# Configure environment variables  
load_dotenv() # take environment variables from .env.

FILE_FORMAT_DICT = {
***REMOVED***"md": "markdown",
***REMOVED***"txt": "text",
***REMOVED***"html": "html",
***REMOVED***"shtml": "html",
***REMOVED***"htm": "html",
***REMOVED***"py": "python",
***REMOVED***"pdf": "pdf",
***REMOVED***"docx": "docx",
***REMOVED***"pptx": "pptx",
***REMOVED***"png": "png",
***REMOVED***"jpg": "jpg",
***REMOVED***"jpeg": "jpeg",
***REMOVED***"gif": "gif",
***REMOVED***"webp": "webp"
***REMOVED***

RETRY_COUNT = 5

SENTENCE_ENDINGS = [".", "!", "?"]
WORDS_BREAKS = list(reversed([",", ";", ":", " ", "(", ")", "[", "]", "{", "}", "\t", "\n"]))

HTML_TABLE_TAGS = {"table_open": "<table>", "table_close": "</table>", "row_open":"<tr>"}

PDF_HEADERS = {
***REMOVED***"title": "h1",
***REMOVED***"sectionHeading": "h2"
}

class TokenEstimator(object):
***REMOVED***GPT2_TOKENIZER = tiktoken.get_encoding("gpt2")

***REMOVED***def estimate_tokens(self, text: Union[str, List]) -> int:

***REMOVED***return len(self.GPT2_TOKENIZER.encode(text, allowed_special="all"))

***REMOVED***def construct_tokens_with_size(self, tokens: str, numofTokens: int) -> str:
***REMOVED***newTokens = self.GPT2_TOKENIZER.decode(
***REMOVED******REMOVED***self.GPT2_TOKENIZER.encode(tokens, allowed_special="all")[:numofTokens]
***REMOVED***)
***REMOVED***return newTokens

TOKEN_ESTIMATOR = TokenEstimator()

class PdfTextSplitter(TextSplitter):
***REMOVED***def __init__(self, length_function: Callable[[str], int] =TOKEN_ESTIMATOR.estimate_tokens, separator: str = "\n\n", **kwargs: Any):
***REMOVED***"""Create a new TextSplitter for htmls from extracted pdfs."""
***REMOVED***super().__init__(**kwargs)
***REMOVED***self._table_tags = HTML_TABLE_TAGS
***REMOVED***self._separators = separator or ["\n\n", "\n", " ", ""]
***REMOVED***self._length_function = length_function
***REMOVED***self._noise = 50 # tokens to accommodate differences in token calculation, we don't want the chunking-on-the-fly to inadvertently chunk anything due to token calc mismatch

***REMOVED***def extract_caption(self, text):
***REMOVED***separator = self._separators[-1]
***REMOVED***for _s in self._separators:
***REMOVED******REMOVED***if _s == "":
***REMOVED******REMOVED***separator = _s
***REMOVED******REMOVED***break
***REMOVED******REMOVED***if _s in text:
***REMOVED******REMOVED***separator = _s
***REMOVED******REMOVED***break
***REMOVED***
***REMOVED***# Now that we have the separator, split the text
***REMOVED***if separator:
***REMOVED******REMOVED***lines = text.split(separator)
***REMOVED***else:
***REMOVED******REMOVED***lines = list(text)
***REMOVED***
***REMOVED***# remove empty lines
***REMOVED***lines = [line for line in lines if line!='']
***REMOVED***caption = ""
***REMOVED***
***REMOVED***if len(text.split(f"<{PDF_HEADERS['title']}>"))>1:
***REMOVED******REMOVED***caption +=  text.split(f"<{PDF_HEADERS['title']}>")[-1].split(f"</{PDF_HEADERS['title']}>")[0]
***REMOVED***if len(text.split(f"<{PDF_HEADERS['sectionHeading']}>"))>1:
***REMOVED******REMOVED***caption +=  text.split(f"<{PDF_HEADERS['sectionHeading']}>")[-1].split(f"</{PDF_HEADERS['sectionHeading']}>")[0]
***REMOVED***
***REMOVED***caption += "\n"+ lines[-1].strip()

***REMOVED***return caption
***REMOVED***
***REMOVED***def mask_urls_and_imgs(self, text) -> Tuple[Dict[str, str], str]:

***REMOVED***def find_urls(string):
***REMOVED******REMOVED***regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^()\s<>]+|\(([^()\s<>]+|(\([^()\s<>]+\)))*\))+(?:\(([^()\s<>]+|(\([^()\s<>]+\)))*\)|[^()\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
***REMOVED******REMOVED***urls = re.findall(regex, string)
***REMOVED******REMOVED***return [x[0] for x in urls]
***REMOVED***
***REMOVED***def find_imgs(string):
***REMOVED******REMOVED***regex = r'(<img\s+src="[^"]+"[^>]*>.*?</img>)'
***REMOVED******REMOVED***imgs = re.findall(regex, string, re.DOTALL)
***REMOVED******REMOVED***return imgs
***REMOVED***
***REMOVED***content_dict = {}
***REMOVED***masked_text = text
***REMOVED***urls = set(find_urls(text))

***REMOVED***for i, url in enumerate(urls):
***REMOVED******REMOVED***masked_text = masked_text.replace(url, f"##URL{i}##")
***REMOVED******REMOVED***content_dict[f"##URL{i}##"] = url

***REMOVED***imgs = set(find_imgs(text))
***REMOVED***for i, img in enumerate(imgs):
***REMOVED******REMOVED***masked_text = masked_text.replace(img, f"##IMG{i}##")
***REMOVED******REMOVED***content_dict[f"##IMG{i}##"] = img

***REMOVED***return content_dict, masked_text

***REMOVED***def split_text(self, text: str) -> List[str]:
***REMOVED***content_dict, masked_text = self.mask_urls_and_imgs(text)
***REMOVED***start_tag = self._table_tags["table_open"]
***REMOVED***end_tag = self._table_tags["table_close"]
***REMOVED***splits = masked_text.split(start_tag)
***REMOVED***
***REMOVED***final_chunks = self.chunk_rest(splits[0]) # the first split is before the first table tag so it is regular text
***REMOVED***
***REMOVED***table_caption_prefix = ""
***REMOVED***if len(final_chunks)>0:
***REMOVED******REMOVED***table_caption_prefix += self.extract_caption(final_chunks[-1]) # extracted from the last chunk before the table
***REMOVED***for part in splits[1:]:
***REMOVED******REMOVED***table, rest = part.split(end_tag)
***REMOVED******REMOVED***table = start_tag + table + end_tag 
***REMOVED******REMOVED***minitables = self.chunk_table(table, table_caption_prefix)
***REMOVED******REMOVED***final_chunks.extend(minitables)

***REMOVED******REMOVED***if rest.strip()!="":
***REMOVED******REMOVED***text_minichunks = self.chunk_rest(rest)
***REMOVED******REMOVED***final_chunks.extend(text_minichunks)
***REMOVED******REMOVED***table_caption_prefix = self.extract_caption(text_minichunks[-1])
***REMOVED******REMOVED***else:
***REMOVED******REMOVED***table_caption_prefix = ""
***REMOVED******REMOVED***

***REMOVED***final_final_chunks = [chunk for chunk, chunk_size in merge_chunks_serially(final_chunks, self._chunk_size, content_dict)]

***REMOVED***return final_final_chunks



***REMOVED***def chunk_rest(self, item):
***REMOVED***separator = self._separators[-1]
***REMOVED***for _s in self._separators:
***REMOVED******REMOVED***if _s == "":
***REMOVED******REMOVED***separator = _s
***REMOVED******REMOVED***break
***REMOVED******REMOVED***if _s in item:
***REMOVED******REMOVED***separator = _s
***REMOVED******REMOVED***break
***REMOVED***chunks = []
***REMOVED***if separator:
***REMOVED******REMOVED***splits = item.split(separator)
***REMOVED***else:
***REMOVED******REMOVED***splits = list(item)
***REMOVED***_good_splits = []
***REMOVED***for s in splits:
***REMOVED******REMOVED***if self._length_function(s) < self._chunk_size - self._noise:
***REMOVED******REMOVED***_good_splits.append(s)
***REMOVED******REMOVED***else:
***REMOVED******REMOVED***if _good_splits:
***REMOVED******REMOVED******REMOVED***merged_text = self._merge_splits(_good_splits, separator)
***REMOVED******REMOVED******REMOVED***chunks.extend(merged_text)
***REMOVED******REMOVED******REMOVED***_good_splits = []
***REMOVED******REMOVED***other_info = self.chunk_rest(s)
***REMOVED******REMOVED***chunks.extend(other_info)
***REMOVED***if _good_splits:
***REMOVED******REMOVED***merged_text = self._merge_splits(_good_splits, separator)
***REMOVED******REMOVED***chunks.extend(merged_text)
***REMOVED***return chunks
***REMOVED***
***REMOVED***def chunk_table(self, table, caption):
***REMOVED***if self._length_function("\n".join([caption, table])) < self._chunk_size - self._noise:
***REMOVED******REMOVED***return ["\n".join([caption, table])]
***REMOVED***else:
***REMOVED******REMOVED***headers = ""
***REMOVED******REMOVED***if re.search("<th.*>.*</th>", table):
***REMOVED******REMOVED***headers += re.search("<th.*>.*</th>", table).group() # extract the header out. Opening tag may contain rowspan/colspan
***REMOVED******REMOVED***splits = table.split(self._table_tags["row_open"]) #split by row tag
***REMOVED******REMOVED***tables = []
***REMOVED******REMOVED***current_table = caption + "\n"
***REMOVED******REMOVED***for part in splits:
***REMOVED******REMOVED***if len(part)>0:
***REMOVED******REMOVED******REMOVED***if self._length_function(current_table + self._table_tags["row_open"] + part) < self._chunk_size: # if current table length is within permissible limit, keep adding rows
***REMOVED******REMOVED******REMOVED***if part not in [self._table_tags["table_open"], self._table_tags["table_close"]]: # need add the separator (row tag) when the part is not a table tag
***REMOVED******REMOVED******REMOVED******REMOVED***current_table += self._table_tags["row_open"]
***REMOVED******REMOVED******REMOVED***current_table += part
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***else:
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***# if current table size is beyond the permissible limit, complete this as a mini-table and add to final mini-tables list
***REMOVED******REMOVED******REMOVED***current_table += self._table_tags["table_close"]
***REMOVED******REMOVED******REMOVED***tables.append(current_table)

***REMOVED******REMOVED******REMOVED***# start a new table
***REMOVED******REMOVED******REMOVED***current_table = "\n".join([caption, self._table_tags["table_open"], headers])
***REMOVED******REMOVED******REMOVED***if part not in [self._table_tags["table_open"], self._table_tags["table_close"]]:
***REMOVED******REMOVED******REMOVED******REMOVED***current_table += self._table_tags["row_open"]
***REMOVED******REMOVED******REMOVED***current_table += part

***REMOVED******REMOVED***
***REMOVED******REMOVED***# TO DO: fix the case where the last mini table only contain tags
***REMOVED******REMOVED***
***REMOVED******REMOVED***if not current_table.endswith(self._table_tags["table_close"]):
***REMOVED******REMOVED***
***REMOVED******REMOVED***tables.append(current_table + self._table_tags["table_close"])
***REMOVED******REMOVED***else:
***REMOVED******REMOVED***tables.append(current_table)
***REMOVED******REMOVED***return tables

***REMOVED***
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
***REMOVED***contentVector: Optional[List[float]] = None
***REMOVED***image_mapping: Optional[Dict] = None

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

class ImageParser(BaseParser):
***REMOVED***def parse(self, content: str, file_name: Optional[str] = None) -> Document:
***REMOVED***return Document(content=content, title=file_name)

class ParserFactory:
***REMOVED***def __init__(self):
***REMOVED***self._parsers = {
***REMOVED******REMOVED***"html": HTMLParser(),
***REMOVED******REMOVED***"text": TextParser(),
***REMOVED******REMOVED***"markdown": MarkdownParser(),
***REMOVED******REMOVED***"python": PythonParser(),
***REMOVED******REMOVED***"png": ImageParser(),
***REMOVED******REMOVED***"jpg": ImageParser(),
***REMOVED******REMOVED***"jpeg": ImageParser(),
***REMOVED******REMOVED***"gif": ImageParser(),
***REMOVED******REMOVED***"webp": ImageParser()
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

parser_factory = ParserFactory()

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

def extractStorageDetailsFromUrl(url):
***REMOVED***matches = re.fullmatch(r'https:\/\/([^\/.]*)\.blob\.core\.windows\.net\/([^\/]*)\/(.*)', url)
***REMOVED***if not matches:
***REMOVED***raise Exception(f"Not a valid blob storage URL: {url}")
***REMOVED***return (matches.group(1), matches.group(2), matches.group(3))

def downloadBlobUrlToLocalFolder(blob_url, local_folder, credential):
***REMOVED***(storage_account, container_name, path) = extractStorageDetailsFromUrl(blob_url)
***REMOVED***container_url = f'https://{storage_account}.blob.core.windows.net/{container_name}'
***REMOVED***container_client = ContainerClient.from_container_url(container_url, credential=credential)
***REMOVED***if path and not path.endswith('/'):
***REMOVED***path = path + '/'

***REMOVED***last_destination_folder = None
***REMOVED***for blob in container_client.list_blobs(name_starts_with=path):
***REMOVED***relative_path = blob.name[len(path):]
***REMOVED***destination_path = os.path.join(local_folder, relative_path)
***REMOVED***destination_folder = os.path.dirname(destination_path)
***REMOVED***if destination_folder != last_destination_folder:
***REMOVED******REMOVED***os.makedirs(destination_folder, exist_ok=True)
***REMOVED******REMOVED***last_destination_folder = destination_folder
***REMOVED***blob_client = container_client.get_blob_client(blob.name)
***REMOVED***with open(file=destination_path, mode='wb') as local_file:
***REMOVED******REMOVED***stream = blob_client.download_blob()
***REMOVED******REMOVED***local_file.write(stream.readall())

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
***REMOVED******REMOVED***if cell.column_span and cell.column_span > 1: cell_spans += f" colSpan={cell.column_span}"
***REMOVED******REMOVED***if cell.row_span and cell.row_span > 1: cell_spans += f" rowSpan={cell.row_span}"
***REMOVED******REMOVED***table_html += f"<{tag}{cell_spans}>{html.escape(cell.content)}</{tag}>"
***REMOVED***table_html +="</tr>"
***REMOVED***table_html += "</table>"
***REMOVED***return table_html

def polygon_to_bbox(polygon, dpi=72):
***REMOVED***x_coords = polygon[0::2]
***REMOVED***y_coords = polygon[1::2]
***REMOVED***x0, y0 = min(x_coords)*dpi, min(y_coords)*dpi
***REMOVED***x1, y1 = max(x_coords)*dpi, max(y_coords)*dpi
***REMOVED***return x0, y0, x1, y1

def extract_pdf_content(file_path, form_recognizer_client, use_layout=False): 
***REMOVED***offset = 0
***REMOVED***page_map = []
***REMOVED***model = "prebuilt-layout" if use_layout else "prebuilt-read"
***REMOVED***
***REMOVED***base64file = base64.b64encode(open(file_path, "rb").read()).decode()
***REMOVED***poller = form_recognizer_client.begin_analyze_document(model, AnalyzeDocumentRequest(bytes_source=base64file))
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
***REMOVED***page_offset = page.spans[0].offset
***REMOVED***page_length = page.spans[0].length

***REMOVED***if use_layout:
***REMOVED******REMOVED***tables_on_page = []
***REMOVED******REMOVED***for table in form_recognizer_results.tables:
***REMOVED******REMOVED***table_offset = table.spans[0].offset
***REMOVED******REMOVED***table_length = table.spans[0].length
***REMOVED******REMOVED***if page_offset <= table_offset and table_offset + table_length < page_offset + page_length:
***REMOVED******REMOVED******REMOVED***tables_on_page.append(table)
***REMOVED***else:
***REMOVED******REMOVED***tables_on_page = []

***REMOVED***# (if using layout) mark all positions of the table spans in the page
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
***REMOVED******REMOVED******REMOVED***if role in PDF_HEADERS:
***REMOVED******REMOVED******REMOVED***page_text += f"<{PDF_HEADERS[role]}>"
***REMOVED******REMOVED***if position in roles_end.keys():
***REMOVED******REMOVED******REMOVED***role = roles_end[position]
***REMOVED******REMOVED******REMOVED***if role in PDF_HEADERS:
***REMOVED******REMOVED******REMOVED***page_text += f"</{PDF_HEADERS[role]}>"

***REMOVED******REMOVED***page_text += form_recognizer_results.content[page_offset + idx]
***REMOVED******REMOVED***
***REMOVED******REMOVED***elif not table_id in added_tables:
***REMOVED******REMOVED***page_text += table_to_html(tables_on_page[table_id])
***REMOVED******REMOVED***added_tables.add(table_id)

***REMOVED***page_text += " "
***REMOVED***page_map.append((page_num, offset, page_text))
***REMOVED***offset += len(page_text)

***REMOVED***full_text = "".join([page_text for _, _, page_text in page_map])

***REMOVED***# Extract any images
***REMOVED***image_mapping = {}

***REMOVED***if "figures" in form_recognizer_results.keys() and file_path.endswith(".pdf"):
***REMOVED***document = fitz.open(file_path)

***REMOVED***for figure in form_recognizer_results["figures"]:
***REMOVED******REMOVED***bounding_box = figure.bounding_regions[0]

***REMOVED******REMOVED***page_number = bounding_box['pageNumber'] - 1  # Page numbers in PyMuPDF start from 0
***REMOVED******REMOVED***x0, y0, x1, y1 = polygon_to_bbox(bounding_box['polygon'])

***REMOVED******REMOVED***# Select the figure and upscale it by 200% for higher resolution
***REMOVED******REMOVED***page = document.load_page(page_number)
***REMOVED******REMOVED***bbox = fitz.Rect(x0, y0, x1, y1)

***REMOVED******REMOVED***zoom = 2.0 
***REMOVED******REMOVED***mat = fitz.Matrix(zoom, zoom)
***REMOVED******REMOVED***image = page.get_pixmap(matrix=mat, clip=bbox)

***REMOVED******REMOVED***# Save the extracted image to a base64 string
***REMOVED******REMOVED***image_data = image.tobytes(output='jpg')
***REMOVED******REMOVED***image_base64 = base64.b64encode(image_data).decode("utf-8")
***REMOVED******REMOVED***image_base64 = f"data:image/jpg;base64,{image_base64}"

***REMOVED******REMOVED***# Add the image tag to the full text
***REMOVED******REMOVED***replace_start = figure["spans"][0]["offset"]
***REMOVED******REMOVED***replace_end = figure["spans"][0]["offset"] + figure["spans"][0]["length"]
***REMOVED******REMOVED***original_text = form_recognizer_results.content[replace_start:replace_end]

***REMOVED******REMOVED***if original_text not in full_text:
***REMOVED******REMOVED***continue
***REMOVED******REMOVED***
***REMOVED******REMOVED***img_tag = image_content_to_tag(original_text)
***REMOVED******REMOVED***
***REMOVED******REMOVED***full_text = full_text.replace(original_text, img_tag)
***REMOVED******REMOVED***image_mapping[img_tag] = image_base64

***REMOVED***return full_text, image_mapping

def merge_chunks_serially(chunked_content_list: List[str], num_tokens: int, content_dict: Dict[str, str]={}) -> Generator[Tuple[str, int], None, None]:
***REMOVED***def unmask_urls_and_imgs(text, content_dict={}):
***REMOVED***if "##URL" in text or "##IMG" in text:
***REMOVED******REMOVED***for key, value in content_dict.items():
***REMOVED******REMOVED***text = text.replace(key, value)
***REMOVED***return text
***REMOVED***# TODO: solve for token overlap
***REMOVED***current_chunk = ""
***REMOVED***total_size = 0
***REMOVED***for chunked_content in chunked_content_list:
***REMOVED***chunked_content = unmask_urls_and_imgs(chunked_content, content_dict)
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

def get_payload_and_headers_cohere(
***REMOVED***text, aad_token) -> Tuple[Dict, Dict]:
***REMOVED***oai_headers =  {
***REMOVED***"Content-Type": "application/json",
***REMOVED***"Authorization": f"Bearer {aad_token}",
***REMOVED***

***REMOVED***cohere_body = { "texts": [text], "input_type": "search_document" }
***REMOVED***return cohere_body, oai_headers
***REMOVED***
def get_embedding(text, embedding_model_endpoint=None, embedding_model_key=None, azure_credential=None):
***REMOVED***endpoint = embedding_model_endpoint if embedding_model_endpoint else os.environ.get("EMBEDDING_MODEL_ENDPOINT")
***REMOVED***
***REMOVED***FLAG_EMBEDDING_MODEL = os.getenv("FLAG_EMBEDDING_MODEL", "AOAI")
***REMOVED***FLAG_COHERE = os.getenv("FLAG_COHERE", "ENGLISH")
***REMOVED***FLAG_AOAI = os.getenv("FLAG_AOAI", "V3")

***REMOVED***if azure_credential is None and (endpoint is None or key is None):
***REMOVED***raise Exception("EMBEDDING_MODEL_ENDPOINT and EMBEDDING_MODEL_KEY are required for embedding")

***REMOVED***try:
***REMOVED***if FLAG_EMBEDDING_MODEL == "AOAI":
***REMOVED******REMOVED***endpoint_parts = endpoint.split("/openai/deployments/")
***REMOVED******REMOVED***base_url = endpoint_parts[0]
***REMOVED******REMOVED***deployment_id = endpoint_parts[1].split("/embeddings")[0]
***REMOVED******REMOVED***api_version = endpoint_parts[1].split("api-version=")[1].split("&")[0]
***REMOVED******REMOVED***if azure_credential is not None:
***REMOVED******REMOVED***api_key = azure_credential.get_token("https://cognitiveservices.azure.com/.default").token
***REMOVED******REMOVED***else:
***REMOVED******REMOVED***api_key = embedding_model_key if embedding_model_key else os.getenv("AZURE_OPENAI_API_KEY")
***REMOVED******REMOVED***
***REMOVED******REMOVED***client = AzureOpenAI(api_version=api_version, azure_endpoint=base_url, api_key=api_key)
***REMOVED******REMOVED***if FLAG_AOAI == "V2":
***REMOVED******REMOVED***embeddings = client.embeddings.create(model=deployment_id, input=text)
***REMOVED******REMOVED***elif FLAG_AOAI == "V3":   
***REMOVED******REMOVED***embeddings = client.embeddings.create(model=deployment_id, 
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***  input=text, 
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***  dimensions=int(os.getenv("VECTOR_DIMENSION", 1536)))
***REMOVED******REMOVED***
***REMOVED******REMOVED***return embeddings.model_dump()['data'][0]['embedding']
***REMOVED***
***REMOVED***if FLAG_EMBEDDING_MODEL == "COHERE":
***REMOVED******REMOVED***if FLAG_COHERE == "MULTILINGUAL":
***REMOVED******REMOVED***key = embedding_model_key if embedding_model_key else os.getenv("COHERE_MULTILINGUAL_API_KEY")
***REMOVED******REMOVED***elif FLAG_COHERE == "ENGLISH":
***REMOVED******REMOVED***key = embedding_model_key if embedding_model_key else os.getenv("COHERE_ENGLISH_API_KEY")
***REMOVED******REMOVED***data, headers = get_payload_and_headers_cohere(text, key)

***REMOVED******REMOVED***body = str.encode(json.dumps(data))
***REMOVED******REMOVED***req = urllib.request.Request(endpoint, body, headers)
***REMOVED******REMOVED***response = urllib.request.urlopen(req)
***REMOVED******REMOVED***result = response.read()
***REMOVED******REMOVED***result_content = json.loads(result.decode('utf-8'))
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED***return result_content["embeddings"][0]   
***REMOVED***

***REMOVED***except Exception as e:
***REMOVED***raise Exception(f"Error getting embeddings with endpoint={endpoint} with error={e}")


def chunk_content_helper(
***REMOVED***content: str, file_format: str, file_name: Optional[str],
***REMOVED***token_overlap: int,
***REMOVED***num_tokens: int = 256
) -> Generator[Tuple[str, int, Document], None, None]:
***REMOVED***if num_tokens is None:
***REMOVED***num_tokens = 1000000000

***REMOVED***parser = parser_factory(file_format.split("_pdf")[0]) # to handle cracked pdf converted to html
***REMOVED***doc = parser.parse(content, file_name=file_name)
***REMOVED***# if the original doc after parsing is < num_tokens return as it is
***REMOVED***doc_content_size = TOKEN_ESTIMATOR.estimate_tokens(doc.content)
***REMOVED***if doc_content_size < num_tokens or file_format in ["png", "jpg", "jpeg", "gif", "webp"]:
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
***REMOVED******REMOVED***if file_format == "html_pdf": # cracked pdf converted to html
***REMOVED******REMOVED******REMOVED***splitter = PdfTextSplitter(separator=SENTENCE_ENDINGS + WORDS_BREAKS, chunk_size=num_tokens, chunk_overlap=token_overlap)
***REMOVED******REMOVED***else:
***REMOVED******REMOVED******REMOVED***splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
***REMOVED******REMOVED******REMOVED******REMOVED***separators=SENTENCE_ENDINGS + WORDS_BREAKS,
***REMOVED******REMOVED******REMOVED******REMOVED***chunk_size=num_tokens, chunk_overlap=token_overlap)
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
***REMOVED***use_layout = False,
***REMOVED***add_embeddings = False,
***REMOVED***azure_credential = None,
***REMOVED***embedding_endpoint = None,
***REMOVED***image_mapping = {}
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
***REMOVED******REMOVED***file_format = "html_pdf" # differentiate it from native html
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
***REMOVED******REMOVED***if add_embeddings:
***REMOVED******REMOVED******REMOVED***for i in range(RETRY_COUNT):
***REMOVED******REMOVED******REMOVED***try:
***REMOVED******REMOVED******REMOVED******REMOVED***doc.contentVector = get_embedding(chunk, azure_credential=azure_credential, embedding_model_endpoint=embedding_endpoint)
***REMOVED******REMOVED******REMOVED******REMOVED***break
***REMOVED******REMOVED******REMOVED***except Exception as e:
***REMOVED******REMOVED******REMOVED******REMOVED***print(f"Error getting embedding for chunk with error={e}, retrying, current at {i + 1} retry, {RETRY_COUNT - (i + 1)} retries left")
***REMOVED******REMOVED******REMOVED******REMOVED***time.sleep(30)
***REMOVED******REMOVED******REMOVED***if doc.contentVector is None:
***REMOVED******REMOVED******REMOVED***raise Exception(f"Error getting embedding for chunk={chunk}")
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED***doc.image_mapping = {}
***REMOVED******REMOVED***for key, value in image_mapping.items():
***REMOVED******REMOVED******REMOVED***if key in chunk:
***REMOVED******REMOVED******REMOVED***doc.image_mapping[key] = value
***REMOVED******REMOVED***chunks.append(
***REMOVED******REMOVED******REMOVED***Document(
***REMOVED******REMOVED******REMOVED***content=chunk,
***REMOVED******REMOVED******REMOVED***title=doc.title,
***REMOVED******REMOVED******REMOVED***url=url,
***REMOVED******REMOVED******REMOVED***contentVector=doc.contentVector,
***REMOVED******REMOVED******REMOVED***metadata=doc.metadata,
***REMOVED******REMOVED******REMOVED***image_mapping=doc.image_mapping
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

def image_content_to_tag(image_content: str) -> str:
***REMOVED***# We encode the images in an XML-like format to make the replacement very unlikely to conflict with other text
***REMOVED***# This also lets us preserve the content with minimal escaping, just escaping the <img> tags
***REMOVED***random_id = str(time.time()).replace(".", "")[-4:]
***REMOVED***img_tag = f'<img src="IMG_{random_id}.jpg">{image_content.replace("<img>", "&lt;img&gt;").replace("</img>", "&lt;/img&gt;")}</img>'
***REMOVED***return img_tag

def get_caption(image_path, captioning_model_endpoint, captioning_model_key):
***REMOVED***encoded_image = base64.b64encode(open(image_path, 'rb').read()).decode('ascii')
***REMOVED***file_ext = image_path.split(".")[-1]
***REMOVED***headers = {
***REMOVED***"Content-Type": "application/json",
***REMOVED***"api-key": captioning_model_key,
***REMOVED***

***REMOVED***payload = {
***REMOVED***"messages": [
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"role": "system",
***REMOVED******REMOVED***"content": [
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"type": "text",
***REMOVED******REMOVED***"text": "You are a captioning model that helps uses find descriptive captions."
***REMOVED******REMOVED***
***REMOVED******REMOVED***]
***REMOVED***,
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"role": "user",
***REMOVED******REMOVED***"content": [
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"type": "text",
***REMOVED******REMOVED***"text": "Describe this image as if you were describing it to someone who can't see it. "
***REMOVED******REMOVED***,
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"type": "image_url",
***REMOVED******REMOVED***"image_url": {
***REMOVED******REMOVED******REMOVED***"url": f"data:image/{file_ext};base64,{encoded_image}"
***REMOVED******REMOVED***
***REMOVED******REMOVED***
***REMOVED******REMOVED***]
***REMOVED***
***REMOVED***],
***REMOVED***"temperature": 0
***REMOVED***

***REMOVED***for i in range(RETRY_COUNT):
***REMOVED***try:
***REMOVED******REMOVED***response = requests.post(captioning_model_endpoint, headers=headers, json=payload)
***REMOVED******REMOVED***response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
***REMOVED******REMOVED***break
***REMOVED***except Exception as e:
***REMOVED******REMOVED***print(f"Error getting caption with error={e}, retrying, current at {i + 1} retry, {RETRY_COUNT - (i + 1)} retries left")
***REMOVED******REMOVED***time.sleep(15)

***REMOVED***if response.status_code != 200:
***REMOVED***raise Exception(f"Error getting caption with status_code={response.status_code}")
***REMOVED***
***REMOVED***caption = response.json()["choices"][0]["message"]["content"]
***REMOVED***img_tag = image_content_to_tag(caption)
***REMOVED***mapping = {img_tag: f"data:image/{file_ext};base64,{encoded_image}"}

***REMOVED***return img_tag, mapping

def chunk_file(
***REMOVED***file_path: str,
***REMOVED***ignore_errors: bool = True,
***REMOVED***num_tokens=256,
***REMOVED***min_chunk_size=10,
***REMOVED***url = None,
***REMOVED***token_overlap: int = 0,
***REMOVED***extensions_to_process = FILE_FORMAT_DICT.keys(),
***REMOVED***form_recognizer_client = None,
***REMOVED***use_layout = False,
***REMOVED***add_embeddings=False,
***REMOVED***azure_credential = None,
***REMOVED***embedding_endpoint = None,
***REMOVED***captioning_model_endpoint = None,
***REMOVED***captioning_model_key = None
) -> ChunkingResult:
***REMOVED***"""Chunks the given file.
***REMOVED***Args:
***REMOVED***file_path (str): The file to chunk.
***REMOVED***Returns:
***REMOVED***List[Document]: List of chunked documents.
***REMOVED***"""
***REMOVED***file_name = os.path.basename(file_path)
***REMOVED***file_format = _get_file_format(file_name, extensions_to_process)
***REMOVED***image_mapping = {}
***REMOVED***if not file_format:
***REMOVED***if ignore_errors:
***REMOVED******REMOVED***return ChunkingResult(
***REMOVED******REMOVED***chunks=[], total_files=1, num_unsupported_format_files=1
***REMOVED******REMOVED***)
***REMOVED***else:
***REMOVED******REMOVED***raise UnsupportedFormatError(f"{file_name} is not supported")

***REMOVED***cracked_pdf = False
***REMOVED***if file_format in ["pdf", "docx", "pptx"]:
***REMOVED***if form_recognizer_client is None:
***REMOVED******REMOVED***raise UnsupportedFormatError("form_recognizer_client is required for pdf files")
***REMOVED***content, image_mapping = extract_pdf_content(file_path, form_recognizer_client, use_layout=use_layout)
***REMOVED***cracked_pdf = True
***REMOVED***elif file_format in ["png", "jpg", "jpeg", "webp"]:
***REMOVED***# Make call to LLM for a descriptive caption
***REMOVED***if captioning_model_endpoint is None or captioning_model_key is None:
***REMOVED******REMOVED***raise Exception("CAPTIONING_MODEL_ENDPOINT and CAPTIONING_MODEL_KEY are required for images")
***REMOVED***content, image_mapping = get_caption(file_path, captioning_model_endpoint, captioning_model_key)
***REMOVED***else:
***REMOVED***try:
***REMOVED******REMOVED***with open(file_path, "r", encoding="utf8") as f:
***REMOVED******REMOVED***content = f.read()
***REMOVED***except UnicodeDecodeError:
***REMOVED******REMOVED***from chardet import detect
***REMOVED******REMOVED***with open(file_path, "rb") as f:
***REMOVED******REMOVED***binary_content = f.read()
***REMOVED******REMOVED***encoding = detect(binary_content).get('encoding', 'utf8')
***REMOVED******REMOVED***content = binary_content.decode(encoding)
***REMOVED***
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
***REMOVED***use_layout=use_layout,
***REMOVED***add_embeddings=add_embeddings,
***REMOVED***azure_credential=azure_credential,
***REMOVED***embedding_endpoint=embedding_endpoint,
***REMOVED***image_mapping=image_mapping
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
***REMOVED***use_layout = False,
***REMOVED***add_embeddings = False,
***REMOVED***azure_credential = None,
***REMOVED***embedding_endpoint = None,
***REMOVED***captioning_model_endpoint = None,
***REMOVED***captioning_model_key = None
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
***REMOVED******REMOVED***use_layout=use_layout,
***REMOVED******REMOVED***add_embeddings=add_embeddings,
***REMOVED******REMOVED***azure_credential=azure_credential,
***REMOVED******REMOVED***embedding_endpoint=embedding_endpoint,
***REMOVED******REMOVED***captioning_model_endpoint=captioning_model_endpoint,
***REMOVED******REMOVED***captioning_model_key=captioning_model_key
***REMOVED***)
***REMOVED***for chunk_idx, chunk_doc in enumerate(result.chunks):
***REMOVED******REMOVED***chunk_doc.filepath = rel_file_path
***REMOVED******REMOVED***chunk_doc.metadata = json.dumps({"chunk_id": str(chunk_idx)})
***REMOVED******REMOVED***chunk_doc.image_mapping = json.dumps(chunk_doc.image_mapping) if chunk_doc.image_mapping else None
***REMOVED***except Exception as e:
***REMOVED***print(e)
***REMOVED***if not ignore_errors:
***REMOVED******REMOVED***raise
***REMOVED***print(f"File ({file_path}) failed with ", e)
***REMOVED***is_error = True
***REMOVED***result =None
***REMOVED***return result, is_error

def chunk_blob_container(
***REMOVED***blob_url: str,
***REMOVED***credential,
***REMOVED***ignore_errors: bool = True,
***REMOVED***num_tokens: int = 1024,
***REMOVED***min_chunk_size: int = 10,
***REMOVED***url_prefix = None,
***REMOVED***token_overlap: int = 0,
***REMOVED***extensions_to_process: List[str] = list(FILE_FORMAT_DICT.keys()),
***REMOVED***form_recognizer_client = None,
***REMOVED***use_layout = False,
***REMOVED***njobs=4,
***REMOVED***add_embeddings = False,
***REMOVED***azure_credential = None,
***REMOVED***embedding_endpoint = None
):
***REMOVED***with tempfile.TemporaryDirectory() as local_data_folder:
***REMOVED***print(f'Downloading {blob_url} to local folder')
***REMOVED***downloadBlobUrlToLocalFolder(blob_url, local_data_folder, credential)
***REMOVED***print(f'Downloaded.')

***REMOVED***result = chunk_directory(
***REMOVED******REMOVED***local_data_folder,
***REMOVED******REMOVED***ignore_errors=ignore_errors,
***REMOVED******REMOVED***num_tokens=num_tokens,
***REMOVED******REMOVED***min_chunk_size=min_chunk_size,
***REMOVED******REMOVED***url_prefix=url_prefix,
***REMOVED******REMOVED***token_overlap=token_overlap,
***REMOVED******REMOVED***extensions_to_process=extensions_to_process,
***REMOVED******REMOVED***form_recognizer_client=form_recognizer_client,
***REMOVED******REMOVED***use_layout=use_layout,
***REMOVED******REMOVED***njobs=njobs,
***REMOVED******REMOVED***add_embeddings=add_embeddings,
***REMOVED******REMOVED***azure_credential=azure_credential,
***REMOVED******REMOVED***embedding_endpoint=embedding_endpoint
***REMOVED***)

***REMOVED***return result


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
***REMOVED***njobs=4,
***REMOVED***add_embeddings = False,
***REMOVED***azure_credential = None,
***REMOVED***embedding_endpoint = None,
***REMOVED***captioning_model_endpoint = None,
***REMOVED***captioning_model_key = None
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
***REMOVED***add_embeddings (bool): If true, adds a vector embedding to each chunk using the embedding model endpoint and key.

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
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***   form_recognizer_client=form_recognizer_client, use_layout=use_layout, add_embeddings=add_embeddings,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***   azure_credential=azure_credential, embedding_endpoint=embedding_endpoint,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***   captioning_model_endpoint=captioning_model_endpoint, captioning_model_key=captioning_model_key)
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
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***   form_recognizer_client=None, use_layout=use_layout, add_embeddings=add_embeddings,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***   azure_credential=azure_credential, embedding_endpoint=embedding_endpoint,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***   captioning_model_endpoint=captioning_model_endpoint, captioning_model_key=captioning_model_key)
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
***REMOVED***def __new__(cls, *args, **kwargs):
***REMOVED***if not cls.instance:
***REMOVED******REMOVED***print("SingletonFormRecognizerClient: Creating instance of Form recognizer per process")
***REMOVED******REMOVED***url = os.getenv("FORM_RECOGNIZER_ENDPOINT")
***REMOVED******REMOVED***key = os.getenv("FORM_RECOGNIZER_KEY")
***REMOVED******REMOVED***if url and key:
***REMOVED******REMOVED***cls.instance = DocumentIntelligenceClient(
***REMOVED******REMOVED******REMOVED***endpoint=url, credential=AzureKeyCredential(key), headers={"x-ms-useragent": "sample-app-aoai-chatgpt/1.0.0"})
***REMOVED******REMOVED***else:
***REMOVED******REMOVED***print("SingletonFormRecognizerClient: Skipping since credentials not provided. Assuming NO form recognizer extensions(like .pdf) in directory")
***REMOVED******REMOVED***cls.instance = object() # dummy object
***REMOVED***return cls.instance

***REMOVED***def __getstate__(self):
***REMOVED***return self.url, self.key

***REMOVED***def __setstate__(self, state):
***REMOVED***url, key = state
***REMOVED***self.instance = DocumentIntelligenceClient(endpoint=url, credential=AzureKeyCredential(key), headers={"x-ms-useragent": "sample-app-aoai-chatgpt/1.0.0"})
