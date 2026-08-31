"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct
import sys

from folio_pdf.core import AbstractFolioObject, lib

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


lib.folio_signer_new_pem.argtypes = [ct.c_void_p, ct.c_int32, ct.c_void_p, ct.c_int32]
lib.folio_signer_new_pem.restype = ct.c_uint64

lib.folio_signer_new_pkcs12.argtypes = [
    ct.c_void_p,
    ct.c_int32,
    ct.c_void_p,
    ct.c_int32,
]
lib.folio_signer_new_pkcs12.restype = ct.c_uint64

lib.folio_signer_free.argtypes = [ct.c_uint64]
lib.folio_signer_free.restype = None


class Signer(AbstractFolioObject):
    """
    Signs PDF documents with PAdES-compliant digital signatures.
    """

    _requires_close = True
    _binding_resource_free_fn = lib.folio_signer_free

    def __init__(self, key: bytes, cert_pem: bytes):
        """
        Creates a signer from PEM-encoded private key and certificate.

        Args:
            key_pem: PEM-encoded private key bytes
            cert_pem: PEM-encoded certificate bytes (may include chain)

        Returns:
            a new `PDFSigner`
        """
        self._is_closed = False
        self.__handle = lib.folio_signer_new_pem(
            ct.c_char_p(key),
            ct.c_int32(len(key)),
            ct.c_char_p(cert_pem),
            ct.c_int32(len(cert_pem)),
        )

    @classmethod
    def new_pkcs12(cls, data: bytes, password: str) -> Self:
        """
        Creates a signer from a PKCS#12 (.p12 / .pfx) keystore.

        Args:
            data: the raw PKCS#12 bytes
            password: the keystore password (may be empty)

        Returns:
            a new `PDFSigner`
        """
        obj = cls.__new__(cls)
        obj._is_closed = False
        obj.__handle = lib.folio_signer_new_pkcs12(
            ct.c_char_p(data), ct.c_int32(len(data)), ct.c_char_p(password.encode())
        )
        return obj

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
