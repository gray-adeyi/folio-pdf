from folio_pdf.element import AbstractPDFElement


class Table(AbstractPDFElement):
    def __init__(self):
        self._table_ptr = ...
