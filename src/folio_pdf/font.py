"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
import sys
from pathlib import Path

from folio_pdf.core import AbstractFolioObject, lib
from folio_pdf.enums import StandardPDFFont

lib.folio_font_standard.argtypes = [ct.c_char_p]
lib.folio_font_standard.restype = ct.c_uint64

lib.folio_font_load_ttf.argtypes = [ct.c_char_p]
lib.folio_font_load_ttf.restype = ct.c_uint64

lib.folio_font_parse_ttf.argtypes = [ct.c_char_p, ct.c_int32]
lib.folio_font_parse_ttf.restype = ct.c_uint64

lib.folio_font_parse_for_language.argtypes = [ct.c_char_p, ct.c_int32, ct.c_char_p]
lib.folio_font_parse_for_language.restype = ct.c_uint64

lib.folio_font_free.argtypes = [ct.c_uint64]
lib.folio_font_free.restype = None

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class Font(AbstractFolioObject):
    """
    Represents a PDF font.

    Custom TrueType fonts can be loaded from a file path with the classmethod
    `load_from_ttf` or from raw bytes with `parse_from_ttf` classmethod.
    """

    _requires_close = True
    _binding_resource_free_fn = lib.font_free

    def __init__(self, font_family: StandardPDFFont):
        self._is_closed = False
        self.__handle: int = lib.folio_font_standard(
            ct.c_char_p(font_family.value.encode())
        )

    @classmethod
    def load_from_ttf(cls, path: Path | str) -> Self:
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
        obj = cls.__new__(cls)
        obj._is_closed = False
        obj.__handle = lib.folio_font_load_ttf(ct.c_char_p(_path.encode()))
        return obj

    @classmethod
    def parse_from_ttf(cls, data: bytes) -> Self:
        """
        Parses a TrueType font from raw bytes. The returned font owns its handle
        and should be closed when no longer needed.

        Args:
            data: the raw `.ttf` file bytes

        Returns:
            a new `Font` backed by the parsed TrueType data
        """
        obj = cls.__new__(cls)
        obj._is_closed = False
        obj.__handle = lib.folio_font_parse_ttf(ct.c_char_p(data), len(data))
        return obj

    @classmethod
    def parse_for_language(cls, data: bytes, language: str) -> Self:
        obj = cls.__new__(cls)
        obj._is_closed = False
        obj.__handle = lib.folio_font_parse_for_language(
            ct.c_char_p(data), len(data), ct.c_char_p(language.encode())
        )
        return obj

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
