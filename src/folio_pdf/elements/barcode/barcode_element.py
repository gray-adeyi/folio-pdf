"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Alignments
from folio_pdf.exceptions import BarcodeElementException

from .barcode import Barcode

lib.folio_barcode_element_new.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_barcode_element_new.restype = ct.c_uint64

lib.folio_barcode_element_set_height.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_barcode_element_set_height.restype = ct.c_int32

lib.folio_barcode_element_set_align.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_barcode_element_set_align.restype = ct.c_int32

lib.folio_barcode_element_set_alt_text.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_barcode_element_set_alt_text.restype = ct.c_int32

lib.folio_barcode_element_free.argtypes = [ct.c_uint64]
lib.folio_barcode_element_free.restype = ct.c_int32


class BarcodeElement(AbstractFolioObject):
    """A barcode element that renders QR codes, Code 128, or
    EAN-13 barcodes into a PDF document."""

    _requires_close = True

    def __init__(self, barcode: Barcode, width: float):
        """Create a barcode element.

        Args:
            barcode: the barcode to be rendered
            width: the rendered width in points
        """
        self.__handle = lib.folio_barcode_element_new(
            barcode._handle, ct.c_double(width)
        )

    @_with_error_handling(BarcodeElementException)
    def height(self, height: float):
        """
        Sets the rendered height of the barcode element in points.

        Args:
            height: the height in points

        Returns:
            this instance for chaining
        """
        return lib.folio_barcode_element_set_height(self._handle, ct.c_double(height))

    @_with_error_handling(BarcodeElementException)
    def align(self, align: Alignments):
        """
        Sets the horizontal alignment of the barcode within its container.

        Args:
            align: the desired alignment

        Returns:
            this instance for chaining
        """
        return lib.folio_barcode_element_set_align(
            self._handle, ct.c_int32(align.value)
        )

    @_with_error_handling(BarcodeElementException)
    def alt_text(self, text: str):
        """
        Sets alternative text for PDF/UA accessibility.

        Args:
            text: the alternative text

        Returns:
            this instance for chaining
        """
        return lib.folio_barcode_element_set_alt_text(
            self._handle, ct.c_char_p(text.encode())
        )

    def close(self):
        lib.folio_barcode_element_free(self._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
