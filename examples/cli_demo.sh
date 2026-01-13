#!/bin/bash
# Demo script for acv CLI

echo "=== awesomecv-jinja CLI Demo ==="
echo ""

# Change to script directory
cd "$(dirname "$0")/.." || exit 1

# Detect if running in development mode with uv
if [ -f "pyproject.toml" ] && command -v uv &> /dev/null; then
    echo "📦 Using development mode (uv run)"
    ACV="uv run acv"
elif command -v acv &> /dev/null; then
    echo "✅ Using installed acv"
    ACV="acv"
else
    echo "❌ Error: acv command not found and uv is not available"
    echo "Install with: pip install awesomecv-jinja"
    echo "Or use: uv add awesomecv-jinja"
    exit 1
fi

echo ""

# Show version
echo "📌 Version:"
$ACV --version
echo ""

# Show help
echo "📚 Help:"
$ACV --help
echo ""

# Generate LaTeX from example
echo "🔨 Generating LaTeX from example_cli.yaml..."
cd examples || exit 1

if [ ! -f example_cli.yaml ]; then
    echo "❌ Error: example_cli.yaml not found"
    exit 1
fi

$ACV example_cli.yaml --tex-only -o demo_output.tex

if [ -f demo_output.tex ]; then
    echo "✅ Success! Generated demo_output.tex"
    echo ""
    echo "File size: $(du -h demo_output.tex | cut -f1)"
    echo ""
    echo "To compile to PDF manually:"
    echo "  xelatex demo_output.tex"
    echo ""
    echo "Or generate PDF directly:"
    echo "  acv example_cli.yaml -o demo_output.pdf"
else
    echo "❌ Failed to generate LaTeX"
    exit 1
fi

