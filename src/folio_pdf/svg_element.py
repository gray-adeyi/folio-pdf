"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

from folio_pdf.core import lib
from folio_pdf.object import AbstractFolioObject
import ctypes as ct


class SVGElement(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._svg_element_handle = -1

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._svg_element_handle)

    def close(self):
        lib.folio_svg_element_free(self.handle)

    def set_size(self): ...

    def set_align(self): ...

    def set_alt_text(self): ...
