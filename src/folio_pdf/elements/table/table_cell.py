"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.color import Color
from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Alignments, VerticalAlignments
from folio_pdf.exceptions import TableCellException


class TableCell(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._cell_handle = -1

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._cell_handle)

    def close(self):
        lib.folio_cell_free(self.handle)

    @classmethod
    def _new_from_handle(cls, cell_handle: int):
        obj = cls.__new__(cls)
        cls._cell_handle = cell_handle
        return obj

    @_with_error_handling(TableCellException)
    def align(self, align: Alignments):
        return lib.folio_cell_set_align(self.handle, ct.c_int32(align.value))

    @_with_error_handling(TableCellException)
    def padding(self, padding: float):
        return lib.folio_cell_set_padding(self.handle, ct.c_double(padding))

    @_with_error_handling(TableCellException)
    def padding_sides(self, top: float, right: float, bottom: float, left: float):
        return lib.folio_cell_set_padding_sides(
            self.handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )

    @_with_error_handling(TableCellException)
    def valign(self, valign: VerticalAlignments):
        return lib.folio_cell_set_valign(self.handle, ct.c_int32(valign))

    @_with_error_handling(TableCellException)
    def background(self, color: Color):
        return lib.folio_cell_set_background(
            self.handle,
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(TableCellException)
    def colspan(self, n: int):
        return lib.folio_cell_set_colspan(self.handle, ct.c_int32(n))

    @_with_error_handling(TableCellException)
    def rowspan(self, n: int):
        return lib.folio_cell_set_rowspan(self.handle, ct.c_int32(n))

    @_with_error_handling(TableCellException)
    def border(self, width: float, color: Color):
        return lib.folio_cell_set_border(
            self.handle,
            ct.c_double(width),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(TableCellException)
    def borders(
        self,
        top_width: float,
        top_red: float,
        top_green: float,
        top_blue: float,
        right_width: float,
        right_red: float,
        right_green: float,
        right_blue: float,
        bottom_width: float,
        bottom_red: float,
        bottom_green: float,
        bottom_blue: float,
        left_width: float,
        left_red: float,
        left_green: float,
        left_blue: float,
    ):  # TODO: Find a way to reduce number of params
        return lib.folio_cell_set_borders(
            ct.c_double(top_width),
            ct.c_double(top_red),
            ct.c_double(top_green),
            ct.c_double(top_blue),
            ct.c_double(right_width),
            ct.c_double(right_red),
            ct.c_double(right_green),
            ct.c_double(right_blue),
            ct.c_double(bottom_width),
            ct.c_double(bottom_red),
            ct.c_double(bottom_green),
            ct.c_double(bottom_blue),
            ct.c_double(left_width),
            ct.c_double(left_red),
            ct.c_double(left_green),
            ct.c_double(left_blue),
        )

    @_with_error_handling(TableCellException)
    def width_hint(self, pts: float):
        return lib.folio_cell_set_width_hint(self.handle, ct.c_double(pts))

    @_with_error_handling(TableCellException)
    def border_radius(self, radius: float):
        return lib.folio_cell_set_border_radius(self.handle, ct.c_double(radius))

    @_with_error_handling(TableCellException)
    def border_radius_per_corner(
        self, top_left: float, top_right: float, bottom_right: float, bottom_left: float
    ):
        return lib.folio_cell_set_border_radius_per_corner(
            self.handle,
            ct.c_double(top_left),
            ct.c_double(top_right),
            ct.c_double(bottom_right),
            ct.c_double(bottom_left),
        )
