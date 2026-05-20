# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 0.0.2 - 2026-05-15

## Added

- `Color` class for representing color values
- Docstrings for all public APIs

### Changed

- All public APIs using discrete `r,g,b` parameters to use `Color` dataclass
- `Column` to `Columns`
- Folio object personalized handle attribute name to `__handle`
- Folio object `handle` to `__handle`
- `html_parse_css_length` to `parse_css_length`

### Removed 

- `Document.new_a4` and replaced with `Document.new_with_size`
- `Document.set_header`, `Document.set_footer`
- `set_` prefix from public APIs

## [0.0.1] - 2026-04-23

### Added



## [0.0.1] - 2026-04-09


### Added



[0.0.2]: https://github.com/gray-adeyi/folio-pdf/releases/tag/v0.0.2
[0.0.1]: https://github.com/gray-adeyi/folio-pdf/releases/tag/v0.0.1
[0.0.0]: https://github.com/gray-adeyi/folio-pdf/releases/tag/v0.0.0
