# AI Coding Assistant Context & Rules

This document provides context for AI coding assistants (Claude Code, Gemini CLI, GitHub Copilot, Cursor, etc.) to understand **awesomecv_jinja** project and assist with development.

## AI Assistant Behavior Rules

**When user asks a question (ends with `?`):** Do NOT make code changes. Analyze codebase and answer based on code analysis and project context.

---

## 0. Documentation Maintenance Rules

### Required Structure

This file (AGENTS.md) **MUST** always contain these sections:

1. **Project Overview** — Project goal, Repository Map, Technology Stack (Python version, tooling, key dependencies)
2. **Build and Test Commands** — Setup, lint, test, types
3. **Code Style Guidelines** — Preferred patterns and anti-patterns
4. **Testing Instructions** — Test structure, writing tests, running tests
5. **Security Considerations** — LaTeX escaping, logging rules, input validation

### Keep Documentation Synchronized

**CRITICAL:** Always verify documentation accuracy against current codebase.

- Before any documentation edit, check if the described behavior matches actual code
- When modifying code, immediately update relevant documentation sections
- Cross-reference between `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, and `docs/`
- Run `uv run python dev/scripts/check_templates.py` to validate templates

### Update Repository Map

**ALWAYS** update the "Repository Map" section when:

- Adding new files or directories
- Removing files or directories
- Moving files to different locations

**Rules:**

- Every file/directory MUST have a comment explaining its purpose
- Use consistent comment style: `# Brief description`
- Keep the tree structure visually aligned
- Group related items together

### ADR Management

**When creating a new ADR in `docs/adr/`:** **MUST** use `docs/adr/template.md` and **MUST** add entry to "ADR Index" in `docs/adr/README.md`. Use naming `XXXX-title.md` (sequential number).

### Size Limit

Keep `AGENTS.md` **under 500 lines**.

If approaching limit:

- Move detailed examples to separate `docs/` files
- Link to external documentation for third-party tools
- Remove outdated or redundant information
- Consolidate similar sections

### Documentation Files

These files constitute project documentation:

- `README.md` — User-facing documentation (installation, usage, features)
- `AGENTS.md` — AI assistant context (this file)
- `CONTRIBUTING.md` — Contribution guidelines
- `docs/` — Detailed documentation (CLI usage, API reference, etc.)
- **Python docstrings** — All public modules, classes, and functions must have docstrings (PEP 257)

**Principle:** Use cases, architecture, design decisions, and philosophy go to Markdown (important → `README.md`, secondary → `docs/`). Technical API details go to Python docstrings.

| Documentation Type | Location |
|--------------------|----------|
| Installation, quick start | `README.md` |
| Features overview | `README.md` |
| Top 1-3 use cases | `README.md` |
| CLI usage guide | `docs/cli_usage.md` |
| Other use cases, tutorials | `docs/` |
| Architecture decisions (ADR) | `docs/adr/` |
| Contribution workflow | `CONTRIBUTING.md` |
| Function parameters, return types | Python docstrings |
| Class/method behavior | Python docstrings |
| Exceptions raised | Python docstrings |
| Code examples (short) | Python docstrings |

### Documentation Language and Style

All project documentation MUST be written in English.

Documentation MUST follow developer-first Plain Technical English and RFC-style conventions.

The following requirements apply:

- Sentences MUST be short and clear.
- Each paragraph MUST express a single idea.
- Active voice MUST be used.
- Imperative mood MUST be used for instructions.
- Rare words and idioms MUST NOT be used.
- Colloquial language MUST NOT be used.
- Humor and jokes MUST NOT be used.
- Marketing or emotional language MUST NOT be used.
- Documentation MUST be clear, neutral, and unambiguous, and MUST be easy to understand for non-native English speakers.

### Avoid Duplication

**README.md** is for users. **AGENTS.md** is for AI assistants and developers.

- `README.md` may reference `AGENTS.md` sections (max 3 links)
- Never duplicate entire sections between files
- Link to detailed docs instead of repeating content
- Keep `README.md` concise and user-friendly

### README.md Structure Requirements

**MUST** always include:

1. **Table of Contents** — TOC with links to all sections (after title, before Features)
2. **Features** section at the top with emoji illustrations (e.g., 🚀 Fast, 🎨 Customizable)
3. **Installation** section with clear setup instructions
4. **CLI Usage** section (must appear BEFORE "Python API")
5. **Python API** section with code examples

**Order matters:** CLI Usage → Python API (users try CLI first)

**Size limit:** Keep `README.md` **under 150 lines**. If approaching limit, move details to `docs/` or link to examples.

**TOC Maintenance:** **ALWAYS** update the Table of Contents in `README.md` when:
- Adding new sections
- Removing sections
- Renaming sections
- Adding/removing subsections under Python API

The TOC MUST accurately reflect the current structure of `README.md`.

---

## 1. Project Overview

### Project Goal

Converts LaTeX resume templates to Jinja2. Input: JSON/YAML data, Output: `.tex` or `.pdf` file.

