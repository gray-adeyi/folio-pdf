"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.exceptions import FormException
from folio_pdf.form_field import FormField

lib.folio_form_new.argtypes = []
lib.folio_form_new.restype = ct.c_uint64

lib.folio_form_free.argtypes = [ct.c_uint64]
lib.folio_form_free.restype = None

lib.folio_form_add_text_field.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_int32,
]
lib.folio_form_add_text_field.restype = ct.c_int32

lib.folio_form_add_checkbox.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_int32,
    ct.c_int32,
]
lib.folio_form_add_checkbox.restype = ct.c_int32

lib.folio_form_add_signature.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_int32,
]
lib.folio_form_add_signature.restype = ct.c_int32

lib.folio_form_add_multiline_text_field.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_int32,
]
lib.folio_form_add_multiline_text_field.restype = ct.c_int32

lib.folio_form_add_password_field.argtypes = [
    ct.c_uint64,
    ct.c_char_p,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_double,
    ct.c_int32,
]
lib.folio_form_add_password_field.restype = ct.c_int32


class Form(AbstractFolioObject):
    """
    Represents an interactive PDF form with fields such as text inputs, checkboxes,
    dropdowns, and radio buttons.
    """

    _requires_close = True

    def __init__(self):
        self.__handle = lib.folio_form_new()

    @_with_error_handling(FormException)
    def add_text_field(
        self, name: str, x1: float, y1: float, x2: float, y2: float, page_index: int
    ) -> "Form":
        """
        Adds a single-line text field to the form.

        Args:
            name: the unique field name
            x1: left coordinate of the field rectangle in points
            y1: bottom coordinate of the field rectangle in points
            x2: right coordinate of the field rectangle in points
            y2: top coordinate of the field rectangle in points
            page_index: zero-based page index where the field is placed

        Returns:
            this form, for chaining
        """
        return lib.folio_form_add_text_field(
            self._handle,
            ct.c_char_p(name.encode()),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_int32(page_index),
        )

    @_with_error_handling(FormException)
    def add_checkbox(
        self,
        name: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        page_index: int,
        checked: bool,
    ) -> "Form":
        """
        Adds a checkbox field to the form.

        Args:
            name: the unique field name
            x1: left coordinate in points
            y1: bottom coordinate in points
            x2: right coordinate in points
            y2: top coordinate in points
            page_index: zero-based page index
            checked: initial checked state

        Returns:
            this form, for chaining
        """
        return lib.folio_form_add_checkbox(
            self._handle,
            ct.c_char_p(name.encode()),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_int32(page_index),
            ct.c_int32(checked),
        )

    @_with_error_handling(FormException)
    def add_dropdown(
        self,
        name: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        page_index: int,
        options: list[str],
    ) -> "Form":
        """
        Adds a dropdown (combo box) field with the given options to the form.

        Args:
            name: the unique field name
            x1: left coordinate in points
            y1: bottom coordinate in points
            x2: right coordinate in points
            y2: top coordinate in points
            page_index: zero-based page index
            options: the selectable option strings

        Returns:
            this form, for chaining
        """
        CharPArray = ct.c_char_p * len(options)
        lib.folio_form_add_dropdown.argtypes = [
            ct.c_uint64,
            ct.c_char_p,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_int32,
            CharPArray,
            ct.c_int32,
        ]
        lib.folio_form_add_dropdown.restype = ct.c_int32
        return lib.folio_form_add_dropdown(
            self._handle,
            ct.c_char_p(name.encode()),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_int32(page_index),
            CharPArray(options),
            len(options),
        )

    @_with_error_handling(FormException)
    def add_signature(
        self,
        name: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        page_index: int,
    ) -> "Form":
        """
        Adds a digital signature field to the form.

        Args:
            name: the unique field name
            x1: left coordinate in points
            y1: bottom coordinate in points
            x2: right coordinate in points
            y2: top coordinate in points
            page_index: zero-based page index

        Returns:
            this form, for chaining
        """
        return lib.folio_form_add_signature(
            self._handle,
            ct.c_char_p(name.encode()),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_int32(page_index),
        )

    @_with_error_handling(FormException)
    def add_multiline_text_field(
        self,
        name: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        page_index: int,
    ) -> "Form":
        """
        Adds a multi-line text area field to the form.

        Args:
            name: the unique field name
            x1: left coordinate in points
            y1: bottom coordinate in points
            x2: right coordinate in points
            y2: top coordinate in points
            page_index: zero-based page index

        Returns:
            this form, for chaining
        """
        return lib.folio_form_add_multiline_text_field(
            self._handle,
            ct.c_char_p(name.encode()),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_int32(page_index),
        )

    @_with_error_handling(FormException)
    def add_password_field(
        self,
        name: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        page_index: int,
    ) -> "Form":
        """
        Adds a password input field (masked text) to the form.

        Args:
            name: the unique field name
            x1: left coordinate in points
            y1: bottom coordinate in points
            x2: right coordinate in points
            y2: top coordinate in points
            page_index: zero-based page index

        Returns:
            this form, for chaining
        """
        return lib.folio_form_add_password_field(
            self._handle,
            ct.c_char_p(name.encode()),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_int32(page_index),
        )

    @_with_error_handling(FormException)
    def add_listbox(
        self,
        name: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        page_index: int,
        options: list[str],
    ) -> "Form":
        """
        Adds a scrollable list box field with the given options to the form.

        Args:
            name: the unique field name
            x1: left coordinate in points
            y1: bottom coordinate in points
            x2: right coordinate in points
            y2: top coordinate in points
            page_index: zero-based page index
            options: the selectable option strings

        Returns:
            this form, for chaining
        """
        CharPArray = ct.c_char_p * len(options)
        lib.folio_form_add_listbox.argtypes = [
            ct.c_uint64,
            ct.c_char_p,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_int32,
            CharPArray,
            ct.c_int32,
        ]
        lib.folio_form_add_listbox.restype = ct.c_int32
        return lib.folio_form_add_listbox(
            self._handle,
            ct.c_char_p(name.encode()),
            ct.c_double(x1),
            ct.c_double(y1),
            ct.c_double(x2),
            ct.c_double(y2),
            ct.c_int32(page_index),
            CharPArray(options),
            ct.c_int32(len(options)),
        )

    @_with_error_handling(FormException)
    def add_radio_group(
        self, name: str, values: list[str], rects: list[float], page_indices: list[int]
    ) -> "Form":
        """
        Adds a radio button group to the form. Each radio button is defined by a
        value, a bounding rectangle (four doubles in {@code rects}), and a page index.

        Args:
            name: the shared group field name
            values: the value associated with each radio button
            rects: flat array of {@code [x1, y1, x2, y2]} per button
            page_indices: zero-based page index for each button

        Returns:
            this form, for chaining
        """
        CharPArray = ct.c_char_p * len(values)
        DoubleArray = ct.c_char_p * len(rects)
        Int32Array = ct.c_char_p * len(page_indices)
        lib.folio_form_add_radio_group.argtypes = [
            ct.c_uint64,
            ct.c_char_p,
            CharPArray,
            DoubleArray,
            Int32Array,
            ct.c_int32,
        ]
        lib.folio_form_add_radio_group.restype = ct.c_int32
        return lib.folio_form_add_radio_group(
            self._handle,
            ct.c_char_p(name.encode()),
            CharPArray(values),
            DoubleArray(rects),
            Int32Array(page_indices),
            ct.c_int32(len(values)),
        )

    @_with_error_handling(FormException)
    def add_field(self, field: FormField) -> "Form":
        """
        Adds a pre-configured {@link FormField} to this form.

        Args:
            field: the field to add

        Returns:
            this form, for chaining
        """
        return lib.folio_form_add_field(self._handle, field._handle)

    def close(self):
        lib.folio_form_free(self._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
