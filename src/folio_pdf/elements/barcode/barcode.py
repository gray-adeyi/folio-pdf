"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, lib
from folio_pdf.enums import ECCLevels


class Barcode(AbstractFolioObject):
    _requires_close = True

    def __init__(self, data: str):
        self._barcode_handle = lib.folio_barcode_qr(ct.c_char_p(data.encode()))

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._barcode_handle)

    def close(self):
        lib.folio_barcode_free(self.handle)

    @classmethod
    def new_qr_ecc(cls, data: str, level: ECCLevels):
        obj = cls.__new__(cls)
        obj._barcode_handle = lib.folio_barcode_qr_ecc(
            ct.c_char_p(data.encode()), ct.c_int32(level.value)
        )
        return obj

    @classmethod
    def new_code128(cls, data: str):
        obj = cls.__new__(cls)
        obj._barcode_handle = lib.folio_barcode_code128(ct.c_char_p(data.encode()))
        return obj

    @classmethod
    def new_ean13(cls, data: str):
        obj = cls.__new__(cls)
        obj._barcode_handle = lib.folio_barcode_ean13(ct.c_char_p(data.encode()))
        return obj

    @property
    def width(self):
        return lib.folio_barcode_width(self.handle)

    @property
    def height(self):
        return lib.folio_barcode_height(self.handle)
