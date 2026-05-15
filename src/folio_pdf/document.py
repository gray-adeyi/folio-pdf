"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Callable

from folio_pdf.color import Color
from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import (
    Alignments,
    EncryptionAlgorithms,
    EncryptionPermissions,
    PageSizes,
    PDFALevels,
)
from folio_pdf.exceptions import _NOT_IMPLEMENTED_ERROR, DocumentException
from folio_pdf.font import Font
from folio_pdf.forms import Form
from folio_pdf.outline import Outline
from folio_pdf.page import Page
from folio_pdf.write_options import WriteOptions

if TYPE_CHECKING:
    from folio_pdf.folio_pdf import Element

# def page_decorator_fn(page_index: int, total_pages: int,
# page_handle: ct.c_uint64,user_data: bytes) -> None: ...
PageDecoratorFn = Callable[[int, int, ct.c_uint64, bytes], None]

lib.folio_document_new.argtypes = [ct.c_double, ct.c_double]
lib.folio_document_new.restype = ct.c_uint64

lib.folio_document_new_letter.argtypes = []
lib.folio_document_new_letter.restype = ct.c_uint64

lib.folio_document_free.argtypes = [ct.c_uint64]
lib.folio_document_free.restype = None

lib.folio_document_set_title.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_document_set_title.restype = ct.c_int32

lib.folio_document_set_author.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_document_set_author.restype = ct.c_int32

lib.folio_document_set_margins.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_document_set_margins.restype = ct.c_int32


lib.folio_document_add_page.argtypes = [ct.c_uint64]
lib.folio_document_add_page.restype = ct.c_int32


lib.folio_document_page_count.argtypes = [ct.c_uint64]
lib.folio_document_page_count.restype = ct.c_int32

lib.folio_document_add.argtypes = [ct.c_uint64, ct.c_uint64]
lib.folio_document_add.restype = ct.c_int32

lib.folio_document_save.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_document_save.restype = ct.c_int32

lib.folio_document_write_to_buffer.argtypes = [ct.c_uint64]
lib.folio_document_write_to_buffer.restype = ct.c_uint64

lib.folio_document_save_with_options.argtypes = [ct.c_uint64, ct.c_char_p, ct.c_uint64]
lib.folio_document_save_with_options.restype = ct.c_int32

lib.folio_document_write_to_buffer_with_options.argtypes = [ct.c_uint64, ct.c_uint64]
lib.folio_document_write_to_buffer_with_options.restype = ct.c_int32

lib.folio_document_set_tagged.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_document_set_tagged.restype = ct.c_int32

lib.folio_document_set_pdfa.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_document_set_pdfa.restype = ct.c_int32

lib.folio_document_set_actual_text.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_document_set_actual_text.restype = ct.c_int32


lib.folio_document_set_encryption.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_char_p,
    ct.c_int32,
]
lib.folio_document_set_encryption.restype = ct.c_int32

lib.folio_document_set_encryption_with_permissions.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_char_p,
    ct.c_int32,
    ct.c_int32,
]
lib.folio_document_set_encryption_with_permissions.restype = ct.c_int32

lib.folio_document_to_bytes.argtypes = [ct.c_uint64]
lib.folio_document_to_bytes.restype = ct.c_uint64

lib.folio_document_validate_pdfa.argtypes = [ct.c_uint64]
lib.folio_document_validate_pdfa.restype = ct.c_int32

lib.folio_document_set_auto_bookmarks.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_document_set_auto_bookmarks.restype = ct.c_int32

lib.folio_document_set_form.argtypes = [ct.c_uint64, ct.c_uint64]
lib.folio_document_set_form.restype = ct.c_int32

lib.folio_document_set_header.argtypes = [ct.c_uint64, ct.c_void_p, ct.c_void_p]
lib.folio_document_set_header.restype = ct.c_int32

lib.folio_document_set_footer.argtypes = [ct.c_uint64, ct.c_void_p, ct.c_void_p]
lib.folio_document_set_footer.restype = ct.c_int32


lib.folio_document_set_header_text.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_uint64,
    ct.c_double,
    ct.c_int32,
]
lib.folio_document_set_header_text.restype = ct.c_int32

lib.folio_document_set_footer_text.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_uint64,
    ct.c_double,
    ct.c_int32,
]
lib.folio_document_set_footer_text.restype = ct.c_int32

lib.folio_document_set_watermark.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_document_set_watermark.restype = ct.c_int32

lib.folio_document_set_watermark_config.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_document_set_watermark_config.restype = ct.c_int32

lib.folio_document_add_outline.argtypes = [ct.c_uint64, ct.c_char_p, ct.c_int32]
lib.folio_document_add_outline.restype = ct.c_uint64

