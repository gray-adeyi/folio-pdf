"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
from typing import TYPE_CHECKING

from folio_pdf.color import Color
from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import (
    Alignment,
    FlexDirection,
    FlexWrap,
    JustifyContent,
)
from folio_pdf.exceptions import FlexException

from .flex_item import FlexItem

_ErrorCode = int

if TYPE_CHECKING:
    from folio_pdf.folio_pdf import Element

lib.folio_flex_new.argtypes = []
lib.folio_flex_new.restype = ct.c_uint64

lib.folio_flex_free.argtypes = [ct.c_uint64]
lib.folio_flex_free.restype = None

lib.folio_flex_add.argtypes = [ct.c_uint64, ct.c_uint64]
lib.folio_flex_add.restype = ct.c_int32

lib.folio_flex_add_item.argtypes = [ct.c_uint64, ct.c_uint64]
lib.folio_flex_add_item.restype = ct.c_int32

lib.folio_flex_set_direction.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_flex_set_direction.restype = ct.c_int32

lib.folio_flex_set_justify_content.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_flex_set_justify_content.restype = ct.c_int32

lib.folio_flex_set_align_items.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_flex_set_align_items.restype = ct.c_int32

lib.folio_flex_set_wrap.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_flex_set_wrap.restype = ct.c_int32

lib.folio_flex_set_gap.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_flex_set_gap.restype = ct.c_int32

lib.folio_flex_set_padding.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_flex_set_padding.restype = ct.c_int32

lib.folio_flex_set_background.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_flex_set_background.restype = ct.c_int32

lib.folio_flex_set_space_before.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_flex_set_space_before.restype = ct.c_int32

lib.folio_flex_set_space_after.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_flex_set_space_after.restype = ct.c_int32

lib.folio_flex_set_row_gap.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_flex_set_row_gap.restype = ct.c_int32

lib.folio_flex_set_column_gap.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_flex_set_column_gap.restype = ct.c_int32

lib.folio_flex_set_align_content.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_flex_set_align_content.restype = ct.c_int32

lib.folio_flex_set_borders.argtypes = [
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
lib.folio_flex_set_borders.restype = ct.c_int32

lib.folio_flex_set_padding_all.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_flex_set_padding_all.restype = ct.c_int32

lib.folio_flex_set_border.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_flex_set_border.restype = ct.c_int32


class Flex(AbstractFolioObject):
    _requires_close = True
    _binding_resource_free_fn = lib.folio_flex_free

    def __init__(self):
        self._is_closed = False
        self.__handle = lib.folio_flex_new()

    @_with_error_handling(FlexException)
    def add(self, element: "Element") -> _ErrorCode:
        return lib.folio_flex_add(self._handle, element._handle)

    @_with_error_handling(FlexException)
    def add_item(self, item: FlexItem) -> _ErrorCode:
        return lib.folio_flex_add_item(self._handle, item._handle)

    @_with_error_handling(FlexException)
    def direction(self, direction: FlexDirection) -> _ErrorCode:
        return lib.folio_flex_set_direction(self._handle, ct.c_int32(direction.value))

    @_with_error_handling(FlexException)
    def justify_content(self, justify: JustifyContent) -> _ErrorCode:
        return lib.folio_flex_set_justify_content(
            self._handle, ct.c_int32(justify.value)
        )

    @_with_error_handling(FlexException)
    def align_items(self, align: Alignment) -> _ErrorCode:
        return lib.folio_flex_set_align_items(self._handle, ct.c_int32(align.value))

    @_with_error_handling(FlexException)
    def wrap(self, wrap: FlexWrap) -> _ErrorCode:
        return lib.folio_flex_set_wrap(self._handle, ct.c_int32(wrap.value))

    @_with_error_handling(FlexException)
    def gap(self, gap: float) -> _ErrorCode:
        return lib.folio_flex_set_gap(self._handle, ct.c_double(gap))

    @_with_error_handling(FlexException)
    def padding(self, padding: float) -> _ErrorCode:
        return lib.folio_flex_set_padding(self._handle, ct.c_double(padding))

    @_with_error_handling(FlexException)
    def background(self, color: Color) -> _ErrorCode:
        return lib.folio_flex_set_background(
            self._handle,
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(FlexException)
    def space_before(self, pts: float) -> _ErrorCode:
        return lib.folio_flex_set_space_before(self._handle, ct.c_double(pts))

    @_with_error_handling(FlexException)
    def space_after(self, pts: float) -> _ErrorCode:
        return lib.folio_flex_set_space_after(self._handle, ct.c_double(pts))

    @_with_error_handling(FlexException)
    def row_gap(self, gap: float) -> _ErrorCode:
        return lib.folio_flex_set_row_gap(self._handle, ct.c_double(gap))

    @_with_error_handling(FlexException)
    def column_gap(self, gap: float) -> _ErrorCode:
        return lib.folio_flex_set_column_gap(self._handle, ct.c_double(gap))

    @_with_error_handling(FlexException)
    def align_content(self, align: Alignment) -> _ErrorCode:
        return lib.folio_flex_set_align_content(self._handle, ct.c_int32(align.value))

    @_with_error_handling(FlexException)
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
    ) -> _ErrorCode:
        return lib.folio_flex_set_borders(
            self._handle,
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
    def padding_all(
        self, top: float, right: float, bottom: float, left: float
    ) -> _ErrorCode:
        return lib.folio_flex_set_padding_all(
            self._handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )

    @_with_error_handling(FlexException)
    def border(self, width: float, red: float, green: float, blue: float) -> _ErrorCode:
        return lib.folio_flex_set_border(
            self._handle,
            ct.c_double(width),
            ct.c_double(red),
            ct.c_double(green),
            ct.c_double(blue),
        )

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
