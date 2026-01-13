# awesomecv-jinja

Generate professional CVs, resumes, and cover letters from YAML/JSON data using [Awesome-CV](https://github.com/posquit0/Awesome-CV) LaTeX templates.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [CLI Usage](#cli-usage)
- [Python API](#python-api)
  - [Generate PDF](#generate-pdf)
  - [Generate LaTeX only](#generate-latex-only)
  - [Customize data](#customize-data)
  - [Document types](#document-types)
  - [Advanced: Use Renderer class](#advanced-use-renderer-class)
- [Requirements](#requirements)
- [Examples](#examples)
- [Development](#development)
- [Credits](#credits)
- [License](#license)
- [Links](#links)

## Features

- 🎨 **Professional templates** — Based on Awesome-CV LaTeX templates
- 🚀 **Simple API** — From data to PDF in one function call
- 🔧 **Jinja2 templating** — Dynamic content generation with custom delimiters
- 🐳 **Flexible compilation** — Local xelatex or Docker (no LaTeX installation required)
- 📝 **Multiple formats** — Generate `.tex`, `.pdf`, or both
- 🔌 **Extensible** — Add your own LaTeX templates

## Installation

**For CLI usage only (recommended):**

```bash
pipx install awesomecv-jinja
```

**For Python API usage:**

```bash
pip install awesomecv-jinja
```

For PDF generation, install xelatex or use Docker. See [docs/docker_setup.md](docs/docker_setup.md).

## CLI Usage

```bash
# Generate PDF from YAML
acv resume.yaml

# Specify document type and output
acv data.yaml -d cv -o my_cv.pdf

# Generate LaTeX only (no PDF)
acv resume.yaml --tex-only

# Use local xelatex instead of Docker
acv resume.yaml -e xelatex

# Compile existing .tex file
acv resume.tex
```

See [docs/cli_usage.md](docs/cli_usage.md) for complete CLI documentation.

## Python API

### Generate PDF

```python
from awesomecv_jinja import render_pdf, load_sample

data = load_sample("resume")
render_pdf(data, output="resume.pdf")
```

### Generate LaTeX only

```python
from awesomecv_jinja import render, load_sample

data = load_sample("resume")
render(data, output="resume.tex")
```

### Customize data

```python
from awesomecv_jinja import render_pdf, load_sample

data = load_sample("resume")
data["first_name"] = "Jane"
data["last_name"] = "Smith"
data["position"] = "Software Engineer"

render_pdf(data, output="jane_smith.pdf")
```

### Document types

```python
from awesomecv_jinja import render_pdf, load_sample

# Resume
render_pdf(load_sample("resume"), doc_type="resume", output="resume.pdf")

# Academic CV
render_pdf(load_sample("cv"), doc_type="cv", output="cv.pdf")

# Cover letter
render_pdf(load_sample("coverletter"), doc_type="coverletter", output="letter.pdf")
```

### Advanced: Use Renderer class

```python
from awesomecv_jinja import Renderer, load_sample

renderer = Renderer(template="awesome_cv")
renderer.render("resume", load_sample("resume"), output="resume.tex")

# List available document types
print(renderer.list_document_types())  # ['resume', 'cv', 'coverletter']
```

## Requirements

- Python 3.10+
- For PDF generation: xelatex (`texlive-full`) or Docker

## Examples

See `examples/` directory:
- `demo.py` — Python API examples
- `pdf_example.py` — PDF generation
- `example_cli.yaml` — Sample YAML input

```bash
uv run python examples/demo.py
```

## Development

```bash
# Fork the repository on GitHub
git clone https://github.com/<your_username>/awesomecv_jinja.git
cd awesomecv_jinja
uv sync
# do something
uv run pytest
git checkout -b feature-branch
git commit -m "Your commit message"
git push origin feature-branch
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Credits

Based on [Awesome-CV](https://github.com/posquit0/Awesome-CV) by [@posquit0](https://github.com/posquit0).

## License

- Code: MIT
- Awesome-CV templates: LPPL-1.3c

## Links

- PyPI: https://pypi.org/project/awesomecv-jinja/
- Read the Docs: https://awesomecv-jinja.readthedocs.io/
