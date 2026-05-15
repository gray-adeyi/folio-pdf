import os
from pathlib import Path
from unittest import TestCase
from uuid import uuid4

from folio_pdf import Font
from folio_pdf.document import Document
from folio_pdf.enums import PageSizes, StandardPDFFonts


class DocumentTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = Document.new_with_size(PageSizes.A4)

    @classmethod
    def tearDownClass(cls):
        cls.doc.close()

    def test_can_create_doument_instance(self):
        with Document(100, 100) as doc:
            self.assertGreater(doc.handle.value, 0)

    def test_can_create_a4_document_instance(self):
        with Document.new_with_size(PageSizes.A4) as doc:
            self.assertGreater(doc.handle.value, 0)

    def test_can_set_document_title(self):
        self.assertIsInstance(self.doc.title("folio test document"), Document)

    def test_can_save(self):
        doc = Document.new_with_size(PageSizes.A4)
        doc.title("folio test document")
        doc.watermark("Folio pdf test")
        page = doc.add_page()
        font = Font(StandardPDFFonts.HELVETICA_BOLD)
        page.add_text("I love folio pdf", font, 14, 100, 100)
        filename = f"{uuid4()}.pdf"
        doc.save(filename)
        filepath = Path(filename)
        self.assertTrue(filepath.exists())  # saved pdf does exist
        self.assertTrue(filepath.is_file())  # saved pdf is file
        self.assertGreater(filepath.stat().st_size, 0)  # saved pdf is non-empty
        os.remove(filepath)
