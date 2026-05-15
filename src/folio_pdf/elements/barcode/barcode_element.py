"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Alignments
from folio_pdf.exceptions import BarcodeElementException

from .barcode import Barcode


class BarcodeElement(AbstractFolioObject):
    """A barcode element that renders QR codes, Code 128, or
    EAN-13 barcodes into a PDF document."""

    _requires_close = True

    def __init__(self, bc: Barcode, width: float):
        self.__handle = lib.folio_barcode_element_new(bc._handle, ct.c_double(width))

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    def close(self):
        lib.folio_barcode_element_free(self._handle)

    @_with_error_handling(BarcodeElementException)
    def height(self, height: float):
        return lib.folio_barcode_element_set_height(self._handle, ct.c_double(height))

    @_with_error_handling(BarcodeElementException)
    def align(self, align: Alignments):
        return lib.folio_barcode_element_set_align(
            self._handle, ct.c_int32(align.value)
        )

    @_with_error_handling(BarcodeElementException)
    def alt_text(self, text: str):
        return lib.folio_barcode_element_set_alt_text(
            self._handle, ct.c_char_p(text.encode())
        )
