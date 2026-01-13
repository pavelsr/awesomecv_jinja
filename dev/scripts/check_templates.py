#!/usr/bin/env python3
"""
Validates syntax of all .tex.j2 templates.

Checks all templates in src/awesomecv_jinja/templates/ for Jinja2 syntax errors.
Supports multiple template directories (awesome_cv, moderncv, etc.).

Usage:
    uv run python dev/scripts/check_templates.py              # Check all templates
    uv run python dev/scripts/check_templates.py awesome_cv   # Check specific template
    uv run python dev/scripts/check_templates.py moderncv     # Check specific template
"""
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Add src to path to import latex_escape filter
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))
from awesomecv_jinja.config import latex_escape


def check_templates(template_name: str | None = None) -> bool:
    """
    Validate all templates for syntax errors.

    Args:
        template_name: Optional template directory name to check.
                       If None, checks all templates.

    Returns:
        True if all templates pass validation, False otherwise.
    """
    templates_base = Path('src/awesomecv_jinja/templates')

    if not templates_base.exists():
        print(f"✗ Templates directory not found: {templates_base}")
        return False

    # Create Jinja2 environment with custom delimiters
    env = Environment(
        loader=FileSystemLoader(str(templates_base)),
        block_start_string='((*',
        block_end_string='*))',
        variable_start_string='(((',
        variable_end_string=')))',
        comment_start_string='((#',
        comment_end_string='#))',
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        autoescape=False,
    )

    # Register custom filters
    env.filters['latex_escape'] = latex_escape

    # Determine which template directories to check
    if template_name:
        template_dirs = [templates_base / template_name]
        if not template_dirs[0].exists():
            print(f"✗ Template directory not found: {template_dirs[0]}")
            return False
    else:
        # Check all template directories
        template_dirs = [d for d in templates_base.iterdir() if d.is_dir()]

    if not template_dirs:
        print("✗ No template directories found")
        return False

    errors = []
    success_count = 0

    for template_dir in sorted(template_dirs):
        print(f"\n{'='*60}")
        print(f"Checking: {template_dir.name}")
        print('='*60)

        # Check all .tex.j2 files in this template directory
        template_files = list(template_dir.rglob('*.tex.j2'))

        if not template_files:
            print(f"  (no .tex.j2 files found)")
            continue

        for template_file in sorted(template_files):
            rel_path = template_file.relative_to(templates_base)
            try:
                # Try to load and compile the template
                env.get_template(str(rel_path))
                print(f"  ✓ {rel_path}")
                success_count += 1
            except Exception as e:
                errors.append((rel_path, str(e)))
                print(f"  ✗ {rel_path}: {e}")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    print(f"Templates checked: {success_count + len(errors)}")
    print(f"Passed: {success_count}")
    print(f"Failed: {len(errors)}")

    if errors:
        print(f"\n{'='*60}")
        print("ERRORS:")
        print('='*60)
        for path, error in errors:
            print(f"  {path}:")
            print(f"    {error}")
        return False
    else:
        print("\n✓ All templates are syntactically correct!")
        return True


if __name__ == '__main__':
    # Parse optional template name argument
    template_name = sys.argv[1] if len(sys.argv) > 1 else None
    success = check_templates(template_name)
    sys.exit(0 if success else 1)

