"""
Pipeline API for data → PDF conversion.

Combines rendering and compilation in a single convenient interface.
"""

from pathlib import Path
from typing import Dict, Any, Union, Literal
import tempfile
import shutil

from .renderer import Renderer
from .compiler import PDFCompiler


def render_pdf(
    data: Dict[str, Any],
    doc_type: str = "resume",
    template: str = "awesome_cv",
    output: Union[str, Path] = "output.pdf",
    engine: Literal["auto", "xelatex", "docker", "docker-sudo"] = "auto",
    keep_tex: bool = False,
) -> Path:
    """
    Render data directly to PDF (data → PDF in one call).
    
    This is a convenience function that:
    1. Renders Jinja2 template to .tex
    2. Copies required .cls files
    3. Compiles .tex to .pdf
    4. Optionally cleans up intermediate files
    
    Args:
        data: Document data dictionary
        doc_type: Document type (resume, cv, coverletter)
        template: Template to use (default: awesome_cv)
        output: Output PDF path
        engine: Compilation engine (auto/xelatex/docker/docker-sudo)
        keep_tex: Keep intermediate .tex file (default: False)
    
    Returns:
        Path to generated PDF file
    
    Raises:
        CompilationError: If PDF compilation fails
        RenderError: If template rendering fails
    
    Examples:
        Quick PDF generation:
        
        >>> from awesomecv_jinja import render_pdf, load_sample
        >>> data = load_sample("resume")
        >>> pdf = render_pdf(data, output="my_resume.pdf")
        >>> print(f"PDF created: {pdf}")
        
        Keep .tex file:
        
        >>> pdf = render_pdf(data, output="resume.pdf", keep_tex=True)
        # Creates both resume.tex and resume.pdf
        
        Use Docker:
        
        >>> pdf = render_pdf(data, engine="docker", output="resume.pdf")
        
        Different document type:
        
        >>> cv_data = load_sample("cv")
        >>> pdf = render_pdf(cv_data, doc_type="cv", output="cv.pdf")
    """
    output_path = Path(output).absolute()
    pdf_path = None  # Initialize for finally block
    
    # Determine where to create tex file
    if keep_tex:
        # Create tex in same location as pdf
        tex_file = output_path.with_suffix(".tex")
        work_dir = output_path.parent
        work_dir.mkdir(parents=True, exist_ok=True)
        cleanup_dir = None
    else:
        # Create in temporary directory
        temp_dir = tempfile.mkdtemp(prefix="awesomecv_")
        work_dir = Path(temp_dir)
        tex_file = work_dir / "document.tex"
        cleanup_dir = work_dir
    
    try:
        # Step 1: Render tex
        renderer = Renderer(template=template)
        renderer.render(doc_type, data, output=tex_file)
        
        # Step 2: Copy required .cls and other assets
        _copy_template_assets(template, work_dir)
        
        # Step 3: Compile to PDF
        compiler = PDFCompiler(engine=engine)
        pdf_path = compiler.compile_file(
            tex_file,
            output=None,  # Compile in place first
            keep_artifacts=keep_tex
        )
        
        # Step 4: Move PDF to final location
        if pdf_path != output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(pdf_path), str(output_path))
            pdf_path = output_path
        
        return pdf_path
    
    finally:
        # Cleanup temporary directory if used
        # Only cleanup on success to allow debugging failures
        if cleanup_dir and cleanup_dir.exists() and pdf_path and pdf_path.exists():
            try:
                shutil.rmtree(cleanup_dir)
            except Exception:
                pass  # Ignore cleanup errors


def _copy_template_assets(template: str, target_dir: Path):
    """
    Copy required template assets (.cls files, fonts, etc.) to target directory.
    
    Args:
        template: Template name (e.g., "awesome_cv")
        target_dir: Directory to copy assets to
    """
    try:
        # For awesome_cv, we need awesome-cv.cls
        if template == "awesome_cv":
            # Try to find .cls in package
            try:
                from importlib.resources import files
                template_files = files("awesomecv_jinja").joinpath(f"templates/{template}")
                cls_content = template_files.joinpath("awesome-cv.cls").read_text()
                (target_dir / "awesome-cv.cls").write_text(cls_content)
            except Exception:
                # Fallback: try file system path
                from pathlib import Path
                import awesomecv_jinja
                package_dir = Path(awesomecv_jinja.__file__).parent
                cls_file = package_dir / f"templates/{template}/awesome-cv.cls"
                
                if cls_file.exists():
                    shutil.copy2(cls_file, target_dir / "awesome-cv.cls")
                else:
                    # Last resort: might be in development mode
                    cls_dev = Path("src/awesomecv_jinja") / f"templates/{template}/awesome-cv.cls"
                    if cls_dev.exists():
                        shutil.copy2(cls_dev, target_dir / "awesome-cv.cls")
    
    except Exception:
        # Don't fail if we can't copy assets - LaTeX might still work
        # if cls file is already in the directory
        pass