Based on [Awesome-CV](https://github.com/posquit0/Awesome-CV). Future: more templates.

### Terminology

- **Template** — LaTeX styles (Awesome-CV, ModernCV)
- **Document type** — resume, cv, coverletter
- **Section** — reusable block (education, experience, skills)

### Repository Map

```
awesomecv_jinja/
├── src/awesomecv_jinja/
│   ├── __init__.py              # Public API exports
│   ├── cli.py                   # CLI entry point (acv command)
│   ├── compiler.py              # PDF compilation (xelatex/docker)
│   ├── config.py                # Jinja2 environment setup
│   ├── exceptions.py            # Custom exceptions
│   ├── pipeline.py              # render_pdf() - data → PDF
│   ├── renderer.py              # Renderer class, render()
│   ├── samples.py               # Sample data for testing
│   ├── py.typed                 # PEP 561 marker
│   └── templates/
│       └── awesome_cv/
│           ├── awesome-cv.cls   # LaTeX class file
│           ├── resume.tex.j2    # Document types
│           ├── cv.tex.j2
│           ├── coverletter.tex.j2
│           └── sections/        # Reusable sections
│               ├── education.tex.j2
│               ├── experience.tex.j2
│               ├── skills.tex.j2
│               ├── honors.tex.j2
│               ├── certificates.tex.j2
│               ├── committees.tex.j2
│               ├── extracurricular.tex.j2
│               ├── presentation.tex.j2
│               ├── summary.tex.j2
│               └── writing.tex.j2
├── tests/
│   ├── conftest.py              # Pytest fixtures
│   ├── test_samples.py
│   ├── unit/                    # Unit tests
│   │   ├── test_compiler.py
│   │   ├── test_config.py
│   │   └── test_renderer.py
│   └── integration/             # Integration tests
│       └── test_pipeline.py
├── examples/
│   ├── demo.py                  # Python API demo
│   ├── pdf_example.py           # PDF generation demo
│   ├── cli_demo.sh              # CLI usage examples
│   └── example_cli.yaml         # Sample YAML input
├── docs/
│   ├── adr/                     # Architecture Decision Records
│   │   ├── README.md            # ADR index
│   │   └── 0001-*.md            # Individual ADRs
│   ├── cli_usage.md             # CLI documentation
│   └── ...                      # Other docs
├── dev/
│   └── scripts/
│       ├── check_templates.py   # Template validation
│       └── prepare_readme.py    # Convert README links for PyPI
├── pyproject.toml               # Project configuration
├── UPSTREAM_VERSION             # Tracked Awesome-CV commit
└── uv.lock                      # Locked dependencies
```

### Technology Stack

| Component | Version/Tool | Notes |
|-----------|--------------|-------|
| Python | >=3.10 | Supports 3.10, 3.11, 3.12, 3.13 |
| Build system | uv | `uv_build>=0.9.3` backend |
| Package manager | uv | `uv sync`, `uv run` |
| Templating | jinja2>=3.1.0 | Core dependency |
| Config parsing | pyyaml>=6.0 | YAML input support |
| Linting | ruff>=0.1.0 | Dev dependency |
| Testing | pytest>=7.0 | Dev dependency |
| PDF compilation | xelatex or Docker | Optional, for PDF output |

---

## 2. Build and Test Commands

### Setup

```bash
# Clone and setup
git clone https://github.com/yourname/awesomecv_jinja.git
cd awesomecv_jinja
uv sync                    # Install all dependencies

# Install with dev dependencies
uv sync --dev
```

### Development Workflow

```bash
# Run tests (preferred method)
uv run pytest

# Run specific test file
uv run pytest tests/unit/test_renderer.py

# Run with verbose output
uv run pytest -v

# Run examples
uv run python examples/demo.py
uv run python examples/pdf_example.py
```

### Linting

```bash
# Check code style
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

### Build

```bash
# Build package (only before release)
uv build

# Editable install (for IDE integration)
uv pip install -e .
```

### CLI Usage

```bash
# Generate PDF from YAML
uv run acv resume.yaml                    # → resume.pdf
uv run acv cv.yaml -d cv -o my_cv.pdf     # Custom output
uv run acv data.yaml --tex-only           # Generate .tex only
uv run acv resume.tex                     # Compile existing .tex
```

---

## 3. Code Style Guidelines

### Preferred Patterns

**KISS (Keep It Simple)**
- Flat module hierarchy: `renderer.py`, `config.py`, `samples.py`
- No subpackages unless >5 related modules
- Simple solutions: `samples.py` better than `data/__init__.py`

**DRY (Don't Repeat Yourself)**
- Shared sections in `sections/` directory
- Sample data in single place (`MASTER_DATA` in `samples.py`)
- Reuse via includes and functions

**SRP (Single Responsibility)**
- Each module does one thing:
  - `renderer.py` — renders templates
  - `compiler.py` — compiles PDF
  - `pipeline.py` — orchestrates render + compile
  - `config.py` — Jinja2 configuration
  - `samples.py` — sample data
  - `exceptions.py` — error types

**PEP 8 + Ruff**
- Line length: 100 characters
- Docstrings for all public functions
- Type hints where possible
- ruff rules: E, F, W, I, N, UP

**Type Checking:** Use type hints for all functions. All public APIs MUST have complete annotations.

### Anti-Patterns (Avoid)

- Creating abstractions for one-time operations
- Subpackages with <5 modules
- Mixing concerns (rendering + PDF in same function)
- Duplicating code >2 times without extracting
- Modules >500 lines without splitting
- Functions that change return type based on arguments (use consistent return types)

### File Management Rules


**MUST NOT create or suggest `Makefile`** (use `uv run` instead. Reasons: 1) `uv` is standard, 2) reduces complexity, 3) cross-platform).

**MUST NOT delete:** `py.typed` (required for PEP 561), `MANIFEST.in`

**Template files:** Store only `.tex.j2` in repository. Do NOT commit `.tex` files unless explicitly instructed.

### Jinja2 Delimiters

LaTeX uses `{}`. Standard `{{` and `{%` conflict.

**Custom delimiters:**
```
((( name )))     — variables
((* if ... *))   — blocks  
((# ... #))      — comments
```

**Whitespace control:**
Use `-` to remove whitespace when needed:
```jinja
((* if condition -*))
content
((*- endif *))
```

### Exception Hierarchy

```python
AwesomeCVJinjaError          # Base exception
├── TemplateNotFoundError    # Template not found
├── DocumentTypeNotFoundError # Invalid doc_type
├── RenderError              # Rendering failed
└── CompilationError         # PDF compilation failed
```

---

## 4. Testing Instructions

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures (resume_data, cv_data, etc.)
├── test_samples.py          # Sample data tests
├── unit/                    # Unit tests (no external deps)
│   ├── test_compiler.py
│   ├── test_config.py
│   └── test_renderer.py
└── integration/             # Integration tests (may need xelatex/docker)
    └── test_pipeline.py
```

### Writing Tests

```python
# Use fixtures from conftest.py
def test_render_resume(resume_data):
    """Descriptive docstring"""
    renderer = Renderer()
    result = renderer.render("resume", resume_data)
    
    assert isinstance(result, str)
    assert resume_data["first_name"] in result
    assert r"\documentclass" in result

# Test exceptions
def test_invalid_template_raises_error():
    with pytest.raises(TemplateNotFoundError, match="not found"):
        Renderer(template="nonexistent")

# Test file output
def test_render_to_file(resume_data, tmp_render_dir):
    renderer = Renderer()
    output_path = tmp_render_dir / "test.tex"
    
    renderer.render("resume", resume_data, output=output_path)
    
    assert output_path.exists()
```

### Test Naming Convention

```python
class TestRendererInit:      # Group by class/function
    def test_init_with_default_template(self):
        """Initializes with default awesome_cv template"""
        ...
    
    def test_init_with_invalid_template_raises_error(self):
        """Raises TemplateNotFoundError for invalid template"""
        ...
```

### Running Specific Tests

```bash
# Run all tests
uv run pytest

# Run unit tests only
uv run pytest tests/unit/

# Run specific test class
uv run pytest tests/unit/test_renderer.py::TestRendererRender

# Run specific test
uv run pytest tests/unit/test_renderer.py::TestRendererRender::test_render_returns_string
```

---

## 5. Security Considerations

### LaTeX Escaping

**Always escape user input** with `latex_escape` filter:

```jinja
((( user_text | latex_escape )))
```

Escapes: `& % $ # _ { } ~ ^ \`

### Logging Rules

- **Never log** sensitive user data (emails, phone numbers, addresses)
- **Log only** template names, document types, error types
- **Avoid** logging full rendered content

### Input Validation

- Validate YAML structure before processing
- Check file paths for directory traversal
- Limit input data size

### Docker Compilation

- Use `docker-sudo` only when necessary
- Prefer `xelatex` when available locally
- Docker images run with limited permissions

---

## Public API

See `README.md` and docstrings for full API documentation.

**Main exports:**
```python
# Rendering
from awesomecv_jinja import Renderer, render, render_pdf

# Sample data
from awesomecv_jinja import load_sample, get_master_data

# Exceptions
from awesomecv_jinja import (
    AwesomeCVJinjaError,
    TemplateNotFoundError,
    DocumentTypeNotFoundError,
    RenderError,
    CompilationError,
)
```

**Quick example:**
```python
from awesomecv_jinja import render_pdf, load_sample

data = load_sample("resume")
render_pdf(data, output="resume.pdf")
```

---

## Upstream & Templates

**Awesome-CV tracking:**
- Upstream repo cloned to `dev/upstream/awesome-cv/` (gitignored)
- Converted templates in `src/awesomecv_jinja/templates/` (committed)
- Version tracked in `UPSTREAM_VERSION` file

**Adding new templates:**
1. Clone to `dev/upstream/<template>/`
2. Convert to `.tex.j2` with custom delimiters: `((( )))`, `((* *))`, `((# #))`
3. Add to `src/awesomecv_jinja/templates/<template>/`
4. Update `AVAILABLE_TEMPLATES` in `renderer.py`
5. Add tests

**License:** Code is MIT, Awesome-CV templates are LPPL-1.3c
