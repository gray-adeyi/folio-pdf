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
    """
    Represents a section heading at a specified level (H1–H6).
    """

    _requires_close = True

    def __init__(self, text: str, level: HeadingLevels):
        """
        Creates a heading with the given text and level using the default font.

        Args:
            text: the heading text
            level: the {@link HeadingLevel} (H1–H6)

        Returns:
            a new `Heading`
        """
        self.__handle = lib.folio_heading_new(
            ct.c_char_p(text.encode()), ct.c_int32(level.value)
        )

    @classmethod
    def new_with_font(
        cls, text: str, level: HeadingLevels, font: Font, font_size: float
    ) -> "Heading":
        """
        Creates a heading with a custom font and font size.

        Args:
            text: the heading text
            level: the {@link HeadingLevel} (H1–H6)
            font: the font to use
            font_size: the font size in points

        Returns:
            a new `Heading`
        """
        obj = cls.__new__(cls)
        obj.__handle = lib.folio_heading_new_with_font(
            ct.c_char_p(text.encode()),
            ct.c_int32(level.value),
            font._handle,
            ct.c_double(font_size),
        )
        return obj

    @classmethod
    def new_embedded(cls, text: str, level: HeadingLevels, font: Font) -> "Heading":
        """
        Creates a heading that embeds the font subset in the PDF output.

        Args:
            text  the heading text
            level the {@link HeadingLevel} (H1–H6)
            font  the font to embed

        Returns:
            a new `Heading` with an embedded font
        """
        obj = cls.__new__(cls)
        obj.__handle = lib.folio_heading_new_embedded(
            ct.c_char_p(text.encode()), ct.c_int32(level.value), font._handle
        )
        return obj

    @_with_error_handling(HeadingException)
    def align(self, align: Alignments) -> "Heading":
        """
        Sets the text alignment for this heading.

        Args:
            align: the desired `Align` value

        Returns:
            this heading, for chaining
        """
        return lib.folio_heading_set_align(self._handle, ct.c_int32(align.value))

    @_with_error_handling(HeadingException)
    def runs(self, run_list: RunList) -> "Heading":
        """
        Replaces the heading text with styled runs from a `RunList`.

        Args:
            run_list: the run list containing styled text segments

        Returns:
            this heading, for chaining
        """
        return lib.folio_heading_set_runs(self._handle, run_list._handle)

    def close(self):
        lib.folio_heading_free(self._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
