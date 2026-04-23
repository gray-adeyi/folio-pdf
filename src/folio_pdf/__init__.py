import ctypes.wintypes
from folio_pdf.document import Document
from io import BytesIO
from .core import lib
import ctypes
from pathlib import Path


lib.folio_html_to_pdf.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.folio_html_to_pdf.restype = ctypes.c_int32


def html_to_pdf(html: str, destination: str | Path):
    _destination = destination
    if isinstance(_destination, Path):
        _destination = _destination.as_posix()
    if not _destination.endswith("pdf"):
        _destination += ".pdf"
    return lib.folio_html_to_pdf(
        ctypes.c_char_p(html.encode()), ctypes.c_char_p(_destination.encode())
    )


lib.folio_html_to_buffer.argtypes = [ctypes.c_char_p, ctypes.c_double, ctypes.c_double]
lib.folio_html_to_buffer.restype = ctypes.c_int64

lib.folio_buffer_data.restype = ctypes.c_void_p


def html_to_buffer(html: str, page_width: float, page_height: float) -> BytesIO:
    buf = lib.folio_html_to_buffer(
        ctypes.c_char_p(html.encode()),
        ctypes.c_double(page_width),
        ctypes.c_double(page_height),
    )
    size = lib.folio_buffer_len(buf)
    ptr = lib.folio_buffer_data(buf)
    data = ctypes.string_at(ptr, size)
    lib.folio_buffer_free(buf)
    return BytesIO(data)


def html_convert(html: str, page_width: float, page_height: float) -> Document:
    doc_ptr = lib.folio_html_convert(
        ctypes.c_char_p(html.encode()),
        ctypes.c_double(page_width),
        ctypes.c_double(page_height),
    )
    return Document._new_from_ptr(doc_ptr)


lib.folio_html_parse_css_length.argtypes = [
    ctypes.c_char_p,
    ctypes.c_double,
    ctypes.c_double,
]
lib.folio_html_parse_css_length.restype = ctypes.c_double


def html_parse_css_length(s: str, font_size: float, relative_to: float) -> float:
    result: ctypes.c_double = lib.folio_html_parse_css_length(
        ctypes.c_char_p(s.encode()),
        ctypes.c_double(font_size),
        ctypes.c_double(relative_to),
    )
    return result.value