lib.folio_document_add_outline_xyz.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_int32,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_document_add_outline_xyz.restype = ct.c_uint64

lib.folio_outline_add_child.argtypes = [ct.c_uint64, ct.c_char_p, ct.c_int32]
lib.folio_outline_add_child.restype = ct.c_uint64

lib.folio_outline_add_child_xyz.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_int32,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_outline_add_child_xyz.restype = ct.c_uint64


lib.folio_document_add_named_dest.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_int32,
    ct.c_char_p,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_document_add_named_dest.restype = ct.c_int32


lib.folio_document_set_viewer_preferences.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_char_p,
    ct.c_int32,
    ct.c_int32,
    ct.c_int32,
    ct.c_int32,
    ct.c_int32,
    ct.c_int32,
]
lib.folio_document_set_viewer_preferences.restype = ct.c_int32


lib.folio_document_add_page_label.argtypes = [
    ct.c_uint64,
    ct.c_int32,
    ct.c_char_p,
    ct.c_char_p,
    ct.c_int32,
]
lib.folio_document_add_page_label.restype = ct.c_int32

lib.folio_document_remove_page.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_document_remove_page.restype = ct.c_int32

lib.folio_document_add_absolute.argtypes = [
    ct.c_uint64,
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_document_add_absolute.restype = ct.c_int32

lib.folio_document_attach_file.argtypes = [
    ct.c_uint64,
    ct.c_void_p,
    ct.c_int32,
    ct.c_char_p,
    ct.c_char_p,
    ct.c_char_p,
    ct.c_char_p,
]
lib.folio_document_attach_file.restype = ct.c_int32

lib.folio_document_add_html.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_document_add_html.restype = ct.c_int32

lib.folio_document_add_html_with_options.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_char_p,
    ct.c_char_p,
]
lib.folio_document_add_html_with_options.restype = ct.c_int32

lib.folio_document_set_first_margins.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_document_set_first_margins.restype = ct.c_int32

lib.folio_document_set_left_margins.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_document_set_left_margins.restype = ct.c_int32

lib.folio_document_set_right_margins.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_document_set_right_margins.restype = ct.c_int32


