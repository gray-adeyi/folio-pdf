"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

from folio_pdf.exceptions import FlexException

from folio_pdf.enums import (
    FlexDirections,
    JustifyContents,
    Alignments,
    FlexWraps,
)

from folio_pdf.flex_item import FlexItem

from folio_pdf.core import lib, _with_error_handling
from folio_pdf.object import AbstractFolioObject
import ctypes as ct
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from folio_pdf.folio_pdf import Element


class Flex(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._flex_handle = lib.folio_flex_new()

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._flex_handle)

    def close(self):
        lib.folio_flex_free(self.handle)

    @_with_error_handling(FlexException)
    def add(self, element: "Element"):
        return lib.folio_flex_add(self.handle, element.handle)

    @_with_error_handling(FlexException)
    def add_item(self, item: FlexItem):
        return lib.folio_flex_add_item(self.handle, item.handle)

    @_with_error_handling(FlexException)
    def set_direction(self, direction: FlexDirections):
        return lib.folio_flex_set_direction(self.handle, ct.c_int32(direction.value))

    @_with_error_handling(FlexException)
    def set_justify_content(self, justify: JustifyContents):
        return lib.folio_flex_set_justify_content(
            self.handle, ct.c_int32(justify.value)
        )

    @_with_error_handling(FlexException)
    def set_align_items(self, align: Alignments):
        return lib.folio_flex_set_align_items(self.handle, ct.c_int32(align.value))

    @_with_error_handling(FlexException)
    def set_wrap(self, wrap: FlexWraps):
        return lib.folio_flex_set_wrap(self.handle, ct.c_int32(wrap.value))

    @_with_error_handling(FlexException)
    def set_gap(self, gap: float):
        return lib.folio_flex_set_gap(self.handle, ct.c_double(gap))

    @_with_error_handling(FlexException)
    def set_padding(self, padding: float):
        return lib.folio_flex_set_padding(self.handle, ct.c_double(padding))

    @_with_error_handling(FlexException)
    def set_background(self, r: float, g: float, b: float):
        return lib.folio_flex_set_background(
            self.handle, ct.c_double(r), ct.c_double(g), ct.c_double(b)
        )

    @_with_error_handling(FlexException)
    def set_space_before(self, pts: float):
        return lib.folio_flex_set_space_before(self.handle, ct.c_double(pts))

    @_with_error_handling(FlexException)
    def set_space_after(self, pts: float):
        return lib.folio_flex_set_space_after(self.handle, ct.c_double(pts))

    @_with_error_handling(FlexException)
    def set_row_gap(self, gap: float):
        return lib.folio_flex_set_row_gap(self.handle, ct.c_double(gap))

    @_with_error_handling(FlexException)
    def set_column_gap(self, gap: float):
        return lib.folio_flex_set_column_gap(self.handle, ct.c_double(gap))

    @_with_error_handling(FlexException)
    def set_align_content(self, align: Alignments):
        return lib.folio_flex_set_align_content(self.handle, ct.c_int32(align.value))

    @_with_error_handling(FlexException)
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
    ):
        return lib.folio_flex_set_borders(
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
            ct.c_double(bottom_blue),
            ct.c_double(bottom_green),
            ct.c_double(left_width),
            ct.c_double(left_red),
            ct.c_double(left_green),
            ct.c_double(left_blue),
        )

    @_with_error_handling(FlexException)
    def set_padding_all(self, top: float, right: float, bottom: float, left: float):
        return lib.folio_flex_set_padding_all(
            self.handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )

    @_with_error_handling(FlexException)
    def set_border(self, width: float, red: float, green: float, blue: float):
        return lib.folio_flex_set_border(
            self.handle,
            ct.c_double(width),
            ct.c_double(red),
            ct.c_double(green),
            ct.c_double(blue),
        )
