from folio_pdf.object import AbstractFolioObject
import ctypes as ct


class AreaBreak(AbstractFolioObject):
    _requires_close = False

    def __init__(self):
        self._area_break_handle = -1

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._area_break_handle)
