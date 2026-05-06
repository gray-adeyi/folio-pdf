"""
Copyright 2026 Gbenga Adeyi and Folio PDF Authors
SPDX-License-Identifier: Apache-2.0
"""

from folio_pdf.core import lib

from abc import abstractmethod
import ctypes as ct


class AbstractFolioObject:
    _requires_close: bool

    @property
    @abstractmethod
    def handle(self) -> ct.c_uint64:
        """Returns the object handle"""
        ...

    def close(self):
        err_msg = (
            "close method has not been implemented for folio object"
            if self._requires_close
            else "folio object does not require close"
        )
        raise NotImplementedError(err_msg)

    def _read_from_obj_buffer(self, buf: int):
        size = lib.folio_buffer_len(buf)
        ptr = lib.folio_buffer_data(buf)
        data = ct.string_at(ptr, size)
        lib.folio_buffer_free(buf)
        return data

    def __enter__(self):
        return self

    def __exit__(self):
        if self._requires_close:
            self.close()
