"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

import ctypes as ct

from folio_pdf.core import AbstractFolioObject, _with_error_handling, lib
from folio_pdf.enums import Pades
from folio_pdf.exceptions import SignerOptionsException
from folio_pdf.ocsp_client import OCSPClient
from folio_pdf.signer import Signer
from folio_pdf.tsa_client import TSAClient


class SignerOptions(AbstractFolioObject):
    _requires_close = True

    def __init__(self, signer: Signer, level: Pades):
        self._signer_options_handle = lib.folio_sign_opts_new(
            signer.handle, ct.c_int32(level.value)
        )

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._signer_options_handle)

    def close(self):
        lib.folio_sign_opts_free(self.handle)

    @_with_error_handling(SignerOptionsException)
    def set_name(self, name: str):
        return lib.folio_sign_opts_set_name(ct.c_char_p(name.encode()))

    @_with_error_handling(SignerOptionsException)
    def set_reason(self, reason: str):
        return lib.folio_sign_opts_set_reason(ct.c_char_p(reason.encode()))

    @_with_error_handling(SignerOptionsException)
    def set_location(self, location: str):
        return lib.folio_sign_opts_set_location(ct.c_char_p(location.encode()))

    @_with_error_handling(SignerOptionsException)
    def set_contact_info(self, info: str):
        return lib.folio_sign_opts_set_contact_info(ct.c_char_p(info.encode()))

    @_with_error_handling(SignerOptionsException)
    def set_tsa(self, tsa: TSAClient):
        return lib.folio_sign_opts_set_tsa(tsa.handle)

    @_with_error_handling(SignerOptionsException)
    def set_ocsp(self, ocsp: OCSPClient):
        return lib.folio_sign_opts_set_ocsp(ocsp.handle)
