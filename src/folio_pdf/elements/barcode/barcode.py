"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
import sys

from folio_pdf.core import AbstractFolioObject, lib
from folio_pdf.enums import ECCLevel

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


lib.folio_barcode_qr.argtypes = [ct.c_char_p]
lib.folio_barcode_qr.restype = ct.c_uint64

lib.folio_barcode_qr_ecc.argtypes = [ct.c_char_p, ct.c_int32]
lib.folio_barcode_qr_ecc.restype = ct.c_uint64

lib.folio_barcode_code128.argtypes = [ct.c_char_p]
lib.folio_barcode_code128.restype = ct.c_uint64

lib.folio_barcode_ean13.argtypes = [ct.c_char_p]
lib.folio_barcode_ean13.restype = ct.c_uint64

lib.folio_barcode_width.argtypes = [ct.c_uint64]
lib.folio_barcode_width.restype = ct.c_int32

lib.folio_barcode_height.argtypes = [ct.c_uint64]
lib.folio_barcode_height.restype = ct.c_int32

lib.folio_barcode_free.argtypes = [ct.c_uint64]
lib.folio_barcode_free.restype = None


class Barcode(AbstractFolioObject):
    """
    Represents a barcode that can be used with a `BarcodeElement` which can then be
    added to a `Document` or `Div`
    """

    _requires_close = True
    _binding_resource_free_fn = lib.folio_barcode_free

    def __init__(self, data: str):
        """
        Creates a QR code barcode element with the default error correction level.

        Args:
            data:  the data to encode

        Returns:
            a new `Barcode` instance
        """
        self._is_closed = False
        self.__handle = lib.folio_barcode_qr(ct.c_char_p(data.encode()))

    @classmethod
    def new_qr_ecc(cls, data: str, level: ECCLevel) -> Self:
        """
           Creates a QR code barcode element with the specified error correction level.

        Args:
            data: the data to encode
            ecc: the QR error correction level

        Returns:
            a new `Barcode` instance
        """
        obj = cls.__new__(cls)
        obj._is_closed = False
        obj.__handle = lib.folio_barcode_qr_ecc(
            ct.c_char_p(data.encode()), ct.c_int32(level.value)
        )
        return obj

    @classmethod
    def new_code128(cls, data: str) -> Self:
        """
        Creates a Code 128 barcode.

        Args:
            data  the data to encode

        Returns:
            a new `Barcode` instance
        """
        obj = cls.__new__(cls)
        obj._is_closed = False
        obj.__handle = lib.folio_barcode_code128(ct.c_char_p(data.encode()))
        return obj

    @classmethod
    def new_ean13(cls, data: str) -> Self:
        """
        Creates an EAN-13 barcode element.

        Args:
            data: the 13-digit EAN-13 string to encode

        Returns:
            a new `Barcode` instance
        """
        obj = cls.__new__(cls)
        obj._is_closed = False
        obj.__handle = lib.folio_barcode_ean13(ct.c_char_p(data.encode()))
        return obj

    @property
    def width(self) -> int:
        """
        Returns the intrinsic symbol width of the underlying barcode data
        (in barcode units).

        Returns:
            the barcode symbol width
        """
        return lib.folio_barcode_width(self._handle)

    @property
    def height(self) -> int:
        """
        Returns the intrinsic symbol height of the underlying barcode data
        (in barcode units).

        Returns:
            the barcode symbol width
        """
        return lib.folio_barcode_height(self._handle)

    def close(self):
        lib.folio_barcode_free(self._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
