"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
from pathlib import Path

from folio_pdf.core import AbstractFolioObject, lib
from folio_pdf.enums import StandardPDFFonts

lib.folio_font_standard.argtypes = [ct.c_char_p]
lib.folio_font_standard.restype = ct.c_uint64

lib.folio_font_load_ttf.argtypes = [ct.c_char_p]
lib.folio_font_load_ttf.restype = ct.c_uint64

lib.folio_font_parse_ttf.argtypes = [ct.c_char_p, ct.c_int32]
lib.folio_font_parse_ttf.restype = ct.c_uint64

lib.folio_font_free.argtypes = [ct.c_uint64]
lib.folio_font_free.restype = None


class Font(AbstractFolioObject):
    _requires_close = True

    def __init__(self, font_family: StandardPDFFonts):
        self.__handle = lib.folio_font_standard(ct.c_char_p(font_family.value.encode()))

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    def close(self):
        # TODO: Find out if standard fonts don't require to be freed and it only
        # applies to font loaded from ttf or parsed from ttf
        lib.font_free(ct.c_int64(self.__handle))

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()

    @classmethod
    def load_from_ttf(cls, path: Path | str):
        _path = path
        if isinstance(_path, Path):
            _path = _path.as_posix()
        obj = cls.__new__(cls)
        cls.__handle = lib.folio_font_load_ttf(ct.c_char_p(_path.encode()))
        return obj

    @classmethod
    def parse_from_ttf(cls, data: bytes):
        obj = cls.__new__(cls)
        cls.__handle = lib.folio_font_parse_ttf(ct.c_char_p(data), len(data))
        return obj
