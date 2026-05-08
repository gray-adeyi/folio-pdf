"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, lib


class Grid(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._grid_handle = lib.folio_grid_new()

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._grid_handle)

    def close(self):
        lib.folio_grid_free(self.handle)

    def add_child(self): ...

    def set_template_columns(self): ...

    def set_template_rows(self): ...

    def set_border(self): ...

    def set_borders(self): ...

    def set_template_areas(self): ...

    def set_auto_rows(self): ...

    def set_placement(self): ...

    def set_padding(self): ...

    def set_background(self): ...

    def set_justify_items(self): ...

    def set_align_items(self): ...

    def set_justify_content(self): ...

    def set_align_content(self): ...

    def set_space_before(self): ...

    def set_space_after(self): ...
