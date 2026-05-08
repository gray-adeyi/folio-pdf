# Folio PDF

[![Downloads](https://static.pepy.tech/badge/folio-pdf)](https://pepy.tech/project/folio-pdf)
[![Downloads](https://static.pepy.tech/badge/folio-pdf/month)](https://pepy.tech/project/folio-pdf)
[![Downloads](https://static.pepy.tech/badge/folio-pdf/week)](https://pepy.tech/project/folio-pdf)

> A Python PDF library powered by bindings to the Go-based [Folio PDF library](https://github.com/carlos7ags/folio). It provides features such as a layout engine, HTML-to-PDF rendering, forms, digital signatures, barcodes, and PDF/A support.
>
> Folio PDF is currently under active development, so some functionality may not yet work as expected and APIs may change over time. Suggestions and bug reports are welcome at [folio-pdf issues](https://github.com/gray-adeyi/folio-pdf/issues).


## Installation

### With [uv](https://docs.astral.sh/uv/)
```bash
uv add folio-pdf
```

### With pip

```bash
pip install folio-pdf
```

## Usage

## Building a pdf from scratch
```python
from folio_pdf import Document, Font

doc = Document.new_a4()
doc.set_title("PDF Document Example")
doc.set_watermark("Made with Folio PDF")

page = doc.add_page()
font = Font(StandardPDFFonts.HELVETICA_BOLD)
page.add_text("I love folio pdf", font, 14, 100, 100)
doc.save("result.pdf")
```

## Generating a pdf from html

```python
from folio_pdf import html_to_pdf

html = '''
<h1 style="color: red;">Hello, world!</h1>
'''
html_to_pdf(html, "result.pdf")
# see generated result.pdf the generated pdf
```
