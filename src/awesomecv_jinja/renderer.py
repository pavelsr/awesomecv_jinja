"""
Renderer for LaTeX CV templates.

Provides main rendering functionality for converting data to LaTeX documents.
"""

from pathlib import Path
from typing import Dict, Any, Optional, Union, List
from jinja2 import TemplateNotFound

from .config import create_latex_environment
from .exceptions import (
    TemplateNotFoundError,
    DocumentTypeNotFoundError,
    RenderError,
)


class Renderer:
    """
    Renderer for LaTeX CV templates.
    
    Handles rendering of different document types (resume, cv, coverletter)
    using Jinja2 templates with LaTeX-compatible syntax.
    
    Attributes:
        template: Name of the template package (e.g., "awesome_cv")
        env: Jinja2 Environment instance
    
    Examples:
        Basic usage:
        
        >>> from awesomecv_jinja import Renderer, load_sample
        >>> 
        >>> renderer = Renderer(template="awesome_cv")
        >>> data = load_sample("resume")
        >>> output = renderer.render("resume", data)
        >>> print(output[:50])
        
        Save to file:
        
        >>> renderer.render("resume", data, output="my_resume.tex")
        
        List available document types:
        
        >>> renderer.list_document_types()
        ['resume', 'cv', 'coverletter']
    """
    
    # Available template packages
    AVAILABLE_TEMPLATES = ["awesome_cv"]
    
    def __init__(
        self,
        template: str = "awesome_cv",
        custom_template_dir: Optional[Path] = None,
    ):
        """
        Initialize renderer with specified template.
        
        Args:
            template: Name of template package to use (default: "awesome_cv")
            custom_template_dir: Path to custom templates directory (optional)
        
        Raises:
            TemplateNotFoundError: If template is not available
        
        Examples:
            >>> # Use built-in template
            >>> renderer = Renderer(template="awesome_cv")
            >>> 
            >>> # Use custom templates
            >>> from pathlib import Path
            >>> renderer = Renderer(custom_template_dir=Path("my_templates"))
        """
        if not custom_template_dir and template not in self.AVAILABLE_TEMPLATES:
            available = ', '.join(self.AVAILABLE_TEMPLATES)
            raise TemplateNotFoundError(
                f"Template '{template}' not found. "
                f"Available templates: {available}"
            )
        
        self.template = template
        self.custom_template_dir = custom_template_dir
        self.env = create_latex_environment(
            template_loader=template if not custom_template_dir else None,
            custom_template_dir=custom_template_dir,
        )
    
    def render(
        self,
        doc_type: str,
        data: Dict[str, Any],
        output: Optional[Union[str, Path]] = None,
    ) -> str:
        """
        Render document with specified type and data.
        
        Args:
            doc_type: Type of document to render (resume, cv, coverletter)
            data: Dictionary with document data
            output: Optional path to save output file
        
        Returns:
            Rendered LaTeX content as string
        
        Raises:
            DocumentTypeNotFoundError: If document type template not found
            RenderError: If rendering fails
        
        Examples:
            >>> renderer = Renderer()
            >>> data = {"first_name": "John", "last_name": "Doe", ...}
            >>> 
            >>> # Get rendered content
            >>> latex = renderer.render("resume", data)
            >>> 
            >>> # Save directly to file
            >>> renderer.render("resume", data, output="resume.tex")
        """
        template_name = f"{doc_type}.tex.j2"
        
        try:
            template = self.env.get_template(template_name)
        except TemplateNotFound as e:
            available = self.list_document_types()
            raise DocumentTypeNotFoundError(
                f"Document type '{doc_type}' not found in template '{self.template}'. "
                f"Available: {', '.join(available)}"
            ) from e
        
        try:
            result = template.render(**data)
        except Exception as e:
            raise RenderError(
                f"Failed to render {doc_type} with template '{self.template}': {e}"
            ) from e
        
        # Save to file if output path provided
        if output:
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(result, encoding='utf-8')
        
        return result
    
    def list_document_types(self) -> List[str]:
        """
        List available document types in current template.
        
        Checks which .tex.j2 files are available in the template.
        
        Returns:
            List of available document type names
        
        Examples:
            >>> renderer = Renderer()
            >>> types = renderer.list_document_types()
            >>> print(types)
            ['resume', 'cv', 'coverletter']
            >>> 
            >>> # Check if specific type is available
            >>> if 'resume' in renderer.list_document_types():
            ...     print("Resume template available")
        """
        available = []
        
        # Standard document types to check
        standard_types = ["resume", "cv", "coverletter"]
        
        for doc_type in standard_types:
            template_name = f"{doc_type}.tex.j2"
            try:
                self.env.get_template(template_name)
                available.append(doc_type)
            except TemplateNotFound:
                pass
        
        return available
    
    def get_template_info(self) -> Dict[str, Any]:
        """
        Get information about current template.
        
        Returns:
            Dictionary with template information
        
        Examples:
            >>> renderer = Renderer()
            >>> info = renderer.get_template_info()
            >>> print(info['name'])
            'awesome_cv'
            >>> print(info['document_types'])
            ['resume', 'cv', 'coverletter']
        """
        return {
            'name': self.template,
            'custom': self.custom_template_dir is not None,
            'document_types': self.list_document_types(),
        }


def render(
    data: Dict[str, Any],
    doc_type: str = "resume",
    template: str = "awesome_cv",
    output: Optional[Union[str, Path]] = None,
) -> str:
    """
    Convenience function for quick rendering.
    
    Creates a Renderer instance and renders document in one call.
    
    Args:
        data: Dictionary with document data
        doc_type: Type of document (default: "resume")
        template: Template to use (default: "awesome_cv")
        output: Optional path to save output file
    
    Returns:
        Rendered LaTeX content as string
    
    Examples:
        Quick render with defaults:
        
        >>> from awesomecv_jinja import render, load_sample
        >>> data = load_sample("resume")
        >>> output = render(data)
        
        Specify document type:
        
        >>> cv_data = load_sample("cv")
        >>> render(cv_data, doc_type="cv", output="my_cv.tex")
        
        Use different template:
        
        >>> render(data, template="moderncv", doc_type="resume")
    """
    renderer = Renderer(template=template)
    return renderer.render(doc_type, data, output)

