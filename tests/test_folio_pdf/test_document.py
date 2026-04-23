from folio_pdf.document import Document
from unittest import TestCase


class DocumentTestCase(TestCase):
    def test_can_create_doument_instance(self):
        doc = Document(100, 100)
        self.assertGreater(doc._doc_ptr, 0)

    def test_can_create_a4_document_instance(self):
        doc = Document.new_a4()
        self.assertGreater(doc._doc_ptr, 0)

    def test_can_set_document_title(self):
        doc = Document.new_a4()
        doc.set_title("folio test document")

    def test_can_save(self):
        doc = Document.new_a4()
        doc.set_title("folio test document")
        doc.save("demo.pdf")
