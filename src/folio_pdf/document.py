from pathlib import Path
from typing import Callable
from folio_pdf.exceptions import DocumentException
from folio_pdf.enums import ErrorCodes
from folio_pdf.core import lib


def _with_error_handling(func: Callable):
    def wrapper(self, *args, **kwargs):
        res_code = func(self, *args, **kwargs)
        err = ErrorCodes(res_code)
        if err != ErrorCodes.OK:
            msg_bytes = lib.folio_last_error()
            raise DocumentException(str(msg_bytes))

    return wrapper


class Document:
    def __init__(self, width: float, height: float):
        self._doc_ptr = lib.folio_document_new(width, height)

    @classmethod
    def new_a4(cls):
        obj = cls.__new__(cls)
        cls._doc_ptr = lib.folio_document_new_a4()
        return obj

    @classmethod
    def _new_from_ptr(cls, doc_ptr: int):
        obj = cls.__new__(cls)
        cls._doc_ptr = doc_ptr
        return obj

    @_with_error_handling
    def set_title(self, value: str):
        return lib.folio_document_set_title(self._doc_ptr, value)

    @_with_error_handling
    def set_author(self, value: str):
        return lib.folio_document_author(self._doc_ptr, value)

    @_with_error_handling
    def set_margins(self, top: float, right: float, bottom: float, left: float):
        return lib.folio_document_set_margins(self._doc_ptr, top, right, bottom, left)

    def add_page(self):
        # TODO: Return Page obj
        lib.folio_document_add_page(self._doc_ptr)

    @_with_error_handling
    def add(self, element):
        return lib.folio_document_add(self._doc_ptr, element)

    @_with_error_handling
    def save(self, destination: str | Path):
        _destination = destination
        if isinstance(_destination, Path):
            _destination = _destination.as_posix()
        return lib.folio_document_save(self._doc_ptr, _destination)

    def close(self):
        lib.folio_document_free(self._doc_ptr)

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()
