from folio_pdf.reader import PDFReader
from folio_pdf.core import lib
from folio_pdf.object import AbstractFolioObject
import ctypes as ct


class FormFiller(AbstractFolioObject):
    _requires_close = True

    def __init__(self, reader: PDFReader):
        self._form_handle = lib.folio_form_filler_new(reader.handle)

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._form_handle)

    def close(self):
        lib.folio_form_filler_free(self.handle)

    def field_names(self): ...

    def get_value(self): ...

    def set_value(self): ...

    def set_checkbox(self): ...
