"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.color import Color
from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Alignment, VerticalAlignment
from folio_pdf.exceptions import TableCellException


if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

_ErrorCode = int

lib.folio_cell_free.argtypes = [ct.c_uint64]
lib.folio_cell_free.restype = None

lib.folio_cell_set_align.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_cell_set_align.restype = ct.c_int32

lib.folio_cell_set_padding.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_cell_set_padding.restype = ct.c_int32

lib.folio_cell_set_padding_sides.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_cell_set_padding_sides.restype = ct.c_int32

lib.folio_cell_set_valign.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_cell_set_valign.restype = ct.c_int32

lib.folio_cell_set_background.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_cell_set_background.restype = ct.c_int32

lib.folio_cell_set_colspan.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_cell_set_colspan.restype = ct.c_int32

lib.folio_cell_set_rowspan.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_cell_set_rowspan.restype = ct.c_int32

lib.folio_cell_set_border.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_cell_set_border.restype = ct.c_int32

lib.folio_cell_set_borders.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_cell_set_borders.restype = ct.c_int32

lib.folio_cell_set_width_hint.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_cell_set_width_hint.restype = ct.c_int32

lib.folio_cell_set_border_radius.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_cell_set_border_radius.restype = ct.c_int32

lib.folio_cell_set_border_radius_per_corner.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_cell_set_border_radius_per_corner.restype = ct.c_int32


class TableCell(AbstractFolioObject):
    _requires_close = True
    _binding_resource_free_fn = lib.folio_cell_free

    def __init__(self):
        self._is_closed = False
        self.__handle = 0

    @_with_error_handling(TableCellException)
    def align(self, align: Alignment) -> _ErrorCode:
        return lib.folio_cell_set_align(self._handle, ct.c_int32(align.value))

    @_with_error_handling(TableCellException)
    def padding(self, padding: float) -> _ErrorCode:
        return lib.folio_cell_set_padding(self._handle, ct.c_double(padding))

    @_with_error_handling(TableCellException)
    def padding_sides(
        self, top: float, right: float, bottom: float, left: float
    ) -> _ErrorCode:
        return lib.folio_cell_set_padding_sides(
            self._handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )

    @_with_error_handling(TableCellException)
    def valign(self, valign: VerticalAlignment) -> _ErrorCode:
        return lib.folio_cell_set_valign(self._handle, ct.c_int32(valign))

    @_with_error_handling(TableCellException)
    def background(self, color: Color) -> _ErrorCode:
        return lib.folio_cell_set_background(
            self._handle,
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(TableCellException)
    def colspan(self, n: int) -> _ErrorCode:
        return lib.folio_cell_set_colspan(self._handle, ct.c_int32(n))

    @_with_error_handling(TableCellException)
    def rowspan(self, n: int) -> _ErrorCode:
        return lib.folio_cell_set_rowspan(self._handle, ct.c_int32(n))

    @_with_error_handling(TableCellException)
    def border(self, width: float, color: Color) -> _ErrorCode:
        return lib.folio_cell_set_border(
            self._handle,
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
    ) -> _ErrorCode:  # TODO: Find a way to reduce number of params
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
    def width_hint(self, pts: float) -> _ErrorCode:
        return lib.folio_cell_set_width_hint(self._handle, ct.c_double(pts))

    @_with_error_handling(TableCellException)
    def border_radius(self, radius: float) -> _ErrorCode:
        return lib.folio_cell_set_border_radius(self._handle, ct.c_double(radius))

    @_with_error_handling(TableCellException)
    def border_radius_per_corner(
        self, top_left: float, top_right: float, bottom_right: float, bottom_left: float
    ) -> _ErrorCode:
        return lib.folio_cell_set_border_radius_per_corner(
            self._handle,
            ct.c_double(top_left),
            ct.c_double(top_right),
            ct.c_double(bottom_right),
            ct.c_double(bottom_left),
        )

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    @classmethod
    def _new_from_handle(cls, cell_handle: int):
        obj = cls.__new__(cls)
        cls.__handle = cell_handle
        return obj
