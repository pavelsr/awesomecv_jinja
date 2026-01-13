"""
awesomecv-jinja - Beautiful LaTeX CV templates with Jinja2

Generate professional CVs and resumes using Awesome-CV LaTeX templates
with the power of Jinja2 templating engine.

Examples:
    Quick start - generate PDF directly:
    
    >>> from awesomecv_jinja import render_pdf, load_sample
    >>> data = load_sample("resume")
    >>> pdf = render_pdf(data, output="my_resume.pdf")
    
    Generate LaTeX only:
    
    >>> from awesomecv_jinja import render
    >>> tex = render(data, output="my_resume.tex")
    
    Advanced usage with Renderer:
    
    >>> from awesomecv_jinja import Renderer
    >>> renderer = Renderer(template="awesome_cv")
    >>> renderer.render("resume", data, output="resume.tex")
"""

from .samples import load_sample, get_master_data
from .renderer import Renderer, render
from .compiler import PDFCompiler, CompilationEngine
from .pipeline import render_pdf
from .exceptions import (
    AwesomeCVJinjaError,
    TemplateNotFoundError,
    DocumentTypeNotFoundError,
    RenderError,
    CompilationError,
)

# Read version from package metadata (single source of truth: pyproject.toml)
try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    # Fallback for Python < 3.8
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version("awesomecv-jinja")
except PackageNotFoundError:
    # Fallback for development mode (package not installed)
    # Read version directly from pyproject.toml
    from pathlib import Path
    
    try:
        # Python 3.11+ has tomllib built-in
        try:
            import tomllib
        except ImportError:
            # Python 3.10 and below need tomli
            import tomli as tomllib
        
        pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
        if pyproject_path.exists():
            with pyproject_path.open("rb") as f:
                pyproject_data = tomllib.load(f)
                __version__ = pyproject_data["project"]["version"]
        else:
            __version__ = "0.0.0"
    except Exception:
        # Ultimate fallback
        __version__ = "0.0.0"
__all__ = [
    # Main API
    "Renderer",
    "render",
    # PDF Pipeline
    "render_pdf",
    "PDFCompiler",
    "CompilationEngine",
    # Sample data
    "load_sample",
    "get_master_data",
    # Exceptions
    "AwesomeCVJinjaError",
    "TemplateNotFoundError",
    "DocumentTypeNotFoundError",
    "RenderError",
    "CompilationError",
]
