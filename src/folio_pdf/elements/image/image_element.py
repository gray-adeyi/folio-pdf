"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
from typing import Literal

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Alignments
from folio_pdf.exceptions import ImageElementException

from .image import Image

lib.folio_image_element_new.argtypes = [ct.c_uint64]
lib.folio_image_element_new.restype = ct.c_uint64

lib.folio_image_element_set_size.argtypes = [ct.c_uint64, ct.c_double, ct.c_double]
lib.folio_image_element_set_size.restype = ct.c_int32

lib.folio_image_element_set_align.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_image_element_set_align.restype = ct.c_int32

lib.folio_image_element_set_alt_text.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_image_element_set_alt_text.restype = ct.c_int32

lib.folio_image_element_set_object_fit.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_image_element_set_object_fit.restype = ct.c_int32

lib.folio_image_element_set_object_position.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_image_element_set_object_position.restype = ct.c_int32

lib.folio_image_element_free.argtypes = [ct.c_uint64]
lib.folio_image_element_free.restype = None


class ImageElement(AbstractFolioObject):
    """
    Represents an image element that can be added to a `Document` or `Div`.
    """

    _requires_free = True

    def __init__(self, img: Image):
        self.__handle = lib.folio_image_element_new(img._handle)

    @_with_error_handling(ImageElementException)
    def size(self, width: float, height: float):
        """
        Sets the rendered size of the image in the document.

        Args:
            width: display width in points
            height: display height in points

        Returns:
            this image element, for chaining
        """
        return lib.folio_image_element_set_size(
            self._handle, ct.c_double(width), ct.c_double(height)
        )

    @_with_error_handling(ImageElementException)
    def align(self, align: Alignments):
        """
        Sets the horizontal alignment of the image on the page.

        Args:
            align: the desired `Alignments` variant

        Returns:
            this image element, for chaining
        """
        return lib.folio_image_element_set_align(self._handle, ct.c_int32(align))

    @_with_error_handling(ImageElementException)
    def alt_text(self, text: str):
        """
        Sets alternative text for PDF/UA accessibility.

        Args:
            text: description of this image for screen readers

        Returns:
            this image element, for chaining
        """
        return lib.folio_image_element_set_align(
            self._handle, ct.c_char_p(text.encode())
        )

    @_with_error_handling(ImageElementException)
    def object_fit(
        self, fit: Literal["contain", "cover", "fill", "none", "scale-down"]
    ):
        """
        Sets the CSS-style `object-fit` behaviour for this image.

        Args:
            fit: one of `"contain"`, `"cover"`, `"fill"`,
            `"none"`, or `"scale-down"`

        Returns:
            this image element, for chaining
        """
        return lib.folio_image_element_set_object_fit(
            self._handle, ct.c_char_p(fit.encode())
        )

    @_with_error_handling(ImageElementException)
    def object_position(self, pos: str):
        """
        Sets the CSS-style `object-position` for this image
        (e.g., `"center"`, `"top left"`).

        Args:
            pos: the position string

        Returns:
            this image element, for chaining
        """
        return lib.folio_image_element_set_object_position(
            self._handle, ct.c_char_p(pos.encode())
        )

    def close(self):
        lib.folio_image_element_free(self._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
