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
    """
    Represents a PDF font.

    Custom TrueType fonts can be loaded from a file path with the classmethod
    `load_from_ttf` or from raw bytes with `parse_from_ttf` classmethod.
    """

    _requires_close = True

    def __init__(self, font_family: StandardPDFFonts):
        self.__handle: int = lib.folio_font_standard(
            ct.c_char_p(font_family.value.encode())
        )

    @classmethod
    def load_from_ttf(cls, path: Path | str) -> "Font":
        """
        Loads a TrueType font from a file path. The returned font owns its handle
        and should be closed by calling `close` when no longer needed, or using it in
        a context manager with automatically closes it.

        Args:
            path: absolute path to the {@code .ttf} file

        Returns:
            a new `Font` backed by the loaded TrueType data
        """
        _path = path
        if isinstance(_path, Path):
            _path = _path.as_posix()
        obj: Font = cls.__new__(cls)
        cls.__handle = lib.folio_font_load_ttf(ct.c_char_p(_path.encode()))
        return obj

    @classmethod
    def parse_from_ttf(cls, data: bytes) -> "Font":
        """
        Parses a TrueType font from raw bytes. The returned font owns its handle
        and should be closed when no longer needed.

        Args:
            data: the raw `.ttf` file bytes

        Returns:
            a new `Font` backed by the parsed TrueType data
        """
        obj: Font = cls.__new__(cls)
        cls.__handle = lib.folio_font_parse_ttf(ct.c_char_p(data), len(data))
        return obj

    def close(self):
        lib.font_free(ct.c_int64(self.__handle))

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
