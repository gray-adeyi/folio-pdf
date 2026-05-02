from folio_pdf.core import lib
from folio_pdf.object import AbstractFolioObject
import ctypes as ct


class PDFReader(AbstractFolioObject):
    _requires_close = True

    def __init__(self):
        self._reader_handle = -1

    @property
    def handle(self) -> ct.c_uint64:
        return ct.c_uint64(self._reader_handle)

    def close(self):
        lib.folio_reader_free(self.handle)

    @classmethod
    def parse(cls): ...

    @property
    def page_count(self): ...

    @property
    def version(self): ...

    @property
    def info_title(self): ...

    @property
    def info_author(self): ...

    def extract_text(self): ...

    def page_width(self): ...

    def page_height(self): ...

    def structure_tree(self): ...

    def text_spans(self): ...

    def images(self): ...

    def paths(self): ...
