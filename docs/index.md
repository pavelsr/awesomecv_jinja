# awesomecv-jinja

Generate professional CVs, resumes, and cover letters from YAML/JSON data using [Awesome-CV](https://github.com/posquit0/Awesome-CV) LaTeX templates.

## Features

- 🎨 **Professional templates** — Based on Awesome-CV LaTeX templates
- 🚀 **Simple API** — From data to PDF in one function call
- 🔧 **Jinja2 templating** — Dynamic content generation with custom delimiters
- 🐳 **Flexible compilation** — Local xelatex or Docker (no LaTeX installation required)
- 📝 **Multiple formats** — Generate `.tex`, `.pdf`, or both
- 🔌 **Extensible** — Add your own LaTeX templates

## Quick Start

**Installation:**

```bash
pipx install awesomecv-jinja
```

**Generate PDF:**

```bash
acv resume.yaml
```

**Python API:**

```python
from awesomecv_jinja import render_pdf, load_sample

data = load_sample("resume")
render_pdf(data, output="resume.pdf")
```

## Documentation

- [CLI Usage](cli_usage.md) — Complete command-line interface guide
- [Docker Setup](docker_setup.md) — Docker setup for PDF compilation
- [Template Variables](awesomecv_tpl_vars.md) — Available template variables

## Links

- [GitHub Repository](https://github.com/pavelsr/awesomecv_jinja)
- [PyPI Package](https://pypi.org/project/awesomecv-jinja/)
- [Original Awesome-CV](https://github.com/posquit0/Awesome-CV)

## License

- Code: MIT
- Awesome-CV templates: LPPL-1.3c
