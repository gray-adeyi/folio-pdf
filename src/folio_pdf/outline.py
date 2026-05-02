"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

from folio_pdf.object import AbstractFolioObject

from folio_pdf.core import lib
import ctypes as ct


class Outline(AbstractFolioObject):
    _requires_close = False

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._outline_handle)

    @classmethod
    def _new_from_handle(cls, outline_handle: int):
        obj = cls.__new__(cls)
        cls._outline_handle = outline_handle
        return obj

    def add_child(self, title: str, page_index: int) -> "Outline":
        outline_handle = lib.folio_outline_add_child(
            ct.c_uint64(self._outline_handle),
            ct.c_char_p(title.encode()),
            ct.c_int32(page_index),
        )
        return self._new_from_handle(outline_handle)

    def add_child_xyz(
        self, title: str, page_index: int, left: float, top: float, zoom: float
    ) -> "Outline":
        outline_handle = lib.folio_outline_add_child(
            ct.c_uint64(self._outline_handle),
            ct.c_char_p(title.encode()),
            ct.c_int32(page_index),
            ct.c_double(left),
            ct.c_double(top),
            ct.c_double(zoom),
        )
        return self._new_from_handle(outline_handle)
