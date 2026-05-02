from folio_pdf.object import AbstractFolioObject
from folio_pdf.core import lib
import ctypes as ct


class RunList(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._run_list_handle = -1

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._run_list_handle)

    def close(self):
        lib.folio_run_list_free(self.handle)

    def add(self): ...

    def add_embedded(self): ...

    def add_link(self): ...

    def last_set_underline(self): ...

    def last_set_strikethrough(self): ...

    def last_set_letter_spacing(self): ...

    def last_set_background_color(self): ...
