"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
from typing import TYPE_CHECKING

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import FloatSides
from folio_pdf.exceptions import FloatException

if TYPE_CHECKING:
    from folio_pdf.folio_pdf import Element


class Float(AbstractFolioObject):
    _requires_close = True

    def __init__(self, side: FloatSides, element: "Element"):
        self.__handle = lib.folio_float_new(ct.c_int32(side.value), element._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    def close(self):
        lib.folio_float_free(self._handle)

    @_with_error_handling(FloatException)
    def margin(self, margin: float):
        return lib.folio_float_set_margin(self._handle, ct.c_double(margin))
