"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
from io import BytesIO
from pathlib import Path

from folio_pdf.color import Color
from folio_pdf.document import Document
from folio_pdf.enums import ErrorCode
from folio_pdf.exceptions import FolioPDFException
from folio_pdf.font import Font
from folio_pdf.merger import PDFMerger
from folio_pdf.outline import Outline
from folio_pdf.page import Page
from folio_pdf.page_importer import PageImporter
from folio_pdf.reader import PDFReader
from folio_pdf.redactor_options import RedactorOptions
from folio_pdf.signer_options import SignerOptions

from .core import _read_from_obj_buffer, get_folio_version, lib

__all__ = [
    "Document",
    "Page",
    "Font",
    "PDFMerger",
    "Outline",
    "PDFReader",
    "RedactorOptions",
    "SignerOptions",
    "Color",
    "PageImporter",
    "get_folio_version",
]


lib.folio_html_to_pdf.argtypes = [ct.c_char_p, ct.c_char_p]
lib.folio_html_to_pdf.restype = ct.c_int32


def html_to_pdf(html: str, destination: str | Path) -> None:
    """
    Converts an HTML string to a PDF file and writes it to the given path.

     Args:
        html: the HTML content to render
        destination: the destination file path for the generated PDF
    """
    _destination = destination
    if isinstance(_destination, Path):
        _destination = _destination.as_posix()
    if not _destination.endswith("pdf"):
        _destination += ".pdf"
    res_code = lib.folio_html_to_pdf(
        ct.c_char_p(html.encode()), ct.c_char_p(_destination.encode())
    )
    err_code = ErrorCode(res_code)
    if err_code != ErrorCode.OK:
        msg_bytes = lib.folio_last_error()
        lib.folio_string_free(ct.c_char_p(msg_bytes))
        raise FolioPDFException(str(msg_bytes))


lib.folio_html_to_buffer.argtypes = [ct.c_char_p, ct.c_double, ct.c_double]
lib.folio_html_to_buffer.restype = ct.c_int64

lib.folio_buffer_data.restype = ct.c_void_p


def html_to_buffer(html: str, page_width: float, page_height: float) -> BytesIO:
    """
    Converts an HTML string to a PDF with custom page dimensions and returns
    the raw bytes in an in memory buffer.

    Args:
        html: the HTML content to render
        page_width: page width in points
        page_height: page height in points

    Returns:
        the generated PDF in a buffer

    Example:
        ```python
        from folio_pdf import html_to_buffer
        from folio_pdf.enums import PageSizes

        # Using the dimensions of an A4 page size
        width, height = PageSizes.A4.dimensions
        result = html_to_buffer(
            html='<h1>Folio PDF is awesome!</h1>',
            page_width=width,
            page_height=height)
        ```
    """
    buf = lib.folio_html_to_buffer(
        ct.c_char_p(html.encode()),
        ct.c_double(page_width),
        ct.c_double(page_height),
    )
    data = _read_from_obj_buffer(buf)
    return BytesIO(data)


lib.folio_html_convert.argtypes = [ct.c_char_p, ct.c_double, ct.c_double]
lib.folio_html_convert.restype = ct.c_uint64


def html_convert(html: str, page_width: float, page_height: float) -> Document:
    """
    Converts an HTML string to a `Document` with custom page dimensions.

    The caller is responsible for closing the returned document.

    Args:
        html: the HTML content to render
        page_width: page width in points
        page_height: page height in points

    Returns:
        a new `Document` representing the converted HTML

    Example:
        ```python
        from folio_pdf import html_convert
        from folio_pdf.enums import PageSizes

        # Using the dimensions of a Letter page size
        width, height = PageSizes.LETTER.dimensions
        doc = html_convert(
            html='<h1>Folio PDF is awesome!</h1>',
            page_width=width,
            page_height=height)
        ```
    """
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


