from folio_pdf.core import lib
from folio_pdf.object import AbstractFolioObject
import ctypes as ct


class List(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._list_handle = -1

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._list_handle)

    def close(self):
        lib.folio_list_free(self.handle)

    def set_style(self): ...

    def set_indent(self): ...

    def set_leading(self): ...

    def add_item(self): ...

    def add_nested_item(self): ...

    def add_item_runs(self): ...

    def add_item_runs_with_sublist(self): ...
