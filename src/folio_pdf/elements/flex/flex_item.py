"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
from typing import TYPE_CHECKING

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Alignments
from folio_pdf.exceptions import FlexItemException

if TYPE_CHECKING:
    from folio_pdf.folio_pdf import Element


class FlexItem(AbstractFolioObject):
    _requires_close = True

    def __init__(self, element: "Element"):
        self.__handle = lib.folio_flex_item_new(element._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    def close(self):
        lib.folio_flex_item_free(self._handle)

    @_with_error_handling(FlexItemException)
    def grow(self, grow: float):
        return lib.folio_flex_item_set_grow(self._handle, ct.c_double(grow))

    @_with_error_handling(FlexItemException)
    def shrink(self, shrink: float):
        return lib.folio_flex_item_set_shrink(self._handle, ct.c_double(shrink))

    @_with_error_handling(FlexItemException)
    def basis(self, basis: float):
        return lib.folio_flex_item_set_basis(self._handle, ct.c_double(basis))

    @_with_error_handling(FlexItemException)
    def align_self(self, align: Alignments):
        return lib.folio_flex_item_set_align_self(self._handle, ct.c_int32(align))

    @_with_error_handling(FlexItemException)
    def margin(self, top: float, right: float, bottom: float, left: float):
        return lib.folio_flex_item_set_margins(
            self._handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )
