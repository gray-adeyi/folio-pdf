"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
import sys

from folio_pdf.color import Color
from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.exceptions import FormFieldException

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

_ErrorCode = int

lib.folio_form_create_text_field.argtypes = [
    ct.c_char_p,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_int32,
]
lib.folio_form_create_text_field.restype = ct.c_uint64

lib.folio_form_create_checkbox.argtypes = [
    ct.c_char_p,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_int32,
    ct.c_int32,
]
lib.folio_form_create_checkbox.restype = ct.c_uint64

lib.folio_form_field_free.argtypes = [ct.c_uint64]
lib.folio_form_field_free.restype = None

lib.folio_form_field_set_value.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_form_field_set_value.restype = ct.c_int32

lib.folio_form_field_set_read_only.argtypes = [ct.c_uint64]
lib.folio_form_field_set_read_only.restype = ct.c_int32

lib.folio_form_field_set_required.argtypes = [ct.c_uint64]
lib.folio_form_field_set_required.restype = ct.c_int32

lib.folio_form_field_set_background_color.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_form_field_set_background_color.restype = ct.c_int32

lib.folio_form_field_set_border_color.argtypes = [
    ct.c_uint64,
    ct.c_double,
    ct.c_double,
    ct.c_double,
]
lib.folio_form_field_set_border_color.restype = ct.c_int32


class FormField(AbstractFolioObject):
    """
    Represents a configurable form field that can be added to a `Form`
    """

    _requires_close = True
    _binding_resource_free_fn = lib.folio_form_field_free

    def __init__(
        self, name: str, x1: float, y1: float, x2: float, y2: float, page_index: int
    ):
        """
        Creates a single-line text field.

        Args:
            name: the unique field name
            x1: left coordinate in points
            y1: bottom coordinate in points
            x2: right coordinate in points
            y2: top coordinate in points
            pageIndex: zero-based page index

        Returns:
            a new `FormField` representing the text field
        """
        self._is_closed = False
        self.__handle = lib.folio_form_create_text_field(
            ct.c_char_p(name.encode()),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_int32(page_index),
        )

    @classmethod
    def new_checkbox(
        cls,
        name: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        page_index: int,
        checked: bool,
    ) -> Self:
        """
        Creates a checkbox field.

        Args:
            name: the unique field name
            x1: left coordinate in points
            y1: bottom coordinate in points
            x2: right coordinate in points
            y2: top coordinate in points
            page_index zero-based page index
            checked: initial checked state

        Returns:
            a new `FormField` representing the checkbox
        """
        obj = cls.__new__(cls)
        obj._is_closed = False
        obj.__handle = lib.folio_form_create_checkbox(
            ct.c_char_p(name.encode()),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_int32(page_index),
            ct.c_int32(checked),
        )
        return obj

    @_with_error_handling(FormFieldException)
    def value(self, value: str) -> _ErrorCode:
        """
        Sets the default value for this field.

        Args:
            value: the initial field value

        Returns:
            this field, for chaining
        """
        return lib.folio_form_field_set_value(ct.c_char_p(value.encode()))

    @_with_error_handling(FormFieldException)
    def read_only(self) -> _ErrorCode:
        """
        Marks this field as read-only so users cannot edit it.

        Retruns:
            this field, for chaining
        """
        return lib.folio_form_field_set_read_only()

    @_with_error_handling(FormFieldException)
    def required(self) -> _ErrorCode:
        """
        Marks this field as required (must be filled before submission).

        Returns:
            this field, for chaining
        """
        return lib.folio_form_field_set_required()

    @_with_error_handling(FormFieldException)
    def background_color(self, color: Color) -> _ErrorCode:
        """
        Sets the background fill color of this field widget.

        Args:
            color: the background {@link Color}

        Returns:
            this field, for chaining
        """
        return lib.folio_form_field_set_background_color(
            self._handle,
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @_with_error_handling(FormFieldException)
    def border_color(self, color: Color) -> _ErrorCode:
        """
        Sets the border color of this field widget.

        Args:
            color: the border {@link Color}

        Returns:
            this field, for chaining
        """
        return lib.folio_form_field_set_border_color(
            self._handle,
            ct.c_double(color.r),
            ct.c_double(color.g),
            ct.c_double(color.b),
        )

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
