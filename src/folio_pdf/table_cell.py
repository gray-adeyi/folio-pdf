from folio_pdf.core import lib
from folio_pdf.object import AbstractFolioObject
import ctypes as ct


class TableCell(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._cell_handle = -1

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._cell_handle)

    def close(self):
        lib.folio_cell_free(self.handle)

    @classmethod
    def _new_from_handle(cls, cell_handle: int):
        obj = cls.__new__(cls)
        cls._cell_handle = cell_handle
        return obj

    def set_align(self): ...

    def set_padding(self): ...

    def set_padding_sides(self): ...

    def set_valign(self): ...

    def set_background(self): ...

    def set_colspan(self): ...

    def set_rowspan(self): ...

    def set_border(self): ...

    def set_borders(self): ...

    def set_width_hint(self): ...

    def set_border_radius(self): ...

    def set_border_radius_per_corner(self): ...
