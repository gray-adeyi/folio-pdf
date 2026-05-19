"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import PadesLevels
from folio_pdf.exceptions import SignerOptionsException
from folio_pdf.ocsp_client import OCSPClient
from folio_pdf.signer import Signer
from folio_pdf.tsa_client import TSAClient

lib.folio_sign_opts_new.argtypes = [ct.c_uint64, ct.c_int32]
lib.folio_sign_opts_new.restype = ct.c_uint64

lib.folio_sign_opts_set_name.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_sign_opts_set_name.restype = ct.c_int32

lib.folio_sign_opts_set_reason.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_sign_opts_set_reason.restype = ct.c_int32

lib.folio_sign_opts_set_location.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_sign_opts_set_location.restype = ct.c_int32

lib.folio_sign_opts_set_contact_info.argtypes = [ct.c_uint64, ct.c_char_p]
lib.folio_sign_opts_set_contact_info.restype = ct.c_int32

lib.folio_sign_opts_set_tsa.argtypes = [ct.c_uint64, ct.c_uint64]
lib.folio_sign_opts_set_tsa.restype = ct.c_int32

lib.folio_sign_opts_set_ocsp.argtypes = [ct.c_uint64, ct.c_uint64]
lib.folio_sign_opts_set_ocsp.restype = ct.c_int32

lib.folio_sign_opts_free.argtypes = [ct.c_uint64]
lib.folio_sign_opts_free.restype = None


class SignerOptions(AbstractFolioObject):
    """
    Configurable signature options passed to the sign callback.
    Set name, reason, location, contact info, TSA, and OCSP.
    """

    _requires_close = True

    def __init__(self, signer: Signer, level: PadesLevels):
        self.__handle = lib.folio_sign_opts_new(signer._handle, ct.c_int32(level.value))

    @_with_error_handling(SignerOptionsException)
    def name(self, name: str):
        """Sets the signer's name.

        Args:
            name: the signer's name

        Returns:
            this signer options, for chaining
        """
        return lib.folio_sign_opts_set_name(ct.c_char_p(name.encode()))

    @_with_error_handling(SignerOptionsException)
    def reason(self, reason: str):
        """Sets the reason for signing.

        Args:
            reason: the reason for signing

        Returns:
             this signer options, for chaining
        """
        return lib.folio_sign_opts_set_reason(ct.c_char_p(reason.encode()))

    @_with_error_handling(SignerOptionsException)
    def location(self, location: str):
        """Sets the signing location.

        Args:
            location: the signing location

        Returns:
            this signer options, for chaining
        """
        return lib.folio_sign_opts_set_location(ct.c_char_p(location.encode()))

    @_with_error_handling(SignerOptionsException)
    def contact_info(self, info: str):
        """Sets contact information.

        Args:
            info: the signer's contact info

        Returns:
            this signer options, for chaining
        """
        return lib.folio_sign_opts_set_contact_info(ct.c_char_p(info.encode()))

    @_with_error_handling(SignerOptionsException)
    def tsa(self, tsa: TSAClient):
        """Sets a TSA (Time Stamp Authority) client for timestamped signatures.

        Args:
            tsa: the `TSAClient`

        Returns:
            this signer options, for chaining
        """
        return lib.folio_sign_opts_set_tsa(tsa._handle)

    @_with_error_handling(SignerOptionsException)
    def ocsp(self, ocsp: OCSPClient):
        """Sets an OCSP client for revocation checking.

        Args:
            ocsp: the `OCSPClient`

        Returns:
            this signer options, for chaining
        """
        return lib.folio_sign_opts_set_ocsp(ocsp._handle)

    def close(self):
        lib.folio_sign_opts_free(self._handle)

    @property
    def _handle(self) -> ct.c_uint64:
        return ct.c_uint64(self.__handle)
