"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
from io import BytesIO
from pathlib import Path

from folio_pdf.document import Document
from folio_pdf.font import Font
from folio_pdf.merger import PDFMerger
from folio_pdf.outline import Outline
from folio_pdf.page import Page
from folio_pdf.reader import PDFReader
from folio_pdf.redactor_options import RedactorOptions
from folio_pdf.signer_options import SignerOptions

from .core import lib

__all__ = [
    "Document",
    "Page",
    "Font",
    "PDFMerger",
    "Outline",
    "PDFReader",
    "RedactorOptions",
    "SignerOptions",
]


lib.folio_html_to_pdf.argtypes = [ct.c_char_p, ct.c_char_p]
lib.folio_html_to_pdf.restype = ct.c_int32


def html_to_pdf(html: str, destination: str | Path):
    _destination = destination
    if isinstance(_destination, Path):
        _destination = _destination.as_posix()
    if not _destination.endswith("pdf"):
        _destination += ".pdf"
    return lib.folio_html_to_pdf(
        ct.c_char_p(html.encode()), ct.c_char_p(_destination.encode())
    )


lib.folio_html_to_buffer.argtypes = [ct.c_char_p, ct.c_double, ct.c_double]
lib.folio_html_to_buffer.restype = ct.c_int64

lib.folio_buffer_data.restype = ct.c_void_p


def html_to_buffer(html: str, page_width: float, page_height: float) -> BytesIO:
    buf = lib.folio_html_to_buffer(
        ct.c_char_p(html.encode()),
        ct.c_double(page_width),
        ct.c_double(page_height),
    )
    size = lib.folio_buffer_len(buf)
    ptr = lib.folio_buffer_data(buf)
    data = ct.string_at(ptr, size)
    lib.folio_buffer_free(buf)
    return BytesIO(data)


def html_convert(html: str, page_width: float, page_height: float) -> Document:
    doc_handle = lib.folio_html_convert(
        ct.c_char_p(html.encode()),
        ct.c_double(page_width),
        ct.c_double(page_height),
    )
    return Document._new_from_handle(doc_handle)


lib.folio_html_parse_css_length.argtypes = [
    ct.c_char_p,
    ct.c_double,
    ct.c_double,
]
lib.folio_html_parse_css_length.restype = ct.c_double


def html_parse_css_length(s: str, font_size: float, relative_to: float) -> float:
    return lib.folio_html_parse_css_length(
        ct.c_char_p(s.encode()),
        ct.c_double(font_size),
        ct.c_double(relative_to),
    )


def sign_pdf(pdf_data: bytes, opts: SignerOptions):
    buf = lib.folio_sign_pdf(
        ct.c_char_p(pdf_data), ct.c_int32(len(pdf_data)), opts.handle
    )
    size = lib.folio_buffer_len(buf)
    ptr = lib.folio_buffer_data(buf)
    data = ct.string_at(ptr, size)
    lib.folio_buffer_free(buf)
    return data


def redact_text(reader: PDFReader, targets: list[str], opts: RedactorOptions): ...


def redact_pattern(reader: PDFReader, pattern: str, opts: RedactorOptions): ...


def redact_regions(
    reader: PDFReader,
): ...
