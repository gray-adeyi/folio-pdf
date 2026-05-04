"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

from folio_pdf.exceptions import BarcodeElementException

from folio_pdf.enums import Alignments
from folio_pdf.barcode import Barcode

from folio_pdf.core import lib, _with_error_handling
from folio_pdf.object import AbstractFolioObject
import ctypes as ct


class BarcodeElement(AbstractFolioObject):
    _requires_close = True

    def __init__(self, bc: Barcode, width: float):
        self._barcode_handle = lib.folio_barcode_element_new(
            bc.handle, ct.c_double(width)
        )

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._barcode_handle)

    def close(self):
        lib.folio_barcode_element_free(self.handle)

    @_with_error_handling(BarcodeElementException)
    def set_height(self, height: float):
        return lib.folio_barcode_element_set_height(self.handle, ct.c_double(height))

    @_with_error_handling(BarcodeElementException)
    def set_align(self, align: Alignments):
        return lib.folio_barcode_element_set_align(self.handle, ct.c_int32(align.value))

    @_with_error_handling(BarcodeElementException)
    def set_alt_text(self, text: str):
        return lib.folio_barcode_element_set_alt_text(
            self.handle, ct.c_char_p(text.encode())
        )
