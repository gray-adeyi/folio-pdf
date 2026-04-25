from folio_pdf.page import Page
import ctypes as ct
from io import BytesIO
from pathlib import Path
from folio_pdf.exceptions import DocumentException
from folio_pdf.enums import (
    PDFALevels,
    EncryptionAlgorithms,
    EncryptionPermissions,
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


class Document:
    def __init__(self, width: float, height: float):
        self._doc_handle = lib.folio_document_new(
            ct.c_double(width), ct.c_double(height)
        )

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
        return lib.folio_document_set_title(
            ct.c_uint64(self._doc_handle), ct.c_char_p(value.encode())
        )

    @_with_error_handling(DocumentException)
    def set_author(self, value: str):
        return lib.folio_document_author(
            ct.c_uint64(self._doc_handle), ct.c_char_p(value.encode())
        )

    @_with_error_handling(DocumentException)
    def set_margins(self, top: float, right: float, bottom: float, left: float):
        return lib.folio_document_set_margins(
            ct.c_uint64(self._doc_handle),
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )

    def add_page(self) -> Page:
        pg_ptr = lib.folio_document_add_page(ct.c_uint64(self._doc_handle))
        return Page._new_from_handle(pg_ptr)

    @_with_error_handling(DocumentException)
    def add(self, element):
        # TODO: Figure out what elements can be added to a page
        return lib.folio_document_add(self._doc_handle, element)

    @_with_error_handling(DocumentException)
    def save(self, destination: str | Path):
        _destination = destination
        if isinstance(_destination, Path):
            _destination = _destination.as_posix()
        return lib.folio_document_save(
            ct.c_uint64(self._doc_handle), ct.c_char_p(_destination.encode())
        )

    def to_buffer(self) -> BytesIO:
        buf = lib.folio_document_write_to_buffer(ct.c_uint64(self._doc_handle))
        size = lib.folio_buffer_len(buf)
        ptr = lib.folio_buffer_data(buf)
        data = ct.string_at(ptr, size)
        lib.folio_buffer_free(buf)
        return BytesIO(data)

    @_with_error_handling(DocumentException)
    def set_tagged(self, enabled: bool):
        return lib.folio_set_tagged(ct.c_uint64(self._doc_handle), ct.c_int32(enabled))

    @_with_error_handling(DocumentException)
    def set_pdfa(self, level: PDFALevels):
        return lib.folio_document_set_pdfa(
            ct.c_uint64(self._doc_handle), ct.c_int32(level.value)
        )

    @_with_error_handling(DocumentException)
    def set_encryption(
        self, user_password: str, owner_password: str, algorithm: EncryptionAlgorithms
    ):
        return lib.folio_document_set_encryption(
            ct.c_uint64(self._doc_handle),
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
            ct.c_uint64(self._doc_handle),
            ct.c_char_p(user_password.encode()),
            ct.c_char_p(owner_password.encode()),
            ct.c_int32(algorithm.value),
            ct.c_int32(permissions.value),
        )

    def to_bytes(self) -> bytes:
        buf = lib.folio_document_to_bytes(ct.c_uint64(self._doc_handle))
        size = lib.folio_buffer_len(buf)
        ptr = lib.folio_buffer_data(buf)
        data = ct.string_at(ptr, size)
        lib.folio_buffer_free(buf)
        return data

    @_with_error_handling(DocumentException)
    def validate_pdfa(self):
        return lib.folio_document_validate_pdfa(ct.c_uint64(self._doc_handle))

    @_with_error_handling(DocumentException)
    def set_auto_bookmarks(self, enabled: bool):
        return lib.folio_document_set_auto_bookmarks(
            ct.c_uint64(self._doc_handle), ct.c_int32(enabled)
        )

    def set_form(self, form): ...

    def set_header(self): ...

    def set_footer(self): ...

    def set_header_text(self): ...

    def set_footer_text(self): ...

    def set_watermark(self): ...

    def set_watermark_config(self): ...

    def add_outline(self): ...

    def add_outline_xyz(self): ...

    def add_named_dest(self): ...

    def set_viewer_preferences(self): ...

    def add_page_label(self): ...

    def remove_page(self): ...

    def add_absolute(self): ...

    def attach_file(self): ...

    def add_html(self): ...

    def add_html_with_options(self): ...

    def set_first_margins(self): ...

    def set_left_margins(self): ...

    def set_right_margins(self): ...

    def close(self):
        lib.folio_document_free(ct.c_uint64(self._doc_handle))

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()
