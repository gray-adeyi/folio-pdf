"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Directions, ListStyles
from folio_pdf.exceptions import ListException
from folio_pdf.font import Font
from folio_pdf.run_list import RunList


class List(AbstractFolioObject):
    _requires_close = True

    def __init__(self, font: Font, font_size: float):
        self._list_handle = lib.folio_list_new(font.handle, ct.c_double(font_size))

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._list_handle)

    def close(self):
        lib.folio_list_free(self.handle)

    @classmethod
    def new_embedded(
        cls,
        font: Font,
        font_size: float,
    ):
        obj = cls.__new__(cls)
        obj._list_handle = lib.folio_list_new_embedded(
            font.handle, ct.c_double(font_size)
        )
        return obj

    @classmethod
    def _new_from_handle(cls, handle: int):
        obj = cls.__new__(cls)
        obj._list_handle = handle
        return obj

    @_with_error_handling(ListException)
    def set_style(self, style: ListStyles):
        return lib.folio_list_set_style(self.handle, ct.c_int32(style))

    @_with_error_handling(ListException)
    def set_indent(self, indent: float):
        return lib.folio_list_set_indent(self.handle, ct.c_double(indent))

    @_with_error_handling(ListException)
    def set_leading(self, leading: float):
        return lib.folio_list_set_leading(self.handle, ct.c_double(leading))

    @_with_error_handling(ListException)
    def set_direction(self, dir: Directions):
        return lib.folio_list_set_direction(self.handle, ct.c_int32(dir.value))

    @_with_error_handling(ListException)
    def add_item(self, text: str):
        return lib.folio_list_add_item(self.handle, ct.c_char_p(text.encode()))

    def add_nested_item(
        self, text: str
    ): ...  # TODO: Find out what type of object the binding call of the fn returns

    @_with_error_handling(ListException)
    def add_item_runs(self, run_list: RunList):
        return lib.folio_list_add_item_runs(self.handle, run_list.handle)

    def add_item_runs_with_sublist(self, run_list: RunList) -> "List":
        handle = lib.folio_list_add_item_runs_with_sublist(self.handle, run_list.handle)
        return self._new_from_handle(handle)
