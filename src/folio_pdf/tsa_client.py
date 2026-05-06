from folio_pdf.core import lib
from folio_pdf.object import AbstractFolioObject
import ctypes as ct


class TSAClient(AbstractFolioObject):
    _requires_close = True

    def __init__(self, url: str):
        self._tsa_client_handle = lib.folio_tsa_client_new(ct.c_char_p(url.encode()))

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._tsa_client_handle)

    def close(self):
        lib.folio_tsa_client_free(self.handle)
