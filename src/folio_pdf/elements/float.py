"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, lib


class Float(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._float_handle = lib.folio_float_new()

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._float_handle)

    def close(self):
        lib.folio_float_free(self.handle)
