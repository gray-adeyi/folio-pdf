from folio_pdf.document import Document
from io import BytesIO
from .core import lib
import ctypes as ct
from pathlib import Path


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
    result: ct.c_double = lib.folio_html_parse_css_length(
        ct.c_char_p(s.encode()),
        ct.c_double(font_size),
        ct.c_double(relative_to),
    )
    return ct.c_double(result).value
