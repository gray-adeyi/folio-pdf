"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

from folio_pdf.exceptions import FlexItemException

from folio_pdf.enums import Alignments

from folio_pdf.core import lib, _with_error_handling
from folio_pdf.object import AbstractFolioObject
import ctypes as ct
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from folio_pdf.folio_pdf import Element


class FlexItem(AbstractFolioObject):
    _requires_close = True

    def __init__(self, element: "Element"):
        self._flex_handle = lib.folio_flex_item_new(element.handle)

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._flex_handle)

    def close(self):
        lib.folio_flex_item_free(self.handle)

    @_with_error_handling(FlexItemException)
    def set_grow(self, grow: float):
        return lib.folio_flex_item_set_grow(self.handle, ct.c_double(grow))

    @_with_error_handling(FlexItemException)
    def set_shrink(self, shrink: float):
        return lib.folio_flex_item_set_shrink(self.handle, ct.c_double(shrink))

    @_with_error_handling(FlexItemException)
    def set_basis(self, basis: float):
        return lib.folio_flex_item_set_basis(self.handle, ct.c_double(basis))

    @_with_error_handling(FlexItemException)
    def set_align_self(self, align: Alignments):
        return lib.folio_flex_item_set_align_self(self.handle, ct.c_int32(align))

    @_with_error_handling(FlexItemException)
    def set_margin(self, top: float, right: float, bottom: float, left: float):
        return lib.folio_flex_item_set_margins(
            self.handle,
            ct.c_double(top),
            ct.c_double(right),
            ct.c_double(bottom),
            ct.c_double(left),
        )
