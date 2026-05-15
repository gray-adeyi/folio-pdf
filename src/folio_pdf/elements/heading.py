"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Alignments, HeadingLevels
from folio_pdf.exceptions import HeadingException
from folio_pdf.font import Font
from folio_pdf.run_list import RunList

lib.folio_heading_new.argtypes = [ct.c_char_p, ct.c_int32]
lib.folio_heading_new.restype = ct.c_uint64

lib.folio_heading_new_with_font.argtypes = [
    ct.c_char_p,
    ct.c_int32,
    ct.c_uint64,
    ct.c_double,
]
lib.folio_heading_new_with_font.restype = ct.c_uint64

lib.folio_heading_new_embedded.argtypes = [
    ct.c_char_p,
    ct.c_int32,
    ct.c_uint64,
]
lib.folio_heading_new_embedded.restype = ct.c_uint64

lib.folio_heading_free.argtypes = [ct.c_uint64]
lib.folio_heading_free.restype = None

lib.folio_heading_set_align.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_heading_set_align.restype = ct.c_int32


class Heading(AbstractFolioObject):
    _requires_close = True

    def __init__(self, text: str, level: HeadingLevels):
        self.__handle = lib.folio_heading_new(
            ct.c_char_p(text.encode()), ct.c_int32(level.value)
        )

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    @classmethod
    def new_with_font(
        cls, text: str, level: HeadingLevels, font: Font, font_size: float
    ):
        obj = cls.__new__(cls)
        obj.__handle = lib.folio_heading_new_with_font(
            ct.c_char_p(text.encode()),
            ct.c_int32(level.value),
            font._handle,
            ct.c_double(font_size),
        )
        return obj

    @classmethod
    def new_embedded(cls, text: str, level: HeadingLevels, font: Font):
        obj = cls.__new__(cls)
        obj.__handle = lib.folio_heading_new_embedded(
            ct.c_char_p(text.encode()), ct.c_int32(level.value), font._handle
        )
        return obj

    def close(self):
        lib.folio_heading_free(self._handle)

    @_with_error_handling(HeadingException)
    def align(self, align: Alignments):
        return lib.folio_heading_set_align(self._handle, ct.c_int32(align.value))

    @_with_error_handling(HeadingException)
    def runs(self, run_list: RunList):
        return lib.folio_heading_set_runs(self._handle, run_list._handle)
