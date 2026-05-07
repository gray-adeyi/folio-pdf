"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, lib


class RedactorOptions(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._redactor_options_handle = lib.folio_redact_opts_new()

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._redactor_options_handle)

    def close(self):
        lib.folio_redact_opts_free(self.handle)

    def set_fill_color(self): ...

    def set_overlay(self): ...

    def set_strip_metadata(self): ...
