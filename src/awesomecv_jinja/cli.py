#!/usr/bin/env python3
"""
awesomecv-jinja CLI - Generate CV/Resume PDFs from YAML

Simple command-line interface for generating professional CVs and resumes.
"""

import argparse
import sys
from pathlib import Path
from typing import NoReturn

try:
    import yaml
except ImportError:
    print(
        "❌ Error: PyYAML is not installed. Install it with: pip install pyyaml",
        file=sys.stderr,
    )
    sys.exit(1)

from .pipeline import render_pdf
from .renderer import render
from .compiler import PDFCompiler
from .exceptions import AwesomeCVJinjaError
from . import __version__


def main() -> NoReturn:
    """Main entry point for the acv CLI command."""
    parser = argparse.ArgumentParser(
        prog="acv",
        description="Generate CV/Resume PDFs from YAML or compile existing .tex files",
        epilog="Examples:\n"
               "  YAML input (render + compile):\n"
               "    acv resume.yaml                                  # Generate resume.pdf\n"
               "    acv cv.yaml -d cv -o my_cv.pdf                   # Specify output\n"
               "    acv data.yaml -e xelatex --save-tex              # Use xelatex engine\n"
               "    acv resume.yaml -e auto                          # Auto-detect engine\n"
               "\n"
               "  TEX input (compile only):\n"
               "    acv resume.tex                                   # Compile to resume.pdf\n"
               "    acv document.tex -e xelatex -o output.pdf        # Custom engine/output",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Positional argument: input file (YAML or TEX)
    parser.add_argument(
        "input_file",
        type=Path,
        help="YAML file with CV data or .tex file to compile",
    )

    # Optional arguments
    parser.add_argument(
        "-d",
        "--doctype",
        choices=["resume", "cv", "coverletter"],
        default="resume",
        help="document type to generate (YAML input only, default: resume)",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output PDF file path (default: input_name.pdf)",
    )

    parser.add_argument(
        "--save-tex",
        action="store_true",
        help="save intermediate LaTeX (.tex) file alongside PDF",
    )

    parser.add_argument(
        "--tex-only",
        action="store_true",
        help="generate only LaTeX (.tex) file without compiling to PDF",
    )

    parser.add_argument(
        "-e",
        "--engine",
        choices=["auto", "xelatex", "docker", "docker-sudo"],
        default="docker-sudo",
        help="PDF compilation engine (default: docker-sudo)",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    # Parse arguments
    args = parser.parse_args()

    # Validate input file exists
    if not args.input_file.exists():
        print(f"❌ Error: File not found: {args.input_file}", file=sys.stderr)
        sys.exit(1)

    if not args.input_file.is_file():
        print(f"❌ Error: Not a file: {args.input_file}", file=sys.stderr)
        sys.exit(1)

    # Check if input is a .tex file (direct compilation mode)
    if args.input_file.suffix.lower() == ".tex":
        # TEX mode: compile existing .tex file to PDF
        if args.tex_only:
            print(
                "❌ Error: --tex-only cannot be used with .tex input file",
                file=sys.stderr,
            )
            sys.exit(1)
        
        print(f"🔨 Compiling LaTeX file: {args.input_file}")
        print(f"📦 Using engine: {args.engine}")
        
        try:
            compiler = PDFCompiler(engine=args.engine)
            output_path = args.output or args.input_file.with_suffix(".pdf")
            pdf_path = compiler.compile_file(
                args.input_file,
                output=output_path,
                keep_artifacts=args.save_tex,
            )
            print(f"✅ PDF created: {pdf_path}")
            
            if args.save_tex:
                print(f"📄 LaTeX source: {args.input_file}")
            
            sys.exit(0)
            
        except AwesomeCVJinjaError as e:
            print(f"❌ Compilation error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"❌ Unexpected error: {e}", file=sys.stderr)
            sys.exit(1)

    # YAML mode: Load YAML data and render template
    try:
        with open(args.input_file, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"❌ Error: Invalid YAML file: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, dict):
        print(
            f"❌ Error: YAML must contain a dictionary, got {type(data).__name__}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Determine output path
    if args.tex_only:
        output_path = args.output or args.input_file.with_suffix(".tex")
    else:
        output_path = args.output or args.input_file.with_suffix(".pdf")

    # Generate document
    try:
        if args.tex_only:
            # Generate only .tex file
            print(f"🔨 Generating {args.doctype} LaTeX from {args.input_file}...")
            render(
                data,
                doc_type=args.doctype,
                output=output_path,
            )
            print(f"✅ LaTeX created: {output_path}")
        else:
            # Generate PDF (and optionally keep .tex)
            print(f"🔨 Generating {args.doctype} PDF from {args.input_file}...")
            print(f"📦 Using engine: {args.engine}")
            pdf_path = render_pdf(
                data,
                doc_type=args.doctype,
                output=output_path,
                engine=args.engine,
                keep_tex=args.save_tex,
            )
            print(f"✅ PDF created: {pdf_path}")

            if args.save_tex:
                tex_path = output_path.with_suffix(".tex")
                if tex_path.exists():
                    print(f"📄 LaTeX saved: {tex_path}")

    except AwesomeCVJinjaError as e:
        print(f"❌ Generation error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()

