"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, lib
from folio_pdf.reader import PDFReader


class FormFiller(AbstractFolioObject):
    _requires_close = True

    def __init__(self, reader: PDFReader):
        self._form_handle = lib.folio_form_filler_new(reader.handle)

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._form_handle)

    def close(self):
        lib.folio_form_filler_free(self.handle)

    def field_names(self): ...

    def get_value(self): ...

    def set_value(self): ...

    def set_checkbox(self): ...
