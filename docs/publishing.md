# Publishing to PyPI

This document describes how to publish `awesomecv-jinja` to PyPI.

## Requirements

- A PyPI account and an API token
- `uv` installed
- All tests passing
- Version updated in `pyproject.toml` (automatically read in code)

## Pre-publish checklist

- [ ] Update the version in `pyproject.toml` (version is automatically read from there)
- [ ] Ensure all tests pass: `uv run pytest`
- [ ] Run the linter: `uv run ruff check src/ tests/`
- [ ] Generate `README_PYPI.md`: `python3 dev/scripts/prepare_readme.py`
- [ ] Update `CHANGELOG.md` (if it exists) or add release notes

## Build the package

1. **Clean previous builds:**
   ```bash
   rm -rf dist/ build/ *.egg-info
   ```

2. **Generate README for PyPI:**
   ```bash
   python3 dev/scripts/prepare_readme.py
   ```
   
   This converts relative links in `README.md` to absolute GitHub URLs and saves the result to `README_PYPI.md`. PyPI uses this file for the project description.
   
   **Why?** PyPI does not support relative markdown links. Links like `[docs/cli_usage.md](docs/cli_usage.md)` become broken on PyPI. This script converts them to absolute GitHub URLs.

3. **Build:**
   ```bash
   uv build
   ```

   This produces:
   - `dist/awesomecv-jinja-<version>.tar.gz` (source distribution)
   - `dist/awesomecv-jinja-<version>-py3-none-any.whl` (wheel)

3. **Verify package contents:**
   ```bash
   # Inspect the source distribution
   tar -tzf dist/*.tar.gz | grep -E "(README|LICENSE|CONTRIBUTING|templates)" | head -20
   
   # Ensure templates are included
   tar -tzf dist/*.tar.gz | grep "\.tex\.j2"
   ```

4. **Check package metadata (recommended):**
   ```bash
   uv pip install twine
   uv run twine check dist/*
   ```
   
   This should output "PASSED" for both files. If you see errors, fix them before uploading.

## Test the build

Before publishing, test installation from the built artifacts:

```bash
# Create a test virtual environment
python -m venv test_install
source test_install/bin/activate  # On Windows: test_install\Scripts\activate

# Install from the wheel
pip install dist/*.whl

# Verify installation
python -c "import awesomecv_jinja; print(awesomecv_jinja.__version__)"
python -c "from awesomecv_jinja import render, load_sample; print('OK')"

# Cleanup
deactivate
rm -rf test_install
```

## Publishing

### Configure credentials

When using `uv run twine`, the isolated environment may not access `~/.pypirc`. Use environment variables instead:

**Option A1: `.env` file with `--env-file` (recommended)**

Create a `.env` file in the project root:

```bash
# .env
TWINE_USERNAME=__token__
TWINE_PASSWORD=pypi-your-api-token-here
TWINE_REPOSITORY_URL=https://upload.pypi.org/legacy/  # For PyPI
# or
# TWINE_REPOSITORY_URL=https://test.pypi.org/legacy/    # For TestPyPI
```

**Important:** Add `.env` to `.gitignore` to avoid committing credentials.

Then run:
```bash
uv run --env-file .env twine upload dist/*.whl dist/*.tar.gz
```

You can also specify the repository URL as a command-line argument instead of using `TWINE_REPOSITORY_URL`:
```bash
uv run --env-file .env twine upload --repository-url https://test.pypi.org/legacy/ dist/*.whl dist/*.tar.gz
```


**Personal setup:** The author uses `.env` with a TestPyPI token and `.env.prod` with a PyPI (upload.pypi.org) token. This allows switching between test and production uploads by changing the `--env-file` argument:

```bash
# Upload to TestPyPI
uv run --env-file .env twine upload --repository-url https://test.pypi.org/legacy/ dist/*.whl dist/*.tar.gz

# Upload to PyPI
uv run --env-file .env.prod twine upload --repository-url https://upload.pypi.org/legacy/ dist/*.whl dist/*.tar.gz
```


**Option A2: `.env` file with `UV_ENV_FILE` environment variable**

Set `UV_ENV_FILE` once, then use `uv run` normally:

```bash
export UV_ENV_FILE=.env
uv run twine upload dist/*.whl dist/*.tar.gz
```

This loads `.env` automatically for all `uv run` commands.

