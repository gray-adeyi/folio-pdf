from folio_pdf.core import lib
from folio_pdf.object import AbstractFolioObject
import ctypes as ct


class FlexItem(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._flex_handle = -1

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._flex_handle)

    def close(self):
        lib.folio_flex_item_free(self.handle)

    def set_grow(self): ...

    def set_shrink(self): ...

    def set_basis(self): ...

    def set_align_self(self): ...

    def set_margin(self): ...
