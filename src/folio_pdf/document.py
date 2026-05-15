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
        self.__handle = lib.folio_document_new(ct.c_double(width), ct.c_double(height))

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    @classmethod
    def new_with_size(cls, size: PageSizes) -> "Document":
        """Creates a new PDF document with page size provided"""
        match size:
            case PageSizes.A4:
                obj = cls.__new__(cls)
                cls.__handle = lib.folio_document_new_a4()
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
        cls.__handle = doc_handle
        return obj

    @_with_error_handling(DocumentException)
    def title(self, value: str) -> "Document":
        """Sets the title of the PDF document

        Args:
            value: what to set the title to

        Returns:
            this document, for chaining
        """
        return lib.folio_document_set_title(self._handle, ct.c_char_p(value.encode()))

    @_with_error_handling(DocumentException)
    def author(self, value: str) -> "Document":
        """Sets the author of the PDF document

        Args:
            value: what to set the author to

        Returns:
            this document, for chaining
        """
        return lib.folio_document_author(self._handle, ct.c_char_p(value.encode()))

    @_with_error_handling(DocumentException)
    def margins(self, top: float, right: float, bottom: float, left: float):
        """
        It sets the page margins used by the layout engine (in PDF points).

        Default is 72pt (1 inch) on all sides.

        Args:
            top: the margin for the top of the page in points
            right: the margin for the right side of the page in points
            bottom: the margin for the bottom of the page in points
            left: the margin for the left side of the page in points

        Returns:
            this document, for chaining
        """
        return lib.folio_document_set_margins(
            self._handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )

    def add_page(self) -> Page:
        """Adds a blank page to the document

        Returns:
            the blank page added to the document
        """
        pg_ptr = lib.folio_document_add_page(self._handle)
        return Page._new_from_handle(pg_ptr)

    @property
    def page_count(self) -> int:
        """Returns the number of pages in the document."""
        return lib.folio_document_page_count(self._handle)

    @_with_error_handling(DocumentException)
    def add(self, element: "Element"):
        """Appends a layout element (e.g. Paragraph) to the document.

        Elements are laid out automatically with word wrapping and page breaks
        when `save`/`to_bytes`/`write_to_buffer` is called.

        Args:
            element: the layout element to add to the document

        Returns:
            this document, for chaining
        """
        return lib.folio_document_add(self._handle, element._handle)

    @_with_error_handling(DocumentException)
    def save(self, destination: str | Path):
        """Writes the document to a file at the given path

        Returns:
            this document, for chaining
        """
        _destination = destination
        if isinstance(_destination, Path):
            _destination = _destination.as_posix()
        return lib.folio_document_save(self._handle, ct.c_char_p(_destination.encode()))

    def to_buffer(self) -> BytesIO:
        buf = lib.folio_document_write_to_buffer(self._handle)
        data = self._read_from_obj_buffer(buf)
        return BytesIO(data)

    @_with_error_handling(DocumentException)
    def save_with_options(self, destination: str | Path, opts: WriteOptions):
        _destination = destination
        if isinstance(_destination, Path):
            _destination = _destination.as_posix()
        return lib.folio_document_save_with_options(
            self._handle, ct.c_char_p(_destination.encode()), opts._handle
        )

    def to_buffer_with_options(self, opts: WriteOptions) -> BytesIO:
        buf = lib.folio_document_write_to_buffer_with_options(
            self._handle, opts._handle
        )
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
        return lib.folio_set_tagged(self._handle, ct.c_int32(enabled))

    @_with_error_handling(DocumentException)
    def pdfa(self, level: PDFALevels):
        return lib.folio_document_set_pdfa(self._handle, ct.c_int32(level.value))

    @_with_error_handling(DocumentException)
    def actual_text(self, enabled: bool):
        """
        Toggles emission of `/ActualText` entries in the marked-content
        sequences of tagged PDFs (ISO 32000-1 §14.9.4).

        `/ActualText` provides assistive technologies with the
        canonical Unicode text for a marked region; turn it off to reduce file
        size when accessibility is not required (or when the visible glyphs
        already match the logical text).

        Args:
            enabled: `True` to emit `/ActualText` entries

        Returns:
            this document, for chaining
        """
        return lib.folio_document_set_actual_text(self._handle, ct.c_int32(enabled))

    @_with_error_handling(DocumentException)
    def encryption(
        self, user_password: str, owner_password: str, algorithm: EncryptionAlgorithms
    ):
        """
        Applies password-based encryption to the output PDF.

        Args:
            user_password: password required to open the document
            owner_password: password granting full owner permissions
            algorithm: the {@link EncryptionAlgorithm} to use

        Returns:
            this document, for chaining
        """
        return lib.folio_document_set_encryption(
            self._handle,
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
        """
        Applies password-based encryption with granular permission flags.

        Args:
            user_password: password required to open the document
            owner_password: password granting full owner permissions
            algorithm: the `EncryptionAlgorithms` variant to use
            permissions: bitwise OR of {@link PdfPermission} flags

        Returns:
            this document, for chaining
        """
        return lib.folio_document_set_encryption_with_permissions(
            self._handle,
            ct.c_char_p(user_password.encode()),
            ct.c_char_p(owner_password.encode()),
            ct.c_int32(algorithm.value),
            ct.c_int32(permissions.value),
        )

    def to_bytes(self) -> bytes:
        """Serializes the complete PDF document and returns the raw bytes."""
        buf = lib.folio_document_to_bytes(self._handle)
        return self._read_from_obj_buffer(buf)

    @_with_error_handling(DocumentException)
    def validate_pdfa(self):
        """Validates the document against its configured PDF/A conformance level.

        Returns:
            this document, for chaining
        """
        return lib.folio_document_validate_pdfa(self._handle)

    @_with_error_handling(DocumentException)
    def auto_bookmarks(self, enabled: bool):
        """
        Enables or disables automatic bookmark generation from headings.

        Args:
            enabled: `True` to generate bookmarks automatically

        Returns:
            this document, for chaining
        """
        return lib.folio_document_set_auto_bookmarks(self._handle, ct.c_int32(enabled))

    @_with_error_handling(DocumentException)
    def form(self, form: Form) -> "Document":
        """
        Attaches an interactive {@link Form} to this document.

        Args:
            form: the form to attach

        Returns:
            this document, for chaining
        """
        return lib.folio_document_set_form(self._handle, form._handle)

    @_with_error_handling(DocumentException)
    def header_text(
        self, value: str, font: Font, size: float, align: Alignments
    ) -> "Document":
        """Sets a simple text header rendered on every page.

        The text may contain `{page}` and `{pages}` placeholders.

        Args:
            value: the header text
            font: the font to use
            size: font size in points
            align: horizontal alignment

        Returns:
            this document, for chaining
        """
        return lib.folio_document_set_header_text(
            self._handle,
            ct.c_char_p(value.encode()),
            font._handle,
            ct.c_double(size),
            ct.c_int32(align.value),
        )

    @_with_error_handling(DocumentException)
    def footer_text(
        self, value: str, font: Font, size: float, align: Alignments
    ) -> "Document":
        """Sets a simple text footer rendered on every page.

        The text may contain `{page}` and `{pages}` placeholders.

        Args:
            value: the header text
            font: the font to use
            size: font size in points
            align: horizontal alignment

        Returns:
            this document, for chaining
        """
        return lib.folio_document_set_footer_text(
            self._handle,
            ct.c_char_p(value.encode()),
            font._handle,
            ct.c_double(size),
            ct.c_int32(align.value),
        )

    @_with_error_handling(DocumentException)
    def watermark(self, text: str) -> "Document":
        """Adds a simple text watermark to every page using default styling.

        Args:
            text: the wateramark text

        Returns:
            this document, for chaining
        """
        return lib.folio_document_set_watermark(
            self._handle, ct.c_char_p(text.encode())
        )

    @_with_error_handling(DocumentException)
    def watermark_config(
        self,
        text: str,
        font_size: float,
        color: Color,
        angle: float,
        opacity: float,
    ) -> "Document":
        """Adds a text watermark to every page with custom font size, color,
        angle, and opacity.

        Args:
            text: the wateramark text
            font_size: font size in points
            color: text color
            angle: rotation angle in degrees
            opacity: opacity in the range `0.0 - 1.0`

        Returns:
            this document, for chaining
        """
        return lib.folio_document_set_watermark_config(
            self._handle,
            ct.c_char_p(text.encode()),
            ct.c_double(font_size),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
            ct.c_double(angle),
            ct.c_double(opacity),
        )

    def add_outline(self, title: str, page_index: int) -> Outline:
        """Adds a top-level PDF outline (bookmark) entry pointing to a page.

        Args:
            title: the bookmark label
            page_index: zero-based target page index

        Returns:
            the outline object representing the added outline
        """
        outline_handle = lib.folio_document_add_outline(
            self._handle,
            ct.c_char_p(title.encode()),
            ct.c_int32(page_index),
        )
        return Outline._new_from_handle(outline_handle)

    def add_outline_xyz(
        self, title: str, page_index: int, left: float, top: float, zoom: float
    ) -> Outline:
        """Adds a top-level PDF outline entry with an explicit XYZ destination.

        Args:
            title: the bookmark label
            page_index: zero-based target page index
            left: left coordinate of the destination view
            top: top coordinate of the destination view
            zoom: zoom factor at the destination

        Returns:
            the outline object representing the added outline
        """
        outline_handle = lib.folio_document_add_outline_xyz(
            self._handle,
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
    ) -> "Document":
        """Adds a named destination that can be targeted by internal links.

        Args:
            name: unique destination name
            page_index: zero-based target page index
            fit_type: PDF fit type string (e.g., {@code "XYZ"})
            top: top coordinate
            left: left coordinate
            zoom: zoom factor

        Returns:
            this document, for chaining
        """
        return lib.folio_document_add_named_dest(
            self._handle,
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
    ) -> "Document":
        """
        Configures PDF viewer preferences for how the document is displayed when opened.

        Args:
            page_layout: PDF page layout name (e.g., {@code "SinglePage"})
            page_mode: PDF page mode name (e.g., {@code "UseOutlines"})
            hide_toolbar: whether to hide the viewer toolbar
            hide_menubar: whether to hide the viewer menu bar
            hide_window_ui: whether to hide the viewer window UI
            fit_window: whether to fit the window to the first page
            center_window: whether to center the window on screen
            display_doc_title: whether to display the document title in the title bar

        Returns:
            this document, for chaining
        """
        return lib.folio_document_set_viewer_preferences(
            self._handle,
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
    def add_page_label(
        self, page_index: int, style: str, prefix: str, start: int
    ) -> "Document":
        """
        Adds a page label range starting at the given page index.

        Args:
            page_index: zero-based page index where the label range starts
            style: numbering style (e.g., `"D"` for decimal, `"r"` for lowercase roman)
            prefix: optional text prefix for each label
            start: the numeric start value for this range

        Returns:
            this document, for chaining
        """
        return lib.folio_document_add_page_label(
            self._handle,
            ct.c_int32(page_index),
            ct.c_char_p(style.encode()),
            ct.c_char_p(prefix.encode()),
            ct.c_int32(start),
        )

    @_with_error_handling(DocumentException)
    def remove_page(self, index: int) -> "Document":
        """
        Removes the page at the given zero-based index from the document.

        Args:
            index: zero-based page index to remove

        Returns:
            this document, for chaining
        """
        return lib.folio_document_remove_page(self._handle, ct.c_int32(index))

    @_with_error_handling(DocumentException)
    def add_absolute(
        self, element: "Element", x: float, y: float, width: float
    ) -> "Document":
        """Adds an element handle at an absolute position on the current page.

        Args:
            element: the native element handle
            x: x coordinate in points from the left edge
            y: y coordinate in points from the top edge
            width: available width in points

        Returns:
            this document, for chaining
        """
        return lib.folio_document_add_absolute(
            self._handle,
            element._handle,
            ct.c_double(x),
            ct.c_double(y),
            ct.c_double(width),
        )

    def attach_file(
        self,
        data: bytes,
        file_name: str,
        mime_type: str,
        description: str,
        af_relationship: str,
    ) -> "Document":
        """
        Attaches a file as an embedded file stream in the PDF.

        Args:
            data: the raw file bytes
            file_name: the name to assign to the attachment
            mime_type: MIME type of the attachment (e.g., `"text/plain"`)
            description: human-readable description of the attachment
            af_relationship: PDF AF relationship value (e.g., `"Data"`)

        Returns:
            this document, for chaining
        """
        return lib.folio_document_attach_file(
            self._handle,
            ct.c_char_p(data),
            ct.c_int32(len(data)),
            ct.c_char_p(file_name.encode()),
            ct.c_char_p(mime_type.encode()),
            ct.c_char_p(description.encode()),
            ct.c_char_p(af_relationship.encode()),
        )

    @_with_error_handling(DocumentException)
    def add_html(self, html: str) -> "Document":
        """
        Appends an HTML fragment to the document using default rendering options.

        Args:
            html: the HTML content to render

        Returns:
            this document, for chaining
        """
        return lib.folio_document_add_html(self._handle, ct.c_char_p(html.encode()))

    @_with_error_handling(DocumentException)
    def add_html_with_options(
        self,
        html: str,
        default_font_size: float,
        page_width: float,
        page_height: float,
        base_path: str,
        fallback_font_path: str,
    ) -> "Document":
        """
        Appends an HTML fragment with explicit rendering options.

        Args:
            html: the HTML content to render
            default_font_size: base font size in points
            page_width: page width in points used for layout
            page_height: page height in points used for layout
            base_path: base path for resolving relative resource URLs
            fallback_font_path: path to a fallback font file

        Returns:
            this document, for chaining
        """
        return lib.folio_document_add_html_with_options(
            self._handle,
            ct.c_char_p(html.encode()),
            ct.c_double(default_font_size),
            ct.c_double(page_width),
            ct.c_double(page_height),
            ct.c_char_p(base_path.encode()),
            ct.c_char_p(fallback_font_path.encode()),
        )

    @_with_error_handling(DocumentException)
    def first_margins(
        self, top: float, right: float, bottom: float, left: float
    ) -> "Document":
        """
        Sets custom margins for the first page of the document.

        Args:
            top: top margin in points
            right: right margin in points
            bottom: bottom margin in points
            left: left margin in points

        Returns:
            this document, for chaining
        """
        return lib.folio_document_set_first_margins(
            self._handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )

    @_with_error_handling(DocumentException)
    def left_margins(
        self, top: float, right: float, bottom: float, left: float
    ) -> "Document":
        """
        Sets custom margins for left (even-numbered) pages in a duplex layout.

        Args:
            top: top margin in points
            right: right margin in points
            bottom: bottom margin in points
            left: left margin in points

        Returns:
            this document, for chaining
        """
        return lib.folio_document_set_left_margins(
            self._handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )

    @_with_error_handling(DocumentException)
    def right_margins(
        self, top: float, right: float, bottom: float, left: float
    ) -> "Document":
        """
        Sets custom margins for right (odd-numbered) pages in a duplex layout.

        Args:
            top: top margin in points
            right: right margin in points
            bottom: bottom margin in points
            left: left margin in points

        Returns:
            this document, for chaining
        """
        return lib.folio_document_set_right_margins(
            self._handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )

    def close(self):
        lib.folio_document_free(self._handle)
