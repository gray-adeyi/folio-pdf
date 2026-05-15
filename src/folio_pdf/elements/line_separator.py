"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, lib


class LineSeparator(AbstractFolioObject):
    _requires_close = False

    def __init__(self):
        self.__handle = lib.folio_line_separator_new()

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
