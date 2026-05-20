"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

from operator import pos

import ctypes as ct

from folio_pdf.color import Color
from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Alignments
from folio_pdf.exceptions import TabbedLineException
from folio_pdf.font import Font

lib.folio_tabbed_line_free.argtypes = [ct.c_uint64]
lib.folio_tabbed_line_free.restype = None


lib.folio_tabbed_line_set_color.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_tabbed_line_set_color.restype = ct.c_int32

lib.folio_tabbed_line_set_leading.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_tabbed_line_set_leading.restype = ct.c_int32


class TabbedLine(AbstractFolioObject):
    """
    A line of text divided into tab-stop segments, useful for layouts like
    tables of contents or form fields where text must align at
    specific horizontal positions.
    """

    _requires_close = True

    def __init__(
        self,
        font: Font,
        font_size: float,
        positions: list[float],
        aligns: list[Alignments],
        leaders: list[int],
    ):
        """
        Creates a tabbed line using a standard (non-embedded) font.

        Args:
            font: the font for all segments
            fontSize: the font size in points
            positions: the tab-stop positions in points from the left margin
            aligns: the alignment of text at each tab stop
            leaders: leader style codes for each segment (0 = none)

        Returns:
            a new `TabbedLine` instance
        """
        DoubleArray = ct.c_double * len(positions)
        Int32Array = ct.c_int32 * len(aligns)
        lib.folio_tabbed_line_new.argtypes = [
            ct.c_uint64,
            ct.c_double,
            DoubleArray,
            Int32Array,
            Int32Array,
            ct.c_int32,
        ]
        lib.folio_tabbed_line_new.restype = ct.c_uint64
        self.__handle = lib.folio_tabbed_line_new(
            font._handle,
            ct.c_double(font_size),
            DoubleArray(positions),
            Int32Array([align.value for align in aligns]),
            Int32Array(leaders),
            ct.c_int32(len(leaders)),
        )

    @classmethod
    def new_embedded(
        cls,
        font: Font,
        font_size: float,
        positions: list[float],
        aligns: list[Alignments],
        leaders: list[int],
    ) -> "TabbedLine":
        """
        Creates a tabbed line using an embedded (subset) font.

        Args:
            font: the embedded font for all segments
            font_size: the font size in points
            positions: the tab-stop positions in points from the left margin
            aligns: the alignment of text at each tab stop
            leaders: leader style codes for each segment (0 = none)

        Returns:
            a new `TabbedLine` instance
        """
        DoubleArray = ct.c_double * len(positions)
        Int32Array = ct.c_int32 * len(aligns)
        lib.folio_tabbed_line_new_embedded.argtypes = [
            ct.c_uint64,
            ct.c_double,
            DoubleArray,
            Int32Array,
            Int32Array,
            ct.c_int32,
        ]
        lib.folio_tabbed_line_new_embedded.restype = ct.c_uint64
        obj = cls.__new__(cls)
        obj._tabbed_line_handle = lib.folio_tabbed_line_new_embedded(
            font._handle,
            ct.c_double(font_size),
            DoubleArray(positions),
            Int32Array([align.value for align in aligns]),
            Int32Array(leaders),
            ct.c_int32(len(leaders)),
        )
        return obj

    @_with_error_handling(TabbedLineException)
    def segments(self, segments: list[str]) -> "TabbedLine":
        """
        Sets the text content of each tab segment.

        The number of strings should match the number of tab stops
        defined at construction time.

        Args
            segments: the text for each tab stop, in order

        Returns:
            this instance for chaining
        """
        CharPArray = ct.c_char_p * len(segments)
        lib.folio_tabbed_line_set_segments.argtypes = [
            ct.c_uint64,
            CharPArray,
            ct.c_int32,
        ]
        lib.folio_tabbed_line_set_segments.restype = ct.c_int32
        return lib.folio_tabbed_line_set_segments(
            self._handle, CharPArray(segments), ct.c_int32(len(segments))
        )

    @_with_error_handling(TabbedLineException)
    def color(self, color: Color) -> "TabbedLine":
        """
        Sets the text color for this tabbed line.

        Args:
            color: the RGB color

        Returns:
            this instance for chaining
        """
        return lib.folio_tabbed_line_set_color(
            self._handle,
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(TabbedLineException)
    def leading(self, leading: float) -> "TabbedLine":
        """
        Sets the line-height multiplier for this tabbed line.

        Args:
            leading: the leading multiplier (e.g. `1.5` for 150% line height)

        Returns:
            this instance for chaining
        """
        return lib.folio_tabbed_line_set_leading(self._handle, ct.c_double(leading))

    def close(self):
        lib.folio_tabbed_line_free(self._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
