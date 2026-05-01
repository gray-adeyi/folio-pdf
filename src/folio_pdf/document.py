from folio_pdf.object import AbstractFolioObject
from folio_pdf.outline import Outline
from folio_pdf.font import Font
from folio_pdf.forms import Form
from folio_pdf.page import Page
import ctypes as ct
from io import BytesIO
from pathlib import Path
from folio_pdf.exceptions import DocumentException
from folio_pdf.enums import (
    PDFALevels,
    EncryptionAlgorithms,
    EncryptionPermissions,
    Alignments,
)
from folio_pdf.core import lib, _with_error_handling


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

lib.folio_document_set_tagged.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_document_set_tagged.restype = ct.c_int32

lib.folio_document_set_pdfa.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_document_set_pdfa.restype = ct.c_int32


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
    def __init__(self, width: float, height: float):
        self._doc_handle = lib.folio_document_new(
            ct.c_double(width), ct.c_double(height)
        )

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._doc_handle)

    @classmethod
    def new_a4(cls):
        obj = cls.__new__(cls)
        cls._doc_handle = lib.folio_document_new_a4()
        return obj

    @classmethod
    def _new_from_handle(cls, doc_handle: int):
        obj = cls.__new__(cls)
        cls._doc_handle = doc_handle
        return obj

    @_with_error_handling(DocumentException)
    def set_title(self, value: str):
        return lib.folio_document_set_title(self.handle, ct.c_char_p(value.encode()))

    @_with_error_handling(DocumentException)
    def set_author(self, value: str):
        return lib.folio_document_author(self.handle, ct.c_char_p(value.encode()))

    @_with_error_handling(DocumentException)
    def set_margins(self, top: float, right: float, bottom: float, left: float):
        return lib.folio_document_set_margins(
            self.handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )

    def add_page(self) -> Page:
        pg_ptr = lib.folio_document_add_page(self.handle)
        return Page._new_from_handle(pg_ptr)

    @_with_error_handling(DocumentException)
    def add(self, element):
        # TODO: Figure out what elements can be added to a page
        return lib.folio_document_add(self.handle, element)

    @_with_error_handling(DocumentException)
    def save(self, destination: str | Path):
        _destination = destination
        if isinstance(_destination, Path):
            _destination = _destination.as_posix()
        return lib.folio_document_save(self.handle, ct.c_char_p(_destination.encode()))

    def to_buffer(self) -> BytesIO:
        buf = lib.folio_document_write_to_buffer(self.handle)
        size = lib.folio_buffer_len(buf)
        ptr = lib.folio_buffer_data(buf)
        data = ct.string_at(ptr, size)
        lib.folio_buffer_free(buf)
        return BytesIO(data)

    @_with_error_handling(DocumentException)
    def set_tagged(self, enabled: bool):
        return lib.folio_set_tagged(self.handle, ct.c_int32(enabled))

    @_with_error_handling(DocumentException)
    def set_pdfa(self, level: PDFALevels):
        return lib.folio_document_set_pdfa(self.handle, ct.c_int32(level.value))

    @_with_error_handling(DocumentException)
    def set_encryption(
        self, user_password: str, owner_password: str, algorithm: EncryptionAlgorithms
    ):
        return lib.folio_document_set_encryption(
            self.handle,
            ct.c_char_p(user_password.encode()),
            ct.c_char_p(owner_password.encode()),
            ct.c_int32(algorithm.value),
        )

    @_with_error_handling(DocumentException)
    def set_encryption_with_permissions(
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
        buf = lib.folio_document_to_bytes(self.handle)
        size = lib.folio_buffer_len(buf)
        ptr = lib.folio_buffer_data(buf)
        data = ct.string_at(ptr, size)
        lib.folio_buffer_free(buf)
        return data

    @_with_error_handling(DocumentException)
    def validate_pdfa(self):
        return lib.folio_document_validate_pdfa(self.handle)

    @_with_error_handling(DocumentException)
    def set_auto_bookmarks(self, enabled: bool):
        return lib.folio_document_set_auto_bookmarks(self.handle, ct.c_int32(enabled))

    def set_form(self, form: Form): ...

    def set_header(self): ...

    def set_footer(self): ...

    @_with_error_handling(DocumentException)
    def set_header_text(self, value: str, font: Font, size: float, align: Alignments):
        return lib.folio_document_set_header_text(
            self.handle,
            ct.c_char_p(value.encode()),
            ct.c_uint64(font.handle),
            ct.c_double(size),
            ct.c_int32(align.value),
        )

    @_with_error_handling(DocumentException)
    def set_footer_text(self, value: str, font: Font, size: float, align: Alignments):
        return lib.folio_document_set_footer_text(
            self.handle,
            ct.c_char_p(value.encode()),
            ct.c_uint64(font.handle),
            ct.c_double(size),
            ct.c_int32(align.value),
        )

    @_with_error_handling(DocumentException)
    def set_watermark(self, text: str):
        return lib.folio_document_set_watermark(self.handle, ct.c_char_p(text.encode()))

    @_with_error_handling(DocumentException)
    def set_watermark_config(
        self,
        text: str,
        font_size: float,
        color_r: float,
        color_g: float,
        color_b: float,
        angle: float,
        opacity: float,
    ):
        return lib.folio_document_set_watermark_config(
            self.handle,
            ct.c_char_p(text.encode()),
            ct.c_double(font_size),
            ct.c_double(color_r),
            ct.c_double(color_g),
            ct.c_double(color_b),
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
    def set_viewer_preferences(
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
    def add_absolute(self, element, x: float, y: float, width: float): ...

    def attach_file(self): ...

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
    def set_first_margins(self, top: float, right: float, bottom: float, left: float):
        return lib.folio_document_set_first_margins(
            self.handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )

    @_with_error_handling(DocumentException)
    def set_left_margins(self, top: float, right: float, bottom: float, left: float):
        return lib.folio_document_set_left_margins(
            self.handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )

    @_with_error_handling(DocumentException)
    def set_right_margins(self, top: float, right: float, bottom: float, left: float):
        return lib.folio_document_set_right_margins(
            self.handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )

    def close(self):
        lib.folio_document_free(self.handle)

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()
