from folio_pdf.core import lib
from folio_pdf.object import AbstractFolioObject
import ctypes as ct


class Image(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._image_handle = -1

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._image_handle)

    def close(self):
        lib.folio_image_free(self.handle)

    @classmethod
    def load(cls): ...

    @classmethod
    def load_jpeg(cls): ...

    @classmethod
    def load_png(cls): ...

    @classmethod
    def load_tiff(cls): ...

    @classmethod
    def parse_jpeg(cls): ...

    @classmethod
    def parse_png(cls): ...

    def width(self): ...

    def height(self): ...