class Document(AbstractFolioObject):
    """Document is the top-level API for building a PDF."""

    _requires_close = True

    def __init__(self, width: float, height: float):
        self._doc_handle = lib.folio_document_new(
            ct.c_double(width), ct.c_double(height)
        )

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._doc_handle)

    @classmethod
    def new_with_size(cls, size: PageSizes) -> "Document":
        """Creates a new PDF document with A4 dimensions"""
        match size:
            case PageSizes.A4:
                obj = cls.__new__(cls)
                cls._doc_handle = lib.folio_document_new_a4()
                return obj
            case PageSizes.LETTER:
                return cls(612, 792)
            case PageSizes.LEGAL:
                return cls(612, 1008)
            case PageSizes.TABLOID:
                return cls(792, 1224)

    @classmethod
    def _new_from_handle(cls, doc_handle: int) -> "Document":
        obj = cls.__new__(cls)
        cls._doc_handle = doc_handle
        return obj

    @_with_error_handling(DocumentException)
    def title(self, value: str):
        """Sets the title of the PDF document"""
        return lib.folio_document_set_title(self.handle, ct.c_char_p(value.encode()))

    @_with_error_handling(DocumentException)
    def author(self, value: str):
        """Sets the author of the PDF document"""
        return lib.folio_document_author(self.handle, ct.c_char_p(value.encode()))

    @_with_error_handling(DocumentException)
    def margins(self, top: float, right: float, bottom: float, left: float):
        """
        It sets the page margins used by the layout engine (in PDF points).

        Default is 72pt (1 inch) on all sides.

        Args:
            top: the margin for the top of the page.
            right: the margin for the right side of the page.
            bottom: the margin for the bottom of the page.
            left: the margin for the left side of the page.
        """
        return lib.folio_document_set_margins(
            self.handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )

    def add_page(self) -> Page:
        """Adds a blank page to the document and returns it."""
        pg_ptr = lib.folio_document_add_page(self.handle)
        return Page._new_from_handle(pg_ptr)

    @property
    def page_count(self) -> int:
        """Returns the number of pages in the document."""
        return lib.folio_document_page_count(self.handle)

    @_with_error_handling(DocumentException)
    def add(self, element: "Element"):
        """Appends a layout element (e.g. Paragraph) to the document.

        Elements are laid out automatically with word wrapping and page breaks
        when `save`/`to_bytes`/`write_to_buffer` is called.
        """
        return lib.folio_document_add(self.handle, element.handle)

    @_with_error_handling(DocumentException)
    def save(self, destination: str | Path):
        """Writes the document to a file at the given path"""
        _destination = destination
        if isinstance(_destination, Path):
            _destination = _destination.as_posix()
        return lib.folio_document_save(self.handle, ct.c_char_p(_destination.encode()))

    def to_buffer(self) -> BytesIO:
        buf = lib.folio_document_write_to_buffer(self.handle)
        data = self._read_from_obj_buffer(buf)
        return BytesIO(data)

    @_with_error_handling(DocumentException)
    def save_with_options(self, destination: str | Path, opts: WriteOptions):
        _destination = destination
        if isinstance(_destination, Path):
            _destination = _destination.as_posix()
        return lib.folio_document_save_with_options(
            self.handle, ct.c_char_p(_destination.encode()), opts.handle
        )

    def to_buffer_with_options(self, opts: WriteOptions) -> BytesIO:
        buf = lib.folio_document_write_to_buffer_with_options(self.handle, opts.handle)
        data = self._read_from_obj_buffer(buf)
        return BytesIO(data)

    @_with_error_handling(DocumentException)
    def tagged(self, enabled: bool):
        """
        Enables tagged PDF output (PDF/UA foundation).

        When enabled, the document includes a structure tree with semantic tags
        (P, H1-H6, Table, Figure, etc.) and marked content operators in the
        content streams. This enables screen readers, text extraction, and
        accessibility compliance (Section 508, EN 301 549).
        """
        return lib.folio_set_tagged(self.handle, ct.c_int32(enabled))

    @_with_error_handling(DocumentException)
    def pdfa(self, level: PDFALevels):
        return lib.folio_document_set_pdfa(self.handle, ct.c_int32(level.value))

    @_with_error_handling(DocumentException)
    def actual_text(self, enabled: bool):
        """
        It controls whether the document wraps shaped Arabic words in
        ISO 32000-2 §14.9.4 /Span /ActualText marked-content sequences. When
        enabled (the default), copy/paste and accessibility consumers recover the
        original Unicode codepoints rather than the Arabic Presentation Forms-B
        substitutions emitted by the shaper. Disabling shaves a few dozen bytes
        per shaped Arabic word and is appropriate for size-sensitive documents
        that do not need text round-tripping.
        """
        return lib.folio_document_set_actual_text(self.handle, ct.c_int32(enabled))

    @_with_error_handling(DocumentException)
    def encryption(
        self, user_password: str, owner_password: str, algorithm: EncryptionAlgorithms
    ):
        return lib.folio_document_set_encryption(
            self.handle,
            ct.c_char_p(user_password.encode()),
            ct.c_char_p(owner_password.encode()),
            ct.c_int32(algorithm.value),
        )

    @_with_error_handling(DocumentException)
    def encryption_with_permissions(
        self,
        user_password: str,
        owner_password: str,
        algorithm: EncryptionAlgorithms,
        permissions: EncryptionPermissions,
    ):
        return lib.folio_document_set_encryption_with_permissions(
            self.handle,
            ct.c_char_p(user_password.encode()),
            ct.c_char_p(owner_password.encode()),
            ct.c_int32(algorithm.value),
            ct.c_int32(permissions.value),
        )

    def to_bytes(self) -> bytes:
        """Serializes the complete PDF document and returns the raw bytes."""
        buf = lib.folio_document_to_bytes(self.handle)
        return self._read_from_obj_buffer(buf)

    @_with_error_handling(DocumentException)
    def validate_pdfa(self):
        return lib.folio_document_validate_pdfa(self.handle)

    @_with_error_handling(DocumentException)
    def auto_bookmarks(self, enabled: bool):
        """
        It Enables automatic bookmark/outline generation from
        layout headings (H1-H6). When enabled, each Heading element in the
        document flow produces a bookmark entry. Headings are nested by level:
        H2 under H1, H3 under H2, etc.
        """
        return lib.folio_document_set_auto_bookmarks(self.handle, ct.c_int32(enabled))

    @_with_error_handling(DocumentException)
    def form(self, form: Form):
        return lib.folio_document_set_form(self.handle, form.handle)

    @_with_error_handling(DocumentException)
    def header_text(self, value: str, font: Font, size: float, align: Alignments):
        return lib.folio_document_set_header_text(
            self.handle,
            ct.c_char_p(value.encode()),
            font.handle,
            ct.c_double(size),
            ct.c_int32(align.value),
        )

    @_with_error_handling(DocumentException)
    def footer_text(self, value: str, font: Font, size: float, align: Alignments):
        return lib.folio_document_set_footer_text(
            self.handle,
            ct.c_char_p(value.encode()),
            font.handle,
            ct.c_double(size),
            ct.c_int32(align.value),
        )

    @_with_error_handling(DocumentException)
    def watermark(self, text: str):
        return lib.folio_document_set_watermark(self.handle, ct.c_char_p(text.encode()))

    @_with_error_handling(DocumentException)
    def watermark_config(
        self,
        text: str,
        font_size: float,
        color: Color,
        angle: float,
        opacity: float,
    ):
        return lib.folio_document_set_watermark_config(
            self.handle,
            ct.c_char_p(text.encode()),
            ct.c_double(font_size),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
            ct.c_double(angle),
            ct.c_double(opacity),
        )

    def add_outline(self, title: str, page_index: int) -> Outline:
        outline_handle = lib.folio_document_add_outline(
            self.handle,
            ct.c_char_p(title.encode()),
            ct.c_int32(page_index),
        )
        return Outline._new_from_handle(outline_handle)

    def add_outline_xyz(
        self, title: str, page_index: int, left: float, top: float, zoom: float
    ) -> Outline:
        outline_handle = lib.folio_document_add_outline_xyz(
            self.handle,
            ct.c_char_p(title.encode()),
            ct.c_int32(page_index),
            ct.c_double(left),
            ct.c_double(top),
            ct.c_double(zoom),
        )
        return Outline._new_from_handle(outline_handle)

    @_with_error_handling(DocumentException)
    def add_named_dest(
        self,
        name: str,
        page_index: int,
        fit_type: str,
        top: float,
        left: float,
        zoom: float,
    ):
        return lib.folio_document_add_named_dest(
            self.handle,
            ct.c_char_p(name.encode()),
            ct.c_int32(page_index),
            ct.c_char_p(fit_type.encode()),
            ct.c_double(top),
            ct.c_double(left),
            ct.c_double(zoom),
        )

    @_with_error_handling(DocumentException)
    def viewer_preferences(
        self,
        page_layout: str,
        page_mode: str,
        hide_toolbar: bool,
        hide_menubar: bool,
        hide_window_ui: bool,
        fit_window: bool,
        center_window: bool,
        display_doc_title: bool,
    ):
        return lib.folio_document_set_viewer_preferences(
            self.handle,
            ct.c_char_p(page_layout.encode()),
            ct.c_char_p(page_mode.encode()),
            ct.c_int32(hide_toolbar),
            ct.c_int32(hide_menubar),
            ct.c_int32(hide_window_ui),
            ct.c_int32(fit_window),
            ct.c_int32(center_window),
            ct.c_int32(display_doc_title),
        )

    @_with_error_handling(DocumentException)
    def add_page_label(self, page_index: int, style: str, prefix: str, start: int):
        return lib.folio_document_add_page_label(
            self.handle,
            ct.c_int32(page_index),
            ct.c_char_p(style.encode()),
            ct.c_char_p(prefix.encode()),
            ct.c_int32(start),
        )

    @_with_error_handling(DocumentException)
    def remove_page(self, index: int):
        return lib.folio_document_remove_page(self.handle, ct.c_int32(index))

    @_with_error_handling(DocumentException)
    def add_absolute(self, element: "Element", x: float, y: float, width: float): ...

    def attach_file(self):
        raise _NOT_IMPLEMENTED_ERROR

    @_with_error_handling(DocumentException)
    def add_html(self, html: str):
        return lib.folio_document_add_html(self.handle, ct.c_char_p(html.encode()))

    @_with_error_handling(DocumentException)
    def add_html_with_options(
        self,
        html: str,
        default_font_size: float,
        page_width: float,
        page_height: float,
        base_path: str,
        fallback_font_path: str,
    ):
        return lib.folio_document_add_html_with_options(
            self.handle,
            ct.c_char_p(html.encode()),
            ct.c_double(default_font_size),
            ct.c_double(page_width),
            ct.c_double(page_height),
            ct.c_char_p(base_path.encode()),
            ct.c_char_p(fallback_font_path.encode()),
        )

    @_with_error_handling(DocumentException)
    def first_margins(self, top: float, right: float, bottom: float, left: float):
        return lib.folio_document_set_first_margins(
            self.handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )

    @_with_error_handling(DocumentException)
    def left_margins(self, top: float, right: float, bottom: float, left: float):
        return lib.folio_document_set_left_margins(
            self.handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )

    @_with_error_handling(DocumentException)
    def right_margins(self, top: float, right: float, bottom: float, left: float):
        return lib.folio_document_set_right_margins(
            self.handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )

    def close(self):
        lib.folio_document_free(self.handle)
