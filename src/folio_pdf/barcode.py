"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

from folio_pdf.core import lib
from folio_pdf.object import AbstractFolioObject
import ctypes as ct


class Barcode(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._barcode_handle = -1

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._barcode_handle)

    def close(self):
        lib.folio_barcode_free(self.handle)

    @classmethod
    def new_qr_ecc(cls): ...

    @classmethod
    def new_code128(cls): ...

    @classmethod
    def new_ean13(cls): ...

    @property
    def width(self): ...

    @property
    def height(self): ...
