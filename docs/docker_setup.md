# Docker setup for PDF compilation

## Problem

When using `engine="docker-sudo"`, a timeout may happen if sudo requires an interactive password.

## Solutions

### Option 1: Add the user to the `docker` group (recommended)

```bash
# Add the current user to the docker group
sudo usermod -aG docker $USER

# Re-login, or run:
newgrp docker

# Check: it should work without sudo
docker run hello-world
```

After that, use:
```python
render_pdf(data, output="resume.pdf", engine="docker")  # No sudo.
```

### Option 2: Configure passwordless sudo for Docker

Create `/etc/sudoers.d/docker`:
```
your_username ALL=(ALL) NOPASSWD: /usr/bin/docker
```

**Warning:** This reduces security. Use it only in a development environment.

### Option 3: Use auto-detection

The library automatically selects the best available engine:

```python
# Auto-detect: tries xelatex → docker (no sudo)
render_pdf(data, output="resume.pdf")  # engine="auto" by default
```

### Option 4: Install xelatex (best for development)

```bash
# Ubuntu/Debian
sudo apt install texlive-xetex texlive-fonts-extra

# After installation
render_pdf(data, output="resume.pdf")  # Uses xelatex automatically
```

## For CI/CD

### GitHub Actions

```yaml
- name: Setup LaTeX
  run: |
    sudo apt-get update
    sudo apt-get install -y texlive-xetex texlive-fonts-extra

- name: Generate PDF
  run: |
    python -c "
    from awesomecv_jinja import render_pdf, load_sample
    data = load_sample('resume')
    render_pdf(data, output='resume.pdf')
    "
```

### Docker in CI/CD

```yaml
- name: Generate PDF with Docker
  run: |
    docker pull texlive/texlive:latest
    python -c "
    from awesomecv_jinja import render_pdf, load_sample
    data = load_sample('resume')
    render_pdf(data, output='resume.pdf', engine='docker')
    "
```

## Verify the setup

```python
from awesomecv_jinja.compiler import PDFCompiler, CompilationEngine

compiler = PDFCompiler()

# Check xelatex
if compiler.is_available(CompilationEngine.XELATEX):
    print("✅ xelatex is available")
else:
    print("❌ xelatex is not installed")

# Check docker
if compiler.is_available(CompilationEngine.DOCKER):
    print("✅ Docker is available")
else:
    print("❌ Docker is not installed")

# Try auto-detection
try:
    engine = compiler.detect_engine()
    print(f"✅ Engine selected: {engine.value}")
except:
    print("❌ No engine is available")
```

## Recommendations

**For development:**
- Install xelatex (faster, simpler)

**For production/CI:**
- Use Docker (reproducible)

**For quick start:**
- Use `engine="auto"` (default)

---

*Created: 2024-10-18*

