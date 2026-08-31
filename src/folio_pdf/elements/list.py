"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""
import ctypes as ct
import sys

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Direction, ListStyle
from folio_pdf.exceptions import ListException
from folio_pdf.font import Font
from folio_pdf.run_list import RunList

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

_ErrorCode = int

lib.folio_list_new.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_list_new.restype = ct.c_uint64

lib.folio_list_new_embedded.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_list_new_embedded.restype = ct.c_uint64

lib.folio_list_free.argtypes = [ct.c_uint64]
lib.folio_list_free.restype = None

lib.folio_list_set_style.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_list_set_style.restype = ct.c_int32

lib.folio_list_set_indent.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_list_set_indent.restype = ct.c_int32

lib.folio_list_set_leading.argtypes = [ct.c_uint64, ct.c_double]
lib.folio_list_set_leading.restype = ct.c_int32

lib.folio_list_set_direction.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_list_set_direction.restype = ct.c_int32

lib.folio_list_add_item.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_list_add_item.restype = ct.c_int32

lib.folio_list_add_nested_item.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_list_add_nested_item.restype = ct.c_uint64

lib.folio_list_add_item_runs.argtypes = [ct.c_uint64, ct.c_uint64]
lib.folio_list_add_item_runs.restype = ct.c_int32

lib.folio_list_add_item_runs_with_sublist.argtypes = [ct.c_uint64, ct.c_uint64]
lib.folio_list_add_item_runs_with_sublist.restype = ct.c_uint64


class List(AbstractFolioObject):
    """
    Represents an ordered or unordered list.
    """

    _requires_close = True
    _binding_resource_free_fn = lib.folio_list_free

    def __init__(self, font: Font, font_size: float):
        self._is_closed = False
        self.__handle = lib.folio_list_new(font._handle, ct.c_double(font_size))

    @classmethod
    def new_embedded(
        cls,
        font: Font,
        font_size: float,
    ) -> Self:
        obj = cls.__new__(cls)
        obj._is_closed = False
        obj.__handle = lib.folio_list_new_embedded(font._handle, ct.c_double(font_size))
        return obj

    @classmethod
    def _new_from_handle(cls, handle: int) -> Self:
        obj = cls.__new__(cls)
        obj._is_closed = False
        obj.__handle = handle
        return obj

    @_with_error_handling(ListException)
    def style(self, style: ListStyle) -> _ErrorCode:
        """
        Sets the bullet or numbering style for this list.

        Args:
            style: the desired {@link ListStyle}

        Returns:
            this list, for chaining
        """
        return lib.folio_list_set_style(self._handle, ct.c_int32(style))

    @_with_error_handling(ListException)
    def indent(self, indent: float) -> _ErrorCode:
        """
        Sets the left indent for list items in points.

        Args:
            indent: indent in points

        Returns:
            this list, for chaining
        """
        return lib.folio_list_set_indent(self._handle, ct.c_double(indent))

    @_with_error_handling(ListException)
    def leading(self, leading: float) -> _ErrorCode:
        """
        Sets the line-height multiplier for list items.

        Args:
            leading: line height as a multiple of the font size

        Returns:
            this list, for chaining
        """
        return lib.folio_list_set_leading(self._handle, ct.c_double(leading))

    @_with_error_handling(ListException)
    def direction(self, dir: Direction) -> _ErrorCode:
        """
        Sets the writing direction (LTR, RTL, or AUTO) for this list.

        RTL lists place markers (bullets or numbers) on the right and run
        item text right-to-left. `Directions.AUTO` runs the Unicode Bidi
        algorithm over the items to infer direction. See ISO 32000-2 §14.8.2
        for how direction interacts with tagged-PDF structure attributes.

        Args:
            dir: the desired `Directions` variant

        Returns:
            this list, for chaining
        """
        return lib.folio_list_set_direction(self._handle, ct.c_int32(dir.value))

    @_with_error_handling(ListException)
    def add_item(self, text: str) -> _ErrorCode:
        """
        Adds a list item to the list

        Args:
            text: the value of the list item.

        Returns:
            this list, for chaining
        """
        return lib.folio_list_add_item(self._handle, ct.c_char_p(text.encode()))

    def add_nested_item(self, text: str) -> Self:
        """
        Appends a nested (indented) sub-list item and returns the new sub-list.

        Args:
            text: the nested item text

        Returns:
            the new nested {@link ListElement}
        """
        handle = lib.folio_list_add_nested_item(
            self._handle, ct.c_char_p(text.encode())
        )
        return self._new_from_handle(handle)

    @_with_error_handling(ListException)
    def add_item_runs(self, run_list: RunList) -> _ErrorCode:
        """
        Adds a list item with styled text runs from a {@link RunList}.

        Args:
            run_list: the styled runs for this item

        Returns:
            this list, for chaining
        """
        return lib.folio_list_add_item_runs(self._handle, run_list._handle)

    def add_item_runs_with_sublist(self, run_list: RunList) -> Self:
        """
        Adds a list item with styled runs and returns a nested sub-list.

        Args:
            run_list: the styled runs for this item

        Returns:
            a new `List` representing the nested sub-list
        """
        handle = lib.folio_list_add_item_runs_with_sublist(
            self._handle, run_list._handle
        )
        return self._new_from_handle(handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
