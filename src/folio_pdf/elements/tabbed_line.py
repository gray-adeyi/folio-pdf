"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, lib


class TabbedLine(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._tabbed_line_handle = lib.folio_tabbed_line_new()

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._tabbed_line_handle)

    def close(self):
        lib.folio_tabbed_line_free(self.handle)

    @classmethod
    def new_embedded(cls): ...

    def set_segments(self): ...

    def set_color(self): ...

    def set_leading(self): ...
