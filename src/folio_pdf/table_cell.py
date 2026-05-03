"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

from folio_pdf.exceptions import TableCellException
from folio_pdf.enums import Alignments, VerticalAlignments

from folio_pdf.core import lib, _with_error_handling
from folio_pdf.object import AbstractFolioObject
import ctypes as ct


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
    def set_align(self, align: Alignments):
        return lib.folio_cell_set_align(self.handle, ct.c_int32(align.value))

    @_with_error_handling(TableCellException)
    def set_padding(self, padding: float):
        return lib.folio_cell_set_padding(self.handle, ct.c_double(padding))

    @_with_error_handling(TableCellException)
    def set_padding_sides(self, top: float, right: float, bottom: float, left: float):
        return lib.folio_cell_set_padding_sides(
            self.handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )

    @_with_error_handling(TableCellException)
    def set_valign(self, valign: VerticalAlignments):
        return lib.folio_cell_set_valign(self.handle, ct.c_int32(valign))

    @_with_error_handling(TableCellException)
    def set_background(self, r: float, g: float, b: float):
        return lib.folio_cell_set_background(
            self.handle, ct.c_double(r), ct.c_double(g), ct.c_double(b)
        )

    @_with_error_handling(TableCellException)
    def set_colspan(self, n: int):
        return lib.folio_cell_set_colspan(self.handle, ct.c_int32(n))

    @_with_error_handling(TableCellException)
    def set_rowspan(self, n: int):
        return lib.folio_cell_set_rowspan(self.handle, ct.c_int32(n))

    @_with_error_handling(TableCellException)
    def set_border(self, width: float, r: float, g: float, b: float):
        return lib.folio_cell_set_border(
            self.handle,
            ct.c_double(width),
            ct.c_double(r),
            ct.c_double(g),
            ct.c_double(b),
        )

    @_with_error_handling(TableCellException)
    def set_borders(
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
    def set_width_hint(self, pts: float):
        return lib.folio_cell_set_width_hint(self.handle, ct.c_double(pts))

    @_with_error_handling(TableCellException)
    def set_border_radius(self, radius: float):
        return lib.folio_cell_set_border_radius(self.handle, ct.c_double(radius))

    @_with_error_handling(TableCellException)
    def set_border_radius_per_corner(
        self, top_left: float, top_right: float, bottom_right: float, bottom_left: float
    ):
        return lib.folio_cell_set_border_radius_per_corner(
            self.handle,
            ct.c_double(top_left),
            ct.c_double(top_right),
            ct.c_double(bottom_right),
            ct.c_double(bottom_left),
        )
