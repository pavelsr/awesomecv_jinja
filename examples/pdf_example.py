#!/usr/bin/env python3
"""
Example: Direct PDF generation using render_pdf()

Shows how to generate PDF directly from data without intermediate .tex files.
"""

from pathlib import Path
from awesomecv_jinja import render_pdf, load_sample


def main():
    """Generate PDFs for all document types"""
    
    print("=" * 70)
    print("PDF Generation Example")
    print("=" * 70)
    print()
    
    # Create output directory
    output_dir = Path("output/pdf")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Example 1: Simple PDF generation
    print("1. Generating Resume PDF...")
    try:
        data = load_sample("resume")
        pdf = render_pdf(data, output=output_dir / "resume.pdf")
        print(f"   ✅ PDF created: {pdf}")
        print(f"   📊 Size: {pdf.stat().st_size // 1024} KB")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    print()
    
    # Example 2: Generate CV PDF
    print("2. Generating CV PDF...")
    try:
        cv_data = load_sample("cv")
        pdf = render_pdf(cv_data, doc_type="cv", output=output_dir / "cv.pdf")
        print(f"   ✅ PDF created: {pdf}")
        print(f"   📊 Size: {pdf.stat().st_size // 1024} KB")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    print()
    
    # Example 3: Generate Cover Letter PDF
    print("3. Generating Cover Letter PDF...")
    try:
        letter_data = load_sample("coverletter")
        pdf = render_pdf(
            letter_data,
            doc_type="coverletter",
            output=output_dir / "coverletter.pdf"
        )
        print(f"   ✅ PDF created: {pdf}")
        print(f"   📊 Size: {pdf.stat().st_size // 1024} KB")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    print()
    
    # Example 4: Keep .tex file
    print("4. Generating with .tex file preserved...")
    try:
        data = load_sample("resume")
        pdf = render_pdf(
            data,
            output=output_dir / "resume_with_tex.pdf",
            keep_tex=True  # Also saves .tex
        )
        tex_file = pdf.with_suffix(".tex")
        print(f"   ✅ PDF created: {pdf}")
        print(f"   ✅ TEX saved: {tex_file}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    print()
    
    # Example 5: Specify compilation engine
    print("5. Using specific engine (Docker)...")
    try:
        data = load_sample("resume")
        pdf = render_pdf(
            data,
            output=output_dir / "resume_docker.pdf",
            engine="docker"  # Force Docker
        )
        print(f"   ✅ PDF created with Docker: {pdf}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        print("   ℹ️  Docker might not be available")
    print()
    
    # Example 6: Customized data
    print("6. Generating PDF with customized data...")
    try:
        data = load_sample("resume")
        data["first_name"] = "Jane"
        data["last_name"] = "Smith"
        data["position"] = "Senior Cloud Architect"
        
        pdf = render_pdf(data, output=output_dir / "jane_smith_resume.pdf")
        print(f"   ✅ Custom resume for Jane Smith: {pdf}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    print()
    
    print("=" * 70)
    print("✅ Example completed!")
    print("=" * 70)
    print()
    print("Generated files in:", output_dir)
    print()
    print("Note:")
    print("  - If PDF generation failed, install xelatex or Docker")
    print("  - xelatex: sudo apt install texlive-xetex")
    print("  - Docker: https://docs.docker.com/get-docker/")


if __name__ == "__main__":
    main()

