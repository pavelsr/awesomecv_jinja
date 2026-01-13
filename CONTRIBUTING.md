# Contributing to awesomecv-jinja

This document describes the contribution workflow for awesomecv-jinja.

## Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager

## Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/pavelsr/awesomecv_jinja.git
   cd awesomecv_jinja
   ```

2. Install dependencies:

   ```bash
   uv sync
   ```

3. Verify the installation:

   ```bash
   uv run pytest
   uv run ruff check src/
   ```

## Development Workflow

### Code Style

The project uses **ruff** for linting and formatting. Line length is 100 characters.

Run these commands before committing:

```bash
# Check for linting issues
uv run ruff check src/ tests/

# Auto-fix issues
uv run ruff check --fix src/ tests/

# Format code
uv run ruff format src/ tests/
```

### Running Tests

Run all tests:

```bash
uv run pytest
```

Run specific tests:

```bash
# Verbose output
uv run pytest -v

# Specific test file
uv run pytest tests/unit/test_renderer.py

# Specific test class
uv run pytest tests/unit/test_renderer.py::TestRendererRender

# With coverage
uv run pytest --cov=src/awesomecv_jinja
```

### Running Examples

```bash
uv run python examples/demo.py
uv run python examples/pdf_example.py
```

## Making Changes

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Implement Changes

Follow these guidelines:

- Add docstrings to public functions and classes
- Include type hints for all function signatures
- Keep functions focused (single responsibility)
- Follow existing code style

See `AGENTS.md` section "Code Style Guidelines" for detailed patterns.

### 3. Run Quality Checks

```bash
uv run ruff check src/ tests/
uv run ruff format src/ tests/
uv run pytest
```

### 4. Commit Changes

Write clear commit messages:

```bash
git commit -m "Add feature: support for custom template paths"
```

### 5. Create Pull Request

```bash
git push origin feature/your-feature-name
```

Open a pull request on GitHub.

## Testing Guidelines

- Write tests for new features
- Maintain or improve test coverage
- Include edge cases and error handling

Test structure:

- `tests/unit/` — Unit tests (no external dependencies)
- `tests/integration/` — Integration tests (may require xelatex or Docker)

See `AGENTS.md` section "Testing Instructions" for test examples and naming conventions.

## Adding New Templates

1. Clone upstream template to `dev/upstream/<template_name>/`
2. Convert `.tex` files to `.tex.j2` using custom delimiters
3. Place templates in `src/awesomecv_jinja/templates/<template_name>/`
4. Register in `renderer.py` (`AVAILABLE_TEMPLATES`)
5. Add tests

See `AGENTS.md` section "Upstream & Templates" for details.

## Documentation

Update documentation when making changes:

| Change Type | Update Location |
|-------------|-----------------|
| User-facing features | `README.md` |
| API changes | Docstrings, update examples |
| Architecture changes | `AGENTS.md` |
| New files/directories | `AGENTS.md` Repository Map |

All documentation MUST follow the style rules in `AGENTS.md` section "Documentation Language and Style".

## Reporting Issues

Before opening an issue:

1. Check existing issues for duplicates
2. Verify the issue with the latest version

Include in the issue:

- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Python version and OS
- Relevant code examples or error messages

## Publishing

See [docs/publishing.md](docs/publishing.md) for PyPI publishing instructions (maintainers only).

## Useful Links

- [Awesome-CV Repository](https://github.com/posquit0/Awesome-CV)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [uv Documentation](https://github.com/astral-sh/uv)

## License

Contributions are licensed under the MIT License.