**Option A3: Environment variables (export in shell)**

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-api-token-here
export TWINE_REPOSITORY_URL=https://upload.pypi.org/legacy/  # For PyPI
# or
export TWINE_REPOSITORY_URL=https://test.pypi.org/legacy/    # For TestPyPI
```

Then run:
```bash
uv run twine upload dist/*.whl dist/*.tar.gz
```

**Note:** Use `dist/*.whl dist/*.tar.gz` instead of `dist/*` to avoid uploading non-package files (like `.gitignore`).

**Option B: Use twine directly (without `uv run`)**

If `twine` is installed globally or in an active virtual environment, you can use it directly:
```bash
twine upload dist/*.whl dist/*.tar.gz
```

This will read `~/.pypirc` or prompt for credentials.

**Important:** This option requires twine version 6.0 or higher. Many Linux distributions (including Ubuntu 24.04) ship with twine 5.0, which does not support modern metadata formats used by packages built with `uv build`. If you encounter "Metadata is missing required fields: Name, Version" errors, use `uv run twine` instead (Option A), as it ensures compatibility with packages built by `uv build`.

### Option 1: TestPyPI first (recommended)

**Important:** Make sure you have built the package first (see "Build the package" section above).

1. **Create a TestPyPI account:** `https://test.pypi.org/`

2. **Set credentials:**

   Create a `.env` file:
   ```bash
   # .env
   TWINE_USERNAME=__token__
   TWINE_PASSWORD=pypi-your-testpypi-token-here
   TWINE_REPOSITORY_URL=https://test.pypi.org/legacy/
   ```

3. **Upload to TestPyPI:**
   ```bash
   uv pip install twine
   uv run --env-file .env twine upload dist/*.whl dist/*.tar.gz
   ```
   
   Or use `--repository-url` argument:
   ```bash
   uv run --env-file .env twine upload --repository-url https://test.pypi.org/legacy/ dist/*.whl dist/*.tar.gz
   ```

4. **Test installation from TestPyPI:**
   ```bash
   pip install --index-url https://test.pypi.org/simple/ awesomecv-jinja
   ```

5. **If everything works, publish to PyPI:**
   
   Update `.env` file:
   ```bash
   # .env
   TWINE_USERNAME=__token__
   TWINE_PASSWORD=pypi-your-pypi-token-here
   TWINE_REPOSITORY_URL=https://upload.pypi.org/legacy/
   ```
   
   Then upload:
   ```bash
   uv run --env-file .env twine upload dist/*.whl dist/*.tar.gz
   ```
   
   Or use `--repository-url` argument:
   ```bash
   uv run --env-file .env twine upload --repository-url https://upload.pypi.org/legacy/ dist/*.whl dist/*.tar.gz
   ```

### Option 2: Publish directly to PyPI

**Important:** Make sure you have built the package first (see "Build the package" section above).

1. **Set credentials:**

   Create a `.env` file:
   ```bash
   # .env
   TWINE_USERNAME=__token__
   TWINE_PASSWORD=pypi-your-api-token-here
   TWINE_REPOSITORY_URL=https://upload.pypi.org/legacy/
   ```

2. **Upload:**
   ```bash
   uv pip install twine
   uv run --env-file .env twine upload dist/*.whl dist/*.tar.gz
   ```
   
   Or use `--repository-url` argument:
   ```bash
   uv run --env-file .env twine upload --repository-url https://upload.pypi.org/legacy/ dist/*.whl dist/*.tar.gz
   ```

## After publishing

- [ ] Verify that the package is visible on PyPI: `https://pypi.org/project/awesomecv-jinja/`
- [ ] Test installation: `pip install awesomecv-jinja`
- [ ] Create a GitHub release with release notes
- [ ] Update documentation if needed

## Troubleshooting

**"Package already exists"**
- Increase the version in `pyproject.toml`

**"Invalid distribution format" or "Metadata is missing required fields: Name, Version"**
- Ensure `uv build` completed successfully before uploading
- Use `dist/*.whl dist/*.tar.gz` instead of `dist/*` to avoid uploading non-package files
- Verify that `dist/` directory contains `.whl` and `.tar.gz` files (and no other files)
- Run `twine check dist/*.whl dist/*.tar.gz` to verify package files are valid
- Make sure you're running the command from the project root directory
- If using `twine` directly (without `uv run`), ensure it's version 6.0 or higher. Many Linux distributions (e.g., Ubuntu 24.04) ship with twine 5.0, which does not support modern metadata formats. Use `uv run twine` (Option A) to ensure compatibility.

**"Template files not found"**
- Verify that `MANIFEST.in` includes template files
- Verify that templates are in `src/awesomecv_jinja/templates/`

**Authentication errors**
- Verify that the PyPI API token is correct
- Verify token permissions (it must allow uploads)
- When using `uv run twine`, use environment variables (`TWINE_USERNAME`, `TWINE_PASSWORD`) instead of `~/.pypirc`
- If using `.env` file, ensure it exists and contains correct values
- Verify that `.env` file is in `.gitignore` to avoid committing credentials

## Versioning

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** - breaking changes
- **MINOR** - new features (backward compatible)
- **PATCH** - bug fixes

Update the version in `pyproject.toml`:
```toml
[project]
version = "X.Y.Z"
```

The version is automatically read from `pyproject.toml` in `__init__.py` using `importlib.metadata`, so you only need to update it in one place.

## Additional resources

- [PyPI Documentation](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [uv build Documentation](https://github.com/astral-sh/uv)

---

**Note:** After publishing, users can install the package via:
```bash
pip install awesomecv-jinja
# or
uv add awesomecv-jinja
```