def parse_css_length(s: str, font_size: float, relative_to: float) -> float:
    """Parses a CSS length string and returns its value in points.

    Args:
        s: the CSS length expression (e.g., `"1in"`, `"16px"`, `"50%"`, `"2em"`)
        font_size: the current font size in points (used for `em`/`rem`)
        relative_to: the reference length in points (used for `%`)

    Returns:
        the parsed length in points


    Example:
        ```python
        pts = parse_css_length("1in", 12, 0) # 72.0
        em = parse_css_length("2em", 16,0) # 32.0
        pct = parse_css_length("50%", 12, 100) # 50.0
        ```
    """
    return lib.folio_html_parse_css_length(
        ct.c_char_p(s.encode()),
        ct.c_double(font_size),
        ct.c_double(relative_to),
    )


lib.folio_sign_pdf.argtypes = [
    ct.c_void_p,
    ct.c_int32,
    ct.c_int64,
]
lib.folio_sign_pdf.restype = ct.c_int64


def sign_pdf(pdf_data: bytes, opts: SignerOptions):
    buf = lib.folio_sign_pdf(
        ct.c_char_p(pdf_data), ct.c_int32(len(pdf_data)), opts._handle
    )
    return _read_from_obj_buffer(buf)


def redact_text(reader: PDFReader, targets: list[str], opts: RedactorOptions) -> bytes:
    """
    Redacts every occurrence of each target string in the given PDF reader.

    Args:
        reader: source PDF reader
        targets: literal strings to match and redact
        opts: redaction appearance options

    Returns:
        the redacted PDF bytes
    """
    CharPArray = ct.c_char_p * len(targets)

    lib.folio_redact_text.argtypes = [
        ct.c_uint64,
        CharPArray,
        ct.c_int32,
        ct.c_uint64,
    ]
    lib.folio_redact_text.restype = ct.c_uint64

    buf = lib.folio_redact_text(
        reader._handle, CharPArray(targets), ct.c_int32(len(targets)), opts._handle
    )
    return _read_from_obj_buffer(buf)


lib.folio_redact_pattern.argtypes = [ct.c_uint64, ct.c_char_p, ct.c_uint64]
lib.folio_redact_pattern.restype = ct.c_uint64


def redact_pattern(reader: PDFReader, pattern: str, opts: RedactorOptions):
    """
    Redacts every match of the given regular expression pattern.

    Args:
        reader: source PDF reader
        pattern: a regular expression used to locate redaction targets
        opts: redaction appearance options

    Returns:
        the redacted PDF bytes
    """
    buf = lib.folio_redact_pattern(
        reader._handle, ct.c_char_p(pattern.encode()), opts._handle
    )
    return _read_from_obj_buffer(buf)


def redact_regions(
    reader: PDFReader,
    pages: list[int],
    x1s: list[float],
    y1s: list[float],
    x2s: list[float],
    y2s: list[float],
    opts: RedactorOptions,
):  # TODO: Make this more python friendly
    """
    Redacts the explicit rectangular regions supplied by the caller.

    Args:
        reader: source PDF reader
        regions: list of page regions to black out
        opts: redaction appearance options

    Returns:
        the redacted PDF bytes
    """
    assert len(x1s) == len(y1s) == len(x2s) == len(y2s), (
        "The lists x1s,y1s,x2s & y2s must all be of the same length"
    )
    Int32Array = ct.c_int32 * len(pages)
    DoubleArray = ct.c_double * len(x1s)

    lib.folio_redact_regions.argtypes = [
        ct.c_uint64,
        Int32Array,
        DoubleArray,
        DoubleArray,
        DoubleArray,
        DoubleArray,
        ct.c_int32,
        ct.c_uint64,
    ]
    lib.folio_redact_regions.restype = ct.c_uint64

    buf = lib.folio_redact_regions(
        reader._handle,
        Int32Array(pages),
        DoubleArray(x1s),
        DoubleArray(y1s),
        DoubleArray(x2s),
        DoubleArray(y2s),
        ct.c_int32(len(x1s)),
        opts._handle,
    )
    return _read_from_obj_buffer(buf)
