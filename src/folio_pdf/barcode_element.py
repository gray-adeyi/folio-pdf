from folio_pdf.core import lib
from folio_pdf.object import AbstractFolioObject
import ctypes as ct


class BarcodeElement(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._barcode_handle = -1

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._barcode_handle)

    def close(self):
        lib.folio_barcode_element_free(self.handle)

    def set_height(self): ...

    def set_align(self): ...

    def set_alt_text(self): ...
