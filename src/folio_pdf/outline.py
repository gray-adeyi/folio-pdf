"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, lib


class Outline(AbstractFolioObject):
    _requires_close = False

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    @classmethod
    def _new_from_handle(cls, handle: int):
        obj = cls.__new__(cls)
        cls.__handle = handle
        return obj

    def add_child(self, title: str, page_index: int) -> "Outline":
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
    ) -> "Outline":
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
        outline_handle = lib.folio_outline_add_child(
            self._handle,
            ct.c_char_p(title.encode()),
            ct.c_int32(page_index),
            ct.c_double(left),
            ct.c_double(top),
            ct.c_double(zoom),
        )
        return self._new_from_handle(outline_handle)
