"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
from typing import TYPE_CHECKING

from folio_pdf.color import Color
from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import AlignItems, JustifyContents
from folio_pdf.exceptions import GridException

if TYPE_CHECKING:
    from folio_pdf.folio_pdf import Element


class Grid(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._grid_handle = lib.folio_grid_new()

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._grid_handle)

    def close(self):
        lib.folio_grid_free(self.handle)

    @_with_error_handling(GridException)
    def add_child(self, element: "Element"):
        return lib.folio_grid_add_child(self.handle, element.handle)

    def template_columns(self): ...

    def template_rows(self): ...

    @_with_error_handling(GridException)
    def border(self, width: float, color: Color):
        return lib.folio_grid_set_border(
            self.handle,
            ct.c_double(width),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(GridException)
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
    ):
        return lib.folio_grid_set_borders(
            self.handle,
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

    def template_areas(self): ...

    def auto_rows(self): ...

    @_with_error_handling(GridException)
    def gap(self, row_gap: float, col_gap: float):
        return lib.folio_grid_set_gap(
            self.handle, ct.c_double(row_gap), ct.c_double(col_gap)
        )

    @_with_error_handling(GridException)
    def placement(self, child_index: int, col_start: int, row_start: int, row_end: int):
        return lib.folio_grid_set_placement(
            self.handle,
            ct.c_int32(child_index),
            ct.c_int32(col_start),
            ct.c_int32(row_start),
            ct.c_int32(row_end),
        )

    @_with_error_handling(GridException)
    def padding(self, padding: float):
        return lib.folio_grid_set_padding(self.handle, ct.c_double(padding))

    @_with_error_handling(GridException)
    def background(self, color: Color):
        return lib.folio_grid_set_background(
            self.handle,
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(GridException)
    def justify_items(self, align: AlignItems):
        return lib.folio_grid_set_justify_items(self.handle, ct.c_int32(align.value))

    @_with_error_handling(GridException)
    def align_items(self, align: AlignItems):
        return lib.folio_grid_set_align_items(self.handle, ct.c_int32(align.value))

    @_with_error_handling(GridException)
    def justify_content(self, justify: JustifyContents):
        return lib.folio_grid_set_justify_content(
            self.handle, ct.c_int32(justify.value)
        )

    @_with_error_handling(GridException)
    def align_content(self, align: JustifyContents):
        return lib.folio_grid_set_align_content(self.handle, ct.c_int32(align.value))

    @_with_error_handling(GridException)
    def space_before(self, pts: float):
        return lib.folio_grid_set_space_before(self.handle, ct.c_double(pts))

    @_with_error_handling(GridException)
    def space_after(self, pts: float):
        return lib.folio_grid_set_space_after(self.handle, ct.c_double(pts))
