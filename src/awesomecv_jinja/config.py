"""
Jinja2 configuration for LaTeX templates.

Provides custom Jinja2 environment with LaTeX-compatible delimiters
and LaTeX-specific filters.
"""

from jinja2 import Environment, PackageLoader, FileSystemLoader
from pathlib import Path
from typing import Optional


def create_latex_environment(
    template_loader: Optional[str] = None,
    custom_template_dir: Optional[Path] = None,
) -> Environment:
    """
    Create Jinja2 environment configured for LaTeX templates.
    
    Uses custom delimiters that don't conflict with LaTeX syntax:
    - Variables: ((( variable )))
    - Blocks: ((* if condition *))
    - Comments: ((# comment #))
    
    Args:
        template_loader: Name of template package to load (e.g., "awesome_cv")
        custom_template_dir: Path to custom templates directory (overrides package)
    
    Returns:
        Configured Jinja2 Environment instance
    
    Examples:
        >>> # Default: load from package
        >>> env = create_latex_environment("awesome_cv")
        >>> 
        >>> # Custom directory
        >>> from pathlib import Path
        >>> env = create_latex_environment(custom_template_dir=Path("my_templates"))
        >>> 
        >>> # Use environment
        >>> template = env.get_template("resume.tex.j2")
        >>> output = template.render(first_name="John", last_name="Doe")
    """
    # Configure loader
    if custom_template_dir:
        loader = FileSystemLoader(custom_template_dir)
    elif template_loader:
        loader = PackageLoader(
            'awesomecv_jinja',
            f'templates/{template_loader}'
        )
    else:
        # Default: load awesome_cv
        loader = PackageLoader('awesomecv_jinja', 'templates/awesome_cv')
    
    # Create environment with LaTeX-compatible delimiters
    env = Environment(
        loader=loader,
        # Custom delimiters that don't conflict with LaTeX
        block_start_string='((*',
        block_end_string='*))',
        variable_start_string='(((',
        variable_end_string=')))',
        comment_start_string='((#',
        comment_end_string='#))',
        # Output formatting
        trim_blocks=True,       # Remove first newline after block
        lstrip_blocks=True,     # Strip leading whitespace from blocks
        keep_trailing_newline=True,  # Keep final newline
        # Security
        autoescape=False,       # LaTeX is not HTML - don't autoescape
    )
    
    # Register custom filters
    env.filters['latex_escape'] = latex_escape
    
    return env


def latex_escape(text: str) -> str:
    """
    Escape special LaTeX characters in text.
    
    Escapes the following characters:
    & % $ # _ { } ~ ^ \\
    
    Args:
        text: Text to escape
    
    Returns:
        Text with LaTeX special characters escaped
    
    Examples:
        >>> latex_escape("100% & more")
        '100\\% \\& more'
        >>> 
        >>> latex_escape("Price: $50")
        'Price: \\$50'
        >>> 
        >>> latex_escape("C:\\\\Users\\\\file.txt")
        'C:\\textbackslash{}Users\\textbackslash{}file.txt'
    
    Note:
        Backslash must be replaced first to avoid double-escaping.
    """
    if not isinstance(text, str):
        text = str(text)
    
    # Use placeholder for backslash to avoid double-escaping
    # This prevents {} in \textbackslash{} from being escaped
    BACKSLASH_PLACEHOLDER = '\x00BACKSLASH\x00'
    text = text.replace('\\', BACKSLASH_PLACEHOLDER)
    
    # Now handle other special characters
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
    }
    
    for char, escaped in replacements.items():
        text = text.replace(char, escaped)
    
    # Replace placeholder with final LaTeX command
    text = text.replace(BACKSLASH_PLACEHOLDER, r'\textbackslash{}')
    
    return text

