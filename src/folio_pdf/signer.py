from folio_pdf.core import lib
from folio_pdf.object import AbstractFolioObject
import ctypes as ct


class Signer(AbstractFolioObject):
    _requires_close = True

    def __init__(self, key: bytes, cert_pem: bytes):
        self._signer_handle = lib.folio_signer_new_pem(
            ct.c_char_p(key),
            ct.c_int32(len(key)),
            ct.c_char_p(cert_pem),
            ct.c_int32(len(cert_pem)),
        )

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._signer_handle)

    def close(self):
        lib.folio_signer_free(self.handle)

    @classmethod
    def new_pkcs12(cls, data: bytes, password: str):
        obj = cls.__new__(cls)
        obj._signer_handle = lib.folio_signer_new_pkcs12(
            ct.c_char_p(data), ct.c_int32(len(data)), ct.c_char_p(password.encode())
        )
        return obj
