"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.color import Color
from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Alignments, Directions
from folio_pdf.exceptions import ParagraphException
from folio_pdf.font import Font

lib.folio_paragraph_new.argtypes = [
    ct.c_char_p,
    ct.c_uint64,
    ct.c_double,
]
lib.folio_paragraph_new.restype = ct.c_uint64

lib.folio_paragraph_new_embedded.argtypes = [ct.c_char_p, ct.c_uint64, ct.c_double]
lib.folio_paragraph_new_embedded.restype = ct.c_uint64

lib.folio_paragraph_free.argtypes = [ct.c_uint64]
lib.folio_paragraph_free.restype = None

lib.folio_paragraph_set_align.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_paragraph_set_align.restype = ct.c_int32

lib.folio_paragraph_set_leading.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_paragraph_set_leading.restype = ct.c_int32

lib.folio_paragraph_set_space_before.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_paragraph_set_space_before.restype = ct.c_int32

lib.folio_paragraph_set_space_after.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_paragraph_set_space_after.restype = ct.c_int32

lib.folio_paragraph_set_background.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_paragraph_set_background.restype = ct.c_int32

lib.folio_paragraph_set_first_indent.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_paragraph_set_first_indent.restype = ct.c_int32

lib.folio_paragraph_set_direction.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_paragraph_set_direction.restype = ct.c_int32

lib.folio_paragraph_set_orphans.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_paragraph_set_orphans.restype = ct.c_int32

lib.folio_paragraph_set_widows.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_paragraph_set_widows.restype = ct.c_int32

lib.folio_paragraph_set_ellipsis.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_paragraph_set_ellipsis.restype = ct.c_int32

lib.folio_paragraph_set_word_break.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_paragraph_set_word_break.restype = ct.c_int32

lib.folio_paragraph_set_hyphens.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_paragraph_set_hyphens.restype = ct.c_int32

lib.folio_paragraph_set_text_align_last.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_paragraph_set_text_align_last.restype = ct.c_int32

lib.folio_paragraph_add_run.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_paragraph_add_run.restype = ct.c_int32


class Paragraph(AbstractFolioObject):
    _requires_close = True

    def __init__(self, text: str, font: Font, font_size: float):
        self._paragraph_handle = lib.folio_paragraph_new(
            ct.c_char_p(text.encode()), font.handle, ct.c_double(font_size)
        )

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._paragraph_handle)

    @classmethod
    def new_embedded(cls, text: str, font: Font, font_size: float):
        obj = cls.__new__(cls)
        obj._paragraph_handle = lib.folio_paragraph_new_embedded(
            ct.c_char_p(text.encode()), font.handle, ct.c_double(font_size)
        )
        return obj

    def close(self):
        lib.folio_paragraph_free(self.handle)

    @_with_error_handling(ParagraphException)
    def align(self, align: Alignments):
        return lib.folio_paragraph_set_align(self.handle, ct.c_int32(align.value))

    @_with_error_handling(ParagraphException)
    def leading(self, leading: float):
        return lib.folio_paragraph_set_leading(self.handle, ct.c_double(leading))

    @_with_error_handling(ParagraphException)
    def space_before(self, pts: float):
        return lib.folio_paragraph_set_space_before(self.handle, ct.c_double(pts))

    @_with_error_handling(ParagraphException)
    def space_after(self, pts: float):
        return lib.folio_paragraph_set_space_after(self.handle, ct.c_double(pts))

    @_with_error_handling(ParagraphException)
    def background(self, color: Color):
        return lib.folio_paragraph_set_background(
            self.handle,
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(ParagraphException)
    def first_indent(self, pts: float):
        return lib.folio_paragraph_set_first_indent(self.handle, ct.c_double(pts))

    @_with_error_handling(ParagraphException)
    def direction(self, dir: Directions):
        return lib.folio_paragraph_set_direction(self.handle, ct.c_int32(dir.value))

    @_with_error_handling(ParagraphException)
    def orphans(self, n: int):
        return lib.folio_paragraph_set_orphans(self.handle, ct.c_int32(n))

    @_with_error_handling(ParagraphException)
    def widows(self, n: int):
        return lib.folio_paragraph_set_widows(self.handle, ct.c_int32(n))

    @_with_error_handling(ParagraphException)
    def ellipsis(self, enabled: bool):
        return lib.folio_paragraph_set_ellipsis(self.handle, ct.c_int32(enabled))

    @_with_error_handling(ParagraphException)
    def word_break(self, mode: str):
        return lib.folio_paragraph_set_word_break(
            self.handle,
            ct.c_char_p(mode.encode()),
        )

    @_with_error_handling(ParagraphException)
    def hyphens(self, mode: str):
        return lib.folio_paragraph_set_hyphens(self.handle, ct.c_char_p(mode.encode()))

    @_with_error_handling(ParagraphException)
    def text_align_last(self, align: Alignments):
        return lib.folio_paragraph_set_text_align_last(
            self.handle, ct.c_int32(align.value)
        )

    @_with_error_handling(ParagraphException)
    def add_run(
        self,
        text: str,
        font: Font,
        font_size: float,
        color: Color,
    ):
        return lib.folio_paragraph_add_run(
            self.handle,
            ct.c_char_p(text.encode()),
            font.handle,
            ct.c_double(font_size),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )
