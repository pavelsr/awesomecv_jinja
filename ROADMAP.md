# Roadmap

This document tracks planned features and improvements for awesomecv-jinja.

## Immediate (Sprint 1)

- [ ] Implement `dev/scripts/convert.py`:
  - Convert `.tex` → `.tex.j2` files
  - Replace hardcoded values with Jinja2 variables
  - Support all Awesome-CV fields

- [ ] Implement `dev/scripts/check.py`:
  - Validate delimiter compatibility
  - Check that `(((`, `((*`, `((#` do not appear in upstream `.tex` files
  - Document results

## Short term (Sprint 2)

- [x] Complete first template conversion: ✅ Done
  - ✅ resume.tex.j2, cv.tex.j2, coverletter.tex.j2 exist
  - ✅ All sections converted
  - ✅ Tests for all document types exist

- [x] Create working prototype: ✅ Done
  - ✅ Render from JSON/YAML (see `examples/demo.py`, `examples/pdf_example.py`)
  - ✅ Compile to PDF via xelatex/docker
  - ✅ Examples exist

## Mid term (Sprint 3-4)

- [ ] Improve API:
  - Add convenience functions `render_resume()`, `render_cv()`
  - Implement input data validation
  - Improve error messages with better context

- [ ] Documentation:
  - Complete API documentation
  - Create beginner tutorial
  - Add more usage examples

## Long term (Sprint 5+)

- [ ] Pydantic schemas:
  - Resume data schemas
  - CV data schemas
  - Auto-generated documentation from schemas
  - Runtime validation of input data

- [ ] Second template support:
  - Evaluate ModernCV template
  - Convert ModernCV to `.tex.j2` format
  - Ensure API compatibility across templates
  - Add tests for template switching

- [ ] CI/CD:
  - Set up GitHub Actions
  - Automated tests on pull requests
  - Automated checks for upstream updates
  - Automated release process

## Future considerations

These items are under consideration but not yet planned:

- Python 3.9 support (currently 3.10+)
- Integration with external services (LinkedIn export, etc.)
- Localization (i18n) for multiple languages
- Custom font support in templates
- Template customization API
- Web interface for CV generation

---
