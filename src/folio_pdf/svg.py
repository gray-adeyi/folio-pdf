from folio_pdf.core import lib
from folio_pdf.object import AbstractFolioObject
import ctypes as ct


class SVG(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._svg_handle = -1

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._svg_handle)

    def close(self):
        lib.folio_svg_free(self.handle)

    @classmethod
    def parse(cls): ...

    @classmethod
    def parse_bytes(cls): ...

    @property
    def width(self): ...

    @property
    def height(self): ...
