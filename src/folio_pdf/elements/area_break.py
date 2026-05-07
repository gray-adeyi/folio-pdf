"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, lib


class AreaBreak(AbstractFolioObject):
    _requires_close = False

    def __init__(self):
        self._area_break_handle = lib.folio_area_break_new()

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._area_break_handle)
