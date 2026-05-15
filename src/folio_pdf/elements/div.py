"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
from typing import TYPE_CHECKING

from folio_pdf.color import Color
from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.exceptions import DivException

if TYPE_CHECKING:
    from folio_pdf.folio_pdf import Element


class Div(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._div_handle = -1

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._div_handle)

    def close(self):
        lib.folio_div_free(self.handle)

    @_with_error_handling(DivException)
    def add(self, element: "Element"):
        return lib.folio_div_add(self.handle, element.handle)

    @_with_error_handling(DivException)
    def padding(self, top: float, right: float, bottom: float, left: float):
        return lib.folio_div_set_padding(
            self.handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )

    @_with_error_handling(DivException)
    def background(self, color: Color):
        return lib.folio_div_set_background(
            self.handle,
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(DivException)
    def border(self, width: float, color: Color):
        return lib.folio_div_set_border(
            self.handle,
            ct.c_double(width),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(DivException)
    def width(self, pts: float):
        return lib.folio_div_set_width(self.handle, ct.c_double(pts))

    @_with_error_handling(DivException)
    def min_height(self, pts: float):
        return lib.folio_div_set_min_height(self.handle, ct.c_double(pts))

    @_with_error_handling(DivException)
    def max_width(self, pts: float):
        return lib.folio_div_set_max_width(self.handle, ct.c_double(pts))

    @_with_error_handling(DivException)
    def min_width(self, pts: float):
        return lib.folio_div_set_min_width(self.handle, ct.c_double(pts))

    @_with_error_handling(DivException)
    def width_percent(self, pct: float):
        return lib.folio_div_set_width_percent(self.handle, ct.c_double(pct))

    @_with_error_handling(DivException)
    def aspect_ratio(self, ratio: float):
        return lib.folio_div_set_aspect_ratio(self.handle, ct.c_double(ratio))

    @_with_error_handling(DivException)
    def keep_together(self, enabled: bool):
        return lib.folio_div_set_keep_together(self.handle, ct.c_bool(enabled))

    @_with_error_handling(DivException)
    def border_radius_per_corner(
        self, top_left: float, top_right: float, bottom_right: float, bottom_left: float
    ):
        return lib.folio_div_set_border_radius_per_corner(
            self.handle,
            ct.c_double(top_left),
            ct.c_double(top_right),
            ct.c_double(bottom_right),
            ct.c_double(bottom_left),
        )

    @_with_error_handling(DivException)
    def hcenter(self, enabled: bool):
        return lib.folio_div_set_hcenter(self.handle, ct.c_int32(enabled))

    @_with_error_handling(DivException)
    def hright(self, enabled: bool):
        return lib.folio_div_set_hright(self.handle, ct.c_int32(enabled))

    @_with_error_handling(DivException)
    def clear(self, value: str):
        return lib.folio_div_set_clear(self.handle, ct.c_char_p(value.encode()))

    @_with_error_handling(DivException)
    def outline(self, width: float, style: str, color: Color, offset: float):
        return lib.folio_div_set_outline(
            self.handle,
            ct.c_double(width),
            ct.c_char_p(style.encode()),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
            ct.c_double(offset),
        )

    @_with_error_handling(DivException)
    def add_box_shadow(
        self,
        offset_x: float,
        offset_y: float,
        blur: float,
        spread: float,
        color: Color,
    ):
        return lib.folio_div_add_box_shadow(
            self.handle,
            ct.c_double(offset_x),
            ct.c_double(offset_y),
            ct.c_double(blur),
            ct.c_double(spread),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(DivException)
    def space_before(self, pts: float):
        return lib.folio_div_set_space_before(self.handle, ct.c_double(pts))

    @_with_error_handling(DivException)
    def space_after(self, pts: float):
        return lib.folio_div_set_space_after(self.handle, ct.c_double(pts))

    @_with_error_handling(DivException)
    def border_radius(self, radius: float):
        return lib.folio_div_set_boarder_radius(self.handle, ct.c_double(radius))

    @_with_error_handling(DivException)
    def opacity(self, opacity: float):
        return lib.folio_div_set_opacity(self.handle, ct.c_double(opacity))

    @_with_error_handling(DivException)
    def overflow(self, mode: str):
        return lib.folio_div_set_overflow(self.handle, ct.c_char_p(mode.encode()))

    @_with_error_handling(DivException)
    def tag(self, tag: str):
        return lib.folio_div_set_tag(self.handle, ct.c_char_p(tag.encode()))

    @_with_error_handling(DivException)
    def box_shadow(
        self,
        offset_x: float,
        offset_y: float,
        blur: float,
        spread: float,
        color: Color,
    ):
        return lib.folio_div_set_box_shadow(
            self.handle,
            ct.c_double(offset_x),
            ct.c_double(offset_y),
            ct.c_double(blur),
            ct.c_double(spread),
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(DivException)
    def max_height(self, pts: float):
        return lib.folio_div_set_max_height(self.handle, ct.c_double(pts))
