"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

from folio_pdf.object import AbstractFolioObject
import ctypes as ct


class TableRow(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._row_handle = -1

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._row_handle)

    @classmethod
    def _new_from_handle(cls, row_handle: int):
        obj = cls.__new__(cls)
        cls._row_handle = row_handle
        return obj
