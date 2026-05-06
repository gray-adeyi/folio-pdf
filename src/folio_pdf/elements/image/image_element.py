"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

from folio_pdf.exceptions import ImageElementException

from folio_pdf.enums import Alignments

from folio_pdf.core import lib, _with_error_handling
from folio_pdf.image import Image
from folio_pdf.object import AbstractFolioObject
import ctypes as ct


class ImageElement(AbstractFolioObject):
    _requires_free = True

    def __init__(self, img: Image):
        self._image_element_handle = lib.folio_image_element_new(img.handle)

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._image_element_handle)

    def close(self):
        lib.folio_image_element_free(self.handle)

    @_with_error_handling(ImageElementException)
    def set_size(self, width: float, height: float):
        return lib.folio_image_element_set_size(
            self.handle, ct.c_double(width), ct.c_double(height)
        )

    @_with_error_handling(ImageElementException)
    def set_align(self, align: Alignments):
        return lib.folio_image_element_set_align(self.handle, ct.c_int32(align))

    @_with_error_handling(ImageElementException)
    def set_alt_text(self, text: str):
        return lib.folio_image_element_set_align(
            self.handle, ct.c_char_p(text.encode())
        )

    @_with_error_handling(ImageElementException)
    def set_object_fit(self, fit: str):
        return lib.folio_image_element_set_object_fit(
            self.handle, ct.c_char_p(fit.encode())
        )

    @_with_error_handling(ImageElementException)
    def set_object_position(self, pos: str):
        return lib.folio_image_element_set_object_position(
            self.handle, ct.c_char_p(pos.encode())
        )
