"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.color import Color
from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Alignments
from folio_pdf.exceptions import TabbedLineException
from folio_pdf.font import Font


class TabbedLine(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self.__handle = lib.folio_tabbed_line_new()

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    def close(self):
        lib.folio_tabbed_line_free(self._handle)

    @classmethod
    def new_embedded(
        cls,
        font: Font,
        font_size: float,
        positions: list[float],
        aligns: list[Alignments],
        leaders,
    ):  # TODO: Find out
        obj = cls.__new__(cls)
        obj._tabbed_line_handle = lib.folio_tabbed_line_new_embedded(
            font._handle,
            ct.c_double(font_size),
        )
        return obj

    @_with_error_handling(TabbedLineException)
    def segments(self, segments: list[str]):
        CharPArray = ct.c_char_p * len(segments)
        return lib.folio_tabbed_line_set_segments(
            self._handle, CharPArray(segments), ct.c_int32(len(segments))
        )

    @_with_error_handling(TabbedLineException)
    def color(self, color: Color):
        return lib.folio_tabbed_line_set_color(
            self._handle,
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(TabbedLineException)
    def leading(self, leading: float):
        return lib.folio_tabbed_line_set_leading(self._handle, ct.c_double(leading))
