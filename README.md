# Folio PDF

A PDF library for Python powered by bindings to [https://github.com/carlos7ags/folio](https://github.com/carlos7ags/folio) PDF library for Go: layout engine, HTML to PDF, forms, signatures, barcodes, and PDF/A.

Folio PDF only currently supports the following functions `html_to_pdf`, `html_to_buffer` & `parse_css_length` and is still in development.

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

```
```python
from folio_pdf import html_to_pdf

html = '''
<h1 style="color: red;">Hello, world!</h1>
'''
html_to_pdf(html, "result.pdf")
# see generated result.pdf the generated pdf
```
