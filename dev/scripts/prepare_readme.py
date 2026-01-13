#!/usr/bin/env python3
"""Prepare README for PyPI by converting relative links and adding HTML anchors.

This script reads README.md and:
1. Adds HTML anchors (<a id="..."></a>) before all markdown headings
   - PyPI's readme_renderer doesn't auto-generate IDs, so TOC links won't
     work without explicit anchors
   - Anchor IDs are generated using GitHub-compatible rules (lowercase,
     hyphens for spaces, special chars removed)
2. Converts relative markdown links to absolute GitHub URLs
   - Links like [docs/cli_usage.md](docs/cli_usage.md) become
     [docs/cli_usage.md](https://github.com/.../blob/main/docs/cli_usage.md)

The result is written to README_PYPI.md, which is used by PyPI.

Usage:
    python3 dev/scripts/prepare_readme.py

The script automatically extracts the repository URL from pyproject.toml.
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent


def get_github_base_url() -> str:
    """Extract GitHub repository URL from pyproject.toml.

    Returns:
        Base URL for raw file links (e.g., https://github.com/user/repo/blob/main)
    """
    pyproject_path = PROJECT_ROOT / "pyproject.toml"
    content = pyproject_path.read_text(encoding="utf-8")

    # Extract Repository URL from [project.urls]
    match = re.search(r'Repository\s*=\s*"([^"]+)"', content)
    if not match:
        # Fallback to Homepage
        match = re.search(r'Homepage\s*=\s*"([^"]+)"', content)

    if not match:
        print("Error: Could not find Repository or Homepage URL in pyproject.toml")
        sys.exit(1)

    repo_url = match.group(1).rstrip(".git")
    return f"{repo_url}/blob/main"


def generate_anchor_id(text: str) -> str:
    """Generate anchor ID from heading text (GitHub/PyPI compatible).

    Rules:
    - Convert to lowercase
    - Replace spaces with hyphens
    - Remove special characters (keep alphanumeric and hyphens)
    - Remove consecutive hyphens
    - Strip leading/trailing hyphens

    Args:
        text: Heading text

    Returns:
        Anchor ID string
    """
    # Normalize unicode (e.g., é -> e)
    text = unicodedata.normalize("NFKD", text)
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and underscores with hyphens
    text = re.sub(r'[\s_]+', '-', text)
    # Remove all non-alphanumeric characters except hyphens
    text = re.sub(r'[^\w\-]', '', text)
    # Remove consecutive hyphens
    text = re.sub(r'-+', '-', text)
    # Strip leading/trailing hyphens
    text = text.strip('-')
    return text


def add_heading_anchors(content: str) -> str:
    """Add HTML anchors before markdown headings for PyPI compatibility.

    PyPI's readme_renderer doesn't auto-generate IDs for headings, so we
    need to add them manually. This ensures TOC links work on PyPI.

    Args:
        content: Markdown content

    Returns:
        Content with HTML anchors added before headings
    """
    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if this is a heading (##, ###, etc.)
        heading_match = re.match(r'^(\s*)(#{2,6})\s+(.+)$', line)

        if heading_match:
            indent = heading_match.group(1)
            heading_text = heading_match.group(3)

            # Check if previous line is already an anchor
            has_anchor = False
            if i > 0:
                prev_line = result[-1].strip()
                if prev_line.startswith('<a id=') and prev_line.endswith('></a>'):
                    has_anchor = True

            # Add anchor if not already present
            if not has_anchor:
                anchor_id = generate_anchor_id(heading_text)
                result.append(f"{indent}<a id=\"{anchor_id}\"></a>")

            result.append(line)
        else:
            result.append(line)

        i += 1

    return '\n'.join(result)


def convert_relative_links(content: str, base_url: str) -> str:
    """Convert relative markdown links to absolute GitHub URLs.

    Args:
        content: Markdown content
        base_url: Base URL for absolute links

    Returns:
        Content with converted links
    """
    # Pattern for markdown links: [text](relative/path)
    # Excludes:
    # - URLs starting with http://, https://, mailto:, #
    # - Already absolute paths
    pattern = r'\[([^\]]+)\]\((?!https?://|mailto:|#)([^)]+)\)'

    def replace_link(match: re.Match) -> str:
        text = match.group(1)
        path = match.group(2)
        # Remove leading ./ if present
        path = path.lstrip("./")
        return f"[{text}]({base_url}/{path})"

    return re.sub(pattern, replace_link, content)


def main() -> None:
    """Main entry point."""
    readme_path = PROJECT_ROOT / "README.md"
    output_path = PROJECT_ROOT / "README_PYPI.md"

    if not readme_path.exists():
        print(f"Error: {readme_path} not found")
        sys.exit(1)

    print(f"Reading {readme_path}")
    content = readme_path.read_text(encoding="utf-8")

    base_url = get_github_base_url()
    print(f"Using base URL: {base_url}")

    # Step 1: Add HTML anchors before headings (for PyPI TOC support)
    print("Adding HTML anchors to headings...")
    content = add_heading_anchors(content)

    # Count anchors added (they appear before headings)
    anchor_count = len(re.findall(r'^<a id="[^"]+"></a>', content, re.MULTILINE))
    print(f"  Added anchors to {anchor_count} heading(s)")

    # Step 2: Convert relative links to absolute GitHub URLs
    converted = convert_relative_links(content, base_url)

    # Count converted links
    original_links = re.findall(r'\[([^\]]+)\]\((?!https?://|mailto:|#)([^)]+)\)', content)
    if original_links:
        print(f"Converted {len(original_links)} relative link(s):")
        for text, path in original_links:
            print(f"  - [{text}]({path})")

    output_path.write_text(converted, encoding="utf-8")
    print(f"Written to {output_path}")


if __name__ == "__main__":
    main()
