"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
import sys

from folio_pdf.core import AbstractFolioObject, lib

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


lib.folio_outline_add_child.argtypes = [ct.c_uint64, ct.c_char_p, ct.c_int32]
lib.folio_outline_add_child.restype = ct.c_uint64

lib.folio_outline_add_child_xyz.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_int32,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_outline_add_child_xyz.restype = ct.c_uint64


class Outline(AbstractFolioObject):
    _requires_close = False

    def __init__(self):
        self.__handle = 0

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    @classmethod
    def _new_from_handle(cls, handle: int) -> Self:
        obj = cls.__new__(cls)
        obj.__handle = handle
        return obj

    def add_child(self, title: str, page_index: int) -> Self:
        """Adds a child bookmark under an existing outline entry.

        Args:
            title: the bookmark label
            page_index: zero-based target page index

        Returns:
            the outline object representing the added child
        """
        outline_handle = lib.folio_outline_add_child(
            self._handle,
            ct.c_char_p(title.encode()),
            ct.c_int32(page_index),
        )
        return self._new_from_handle(outline_handle)

    def add_child_xyz(
        self, title: str, page_index: int, left: float, top: float, zoom: float
    ) -> Self:
        """Adds a child bookmark under an existing outline entry with an
        explicit XYZ destination.

        Args:
            title: the bookmark label
            page_index: zero-based target page index
            left: left coordinate of the destination view
            top: top coordinate of the destination view
            zoom: zoom factor at the destination

        Returns:
            the outline object representing the added child
        """
        outline_handle = lib.folio_outline_add_child_xyz(
            self._handle,
            ct.c_char_p(title.encode()),
            ct.c_int32(page_index),
            ct.c_double(left),
            ct.c_double(top),
            ct.c_double(zoom),
        )
        return self._new_from_handle(outline_handle)
