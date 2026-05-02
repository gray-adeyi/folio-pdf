"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

from folio_pdf.core import lib
from folio_pdf.object import AbstractFolioObject
import ctypes as ct


class PDFRedactor(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._redactor_handle = -1

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._redactor_handle)

    def close(self):
        lib.folio_redact_opts_free(self.handle)
