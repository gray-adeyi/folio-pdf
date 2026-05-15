"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Alignments
from folio_pdf.exceptions import ImageElementException

from .image import Image


class ImageElement(AbstractFolioObject):
    _requires_free = True

    def __init__(self, img: Image):
        self.__handle = lib.folio_image_element_new(img._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)

    def close(self):
        lib.folio_image_element_free(self._handle)

    @_with_error_handling(ImageElementException)
    def size(self, width: float, height: float):
        return lib.folio_image_element_set_size(
            self._handle, ct.c_double(width), ct.c_double(height)
        )

    @_with_error_handling(ImageElementException)
    def align(self, align: Alignments):
        return lib.folio_image_element_set_align(self._handle, ct.c_int32(align))

    @_with_error_handling(ImageElementException)
    def alt_text(self, text: str):
        return lib.folio_image_element_set_align(
            self._handle, ct.c_char_p(text.encode())
        )

    @_with_error_handling(ImageElementException)
    def object_fit(self, fit: str):
        return lib.folio_image_element_set_object_fit(
            self._handle, ct.c_char_p(fit.encode())
        )

    @_with_error_handling(ImageElementException)
    def object_position(self, pos: str):
        return lib.folio_image_element_set_object_position(
            self._handle, ct.c_char_p(pos.encode())
        )
