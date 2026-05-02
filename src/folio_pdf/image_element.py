from folio_pdf.core import lib
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

    def set_size(self): ...

    def set_align(self): ...

    def set_alt_text(self): ...

    def set_object_fit(self): ...

    def set_object_position(self): ...
