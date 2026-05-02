"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

from folio_pdf.object import AbstractFolioObject
from folio_pdf.core import lib
import ctypes as ct


class Link(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._link_handle = -1

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._link_handle)

    def close(self):
        lib.folio_link_free(self.handle)

    @classmethod
    def new_embedded(cls): ...

    @classmethod
    def new_internal(cls): ...

    def set_color(self): ...

    def set_underline(self): ...

    def set_align(self): ...
