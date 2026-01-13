#!/usr/bin/env python3
"""
Demo: Complete working example of awesomecv-jinja

Shows basic and advanced usage with the new Pipeline API.
"""

from pathlib import Path
from awesomecv_jinja import render, render_pdf, Renderer, load_sample


def demo_simple():
    """Simple one-liner usage"""
    print("=== Demo 1: Simple Usage ===\n")
    
    # Load sample data
    data = load_sample("resume")
    
    # Render to .tex file
    output = render(data, output="output/simple_resume.tex")
    
    print(f"✅ Resume rendered: {len(output)} characters")
    print(f"✅ Saved to: output/simple_resume.tex")
    print()


def demo_customized():
    """Customized data"""
    print("=== Demo 2: Customized Data ===\n")
    
    # Load and customize
    data = load_sample("resume")
    data["first_name"] = "Jane"
    data["last_name"] = "Smith"
    data["position"] = "Senior Cloud Architect"
    
    # Render
    output = render(data, output="output/customized_resume.tex")
    
    print(f"✅ Customized resume for {data['first_name']} {data['last_name']}")
    print(f"✅ Position: {data['position']}")
    print()


def demo_different_types():
    """Different document types"""
    print("=== Demo 3: Different Document Types ===\n")
    
    renderer = Renderer(template="awesome_cv")
    
    # Resume
    resume_data = load_sample("resume")
    renderer.render("resume", resume_data, output="output/resume.tex")
    print("✅ Resume generated")
    
    # CV
    cv_data = load_sample("cv")
    renderer.render("cv", cv_data, output="output/cv.tex")
    print("✅ CV generated")
    
    # Cover Letter
    letter_data = load_sample("coverletter")
    renderer.render("coverletter", letter_data, output="output/coverletter.tex")
    print("✅ Cover letter generated")
    
    print()


def demo_template_info():
    """Show template information"""
    print("=== Demo 4: Template Information ===\n")
    
    renderer = Renderer()
    
    # Get info
    info = renderer.get_template_info()
    print(f"Template: {info['name']}")
    print(f"Document types: {', '.join(info['document_types'])}")
    print()


def demo_pdf_generation():
    """Generate PDF directly (new Pipeline API)"""
    print("=== Demo 5: Direct PDF Generation ===\n")
    
    # Load sample data
    data = load_sample("resume")
    
    # Generate PDF in one line!
    try:
        pdf = render_pdf(data, output="output/demo_resume.pdf")
        print(f"✅ PDF created: {pdf}")
        print(f"📊 Size: {pdf.stat().st_size // 1024} KB")
    except Exception as e:
        print(f"❌ PDF generation failed: {e}")
        print("ℹ️  Make sure xelatex or Docker is available")
    
    print()


def demo_pdf_with_tex():
    """Generate PDF and keep .tex file"""
    print("=== Demo 6: PDF + TEX ===\n")
    
    data = load_sample("resume")
    
    try:
        # Generate PDF and keep .tex
        pdf = render_pdf(data, output="output/resume_with_tex.pdf", keep_tex=True)
        tex = pdf.with_suffix(".tex")
        
        print(f"✅ PDF created: {pdf}")
        print(f"✅ TEX saved: {tex}")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    print()


if __name__ == "__main__":
    print("=" * 70)
    print("awesomecv-jinja - Demo")
    print("=" * 70)
    print()
    
    # Create output directory
    Path("output").mkdir(exist_ok=True)
    
    # Run demos
    demo_simple()
    demo_customized()
    demo_different_types()
    demo_template_info()
    demo_pdf_generation()
    demo_pdf_with_tex()
    
    print("=" * 70)
    print("✅ All demos completed!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Check generated files in output/")
    print("2. Try pdf_example.py for more PDF examples")
    print("3. Customize data for your own use")
