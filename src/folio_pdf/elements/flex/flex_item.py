"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
from typing import TYPE_CHECKING

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Alignment
from folio_pdf.exceptions import FlexItemException

if TYPE_CHECKING:
    from folio_pdf.folio_pdf import Element


_ErrorCode = int


lib.folio_flex_item_new.argtypes = [ct.c_uint64]
lib.folio_flex_item_new.restype = ct.c_uint64

lib.folio_flex_item_free.argtypes = [ct.c_uint64]
lib.folio_flex_item_free.restype = None

lib.folio_flex_item_set_grow.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_flex_item_set_grow.restype = ct.c_int32

lib.folio_flex_item_set_shrink.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_flex_item_set_shrink.restype = ct.c_int32

lib.folio_flex_item_set_basis.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_flex_item_set_basis.restype = ct.c_int32

lib.folio_flex_item_set_align_self.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_flex_item_set_align_self.restype = ct.c_int32

lib.folio_flex_item_set_margins.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_flex_item_set_margins.restype = ct.c_int32


class FlexItem(AbstractFolioObject):
    """
    A wrapper around a child element inside a {@link Flex} container, providing
    per-item flex layout controls such as grow factor, shrink factor, basis,
    and self-alignment.
    """

    _requires_close = True
    _binding_resource_free_fn = lib.folio_flex_item_free

    def __init__(self, element: "Element"):
        self._is_closed = False
        self.__handle = lib.folio_flex_item_new(element._handle)

    @_with_error_handling(FlexItemException)
    def grow(self, grow: float) -> _ErrorCode:
        """
        Sets the flex-grow factor, controlling how much this item expands to
        fill available space.

        Args:
            grow: the grow factor (0 = do not grow)

        Returns:
            this instance for chaining
        """
        return lib.folio_flex_item_set_grow(self._handle, ct.c_double(grow))

    @_with_error_handling(FlexItemException)
    def shrink(self, shrink: float) -> _ErrorCode:
        """
        Sets the flex-shrink factor, controlling how much this item contracts
        when space is limited.

        Args:
            shrink: the shrink factor (0 = do not shrink)

        Returns
            this instance for chaining
        """
        return lib.folio_flex_item_set_shrink(self._handle, ct.c_double(shrink))

    @_with_error_handling(FlexItemException)
    def basis(self, basis: float) -> _ErrorCode:
        """
        Sets the flex-basis, specifying the initial main-axis size of
        this item in points.

        Args:
            basis: the base size in points

        Returns:
            this instance for chaining
        """
        return lib.folio_flex_item_set_basis(self._handle, ct.c_double(basis))

    @_with_error_handling(FlexItemException)
    def align_self(self, align: Alignment) -> _ErrorCode:
        """
        Overrides the container's {@code alignItems} setting for this individual item.

        Args:
            align: the cross-axis alignment for this item

        Returns:
            this instance for chaining
        """
        return lib.folio_flex_item_set_align_self(self._handle, ct.c_int32(align))

    @_with_error_handling(FlexItemException)
    def margin(
        self, top: float, right: float, bottom: float, left: float
    ) -> _ErrorCode:
        """
        Sets individual margins around this flex item.

        Args:
            top: top margin in points
            right: right margin in points
            bottom: bottom margin in points
            left: left margin in points

        Returns:
            this instance for chaining
        """
        return lib.folio_flex_item_set_margins(
            self._handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
