# CLI Usage Guide

The `acv` CLI provides a simple way to work with CV/Resume files:
- **Generate from YAML**: convert data to LaTeX and compile it to PDF.
- **Compile `.tex` files**: compile existing LaTeX files to PDF.

## Installation

```bash
pip install awesomecv-jinja
# or
uv add awesomecv-jinja
```

After installation, the `acv` command is available in your system.

## Basic usage

### Mode 1: Generate from YAML

```bash
# Basic case: generate a PDF from YAML
acv my_resume.yaml
# → creates my_resume.pdf

# Set the document type
acv my_cv.yaml -d cv
# → creates my_cv.pdf (CV format)

# Set the output file name
acv data.yaml -o custom_name.pdf
# → creates custom_name.pdf

# Generate only the .tex file without compiling to PDF
acv my_resume.yaml --tex-only
# → creates my_resume.tex

# Generate a PDF and keep the generated .tex file
acv my_resume.yaml --save-tex
# → creates my_resume.pdf and my_resume.tex
```

### Mode 2: Compile existing `.tex` files

```bash
# Compile an existing .tex file
acv resume.tex
# → creates resume.pdf

# Select engine and output file
acv document.tex -e xelatex -o output.pdf
# → creates output.pdf using xelatex

# Keep compilation artifacts (.aux, .log)
acv resume.tex --save-tex
# → creates resume.pdf and keeps auxiliary files
```

## Options

### Required argument

- `input_file`: a YAML file with CV/Resume data **or** a `.tex` file to compile.

### Optional arguments

- `-d, --doctype {resume,cv,coverletter}`: document type (default: `resume`) **[YAML only]**
- `-o, --output OUTPUT`: output path (default: `<input_name>.pdf`)
- `-e, --engine {auto,xelatex,docker,docker-sudo}`: PDF compilation engine (default: `docker-sudo`)
- `--save-tex`: for YAML, keep the generated `.tex`; for `.tex`, keep compilation artifacts (`.aux`, `.log`)
- `--tex-only`: generate only the `.tex` file, do not compile PDF **[YAML only]**
- `-v, --version`: print version
- `-h, --help`: show help

#### Available compilation engines

- `auto`: auto-detect (`xelatex` → `docker`)
- `xelatex`: local XeLaTeX (fastest, requires installation)
- `docker`: Docker with TeX Live (no sudo)
- `docker-sudo`: Docker with sudo (default, works on most systems)

## Examples

### Example 1: Resume

```bash
acv resume.yaml
```

### Example 2: Academic CV

```bash
acv cv_data.yaml -d cv -o academic_cv.pdf
```

### Example 3: Cover letter

```bash
acv letter.yaml -d coverletter -o cover_letter.pdf
```

### Example 4: LaTeX only (for manual compilation)

```bash
acv resume.yaml --tex-only
xelatex resume.tex  # compile manually
```

### Example 5: PDF + keep LaTeX

```bash
acv resume.yaml --save-tex -o my_resume.pdf
# → creates my_resume.pdf and my_resume.tex
```

### Example 6: Choose a compilation engine

```bash
# Use local xelatex (faster, if installed)
acv resume.yaml -e xelatex

# Use Docker without sudo
acv resume.yaml -e docker

# Auto-detection (tries xelatex first, then docker)
acv resume.yaml -e auto

# Default is docker-sudo
acv resume.yaml  # equivalent to: acv resume.yaml -e docker-sudo
```

### Example 7: Combined options

```bash
# CV with local xelatex and keep LaTeX
acv cv_data.yaml -d cv -e xelatex --save-tex -o academic_cv.pdf

# Resume with auto-detection
acv resume.yaml -e auto -o output/resume.pdf
```

### Example 8: Compile `.tex` files

```bash
# Simple compilation of an existing .tex file
acv my_document.tex
# → creates my_document.pdf

# Compilation with engine selection
acv resume.tex -e xelatex
acv resume.tex -e docker

# Compilation with a custom output file
acv source.tex -o final_resume.pdf

# Workflow: generate .tex first, then compile
acv data.yaml --tex-only           # → data.tex
# edit data.tex manually...
acv data.tex -e xelatex            # → data.pdf
```

**Note:** When compiling `.tex` files, `-d/--doctype` is ignored because the document
type is already defined in the `.tex` file itself.

## YAML file structure

Minimal resume example:

```yaml
# Personal information
first_name: John
last_name: Doe
position: Software Engineer
address: 123 Main St, City, Country
mobile: +1-234-567-8900
email: john.doe@example.com

# Select sections to include
sections:
  experience: true
  education: true

# Work experience
experience:
  - title: Senior Engineer
    organization: Tech Corp
    location: San Francisco, CA
    period: 2020 - Present
    details:
      - Led team of 5 engineers
      - Built microservices

# Education
education:
  - degree: B.S. in Computer Science
    institution: MIT
    location: Cambridge, MA
    period: 2016 - 2020
```

For a full example, see `examples/example_cli.yaml`.

## Requirements

### For LaTeX generation (`--tex-only`)

- Python 3.10+ and the installed package.

### For PDF generation

By default, the CLI uses **docker-sudo** to compile PDFs.

Available options (select via `-e/--engine`):

- `docker-sudo`: Docker with sudo (CLI default)
- `docker`: Docker without sudo (requires setup)
- `xelatex`: local XeLaTeX (fastest, requires installation)
- `auto`: auto-detect (tries `xelatex` → `docker`)

For Docker setup instructions, see [DOCKER_SETUP.md](DOCKER_SETUP.md).

## Troubleshooting

### Error: "File not found"

Verify that the YAML file exists and that the path is correct.

### Error: "xelatex compilation failed"

Install XeLaTeX or use `--tex-only` to generate LaTeX only:

```bash
acv my_resume.yaml --tex-only
```

### Error: "Invalid YAML file"

Validate your YAML syntax. You can use online validators, or run:

```bash
python -c "import yaml; yaml.safe_load(open('my_file.yaml'))"
```

## Additional information

- Documentation: [README.md](README.md)
- Examples: [examples/](examples/)
- Templates: based on [Awesome-CV](https://github.com/posquit0/Awesome-CV)

