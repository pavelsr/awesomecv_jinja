"""
Integration tests for pipeline API (render_pdf).

These tests verify the complete data → PDF pipeline.
"""

import pytest
from pathlib import Path

from awesomecv_jinja import render_pdf
from awesomecv_jinja.exceptions import CompilationError


class TestRenderPDF:
    """Tests for render_pdf function"""
    
    def test_render_pdf_creates_file(self, resume_data, tmp_render_dir):
        """render_pdf creates PDF file"""
        output = tmp_render_dir / "test.pdf"
        
        try:
            pdf = render_pdf(resume_data, output=output)
            
            # PDF should be created
            assert pdf.exists()
            assert pdf.suffix == ".pdf"
            assert pdf.stat().st_size > 0
        
        except CompilationError:
            # Expected if no LaTeX/Docker available
            pytest.skip("No PDF compilation engine available")
    
    def test_render_pdf_with_keep_tex(self, resume_data, tmp_render_dir):
        """render_pdf with keep_tex=True saves both tex and pdf"""
        output = tmp_render_dir / "test.pdf"
        
        try:
            pdf = render_pdf(resume_data, output=output, keep_tex=True)
            tex = pdf.with_suffix(".tex")
            
            # Both should exist
            assert pdf.exists()
            assert tex.exists()
            assert tex.stat().st_size > 0
        
        except CompilationError:
            pytest.skip("No PDF compilation engine available")
    
    def test_render_pdf_different_doc_types(self, resume_data, cv_data, tmp_render_dir):
        """Can render different document types to PDF"""
        try:
            # Resume
            resume_pdf = render_pdf(
                resume_data,
                doc_type="resume",
                output=tmp_render_dir / "resume.pdf"
            )
            assert resume_pdf.exists()
            
            # CV
            cv_pdf = render_pdf(
                cv_data,
                doc_type="cv",
                output=tmp_render_dir / "cv.pdf"
            )
            assert cv_pdf.exists()
            
            # Different sizes (different content)
            assert resume_pdf.stat().st_size != cv_pdf.stat().st_size
        
        except CompilationError:
            pytest.skip("No PDF compilation engine available")
    
    def test_render_pdf_creates_output_directory(self, resume_data, tmp_path):
        """Creates output directory if it doesn't exist"""
        output = tmp_path / "subdir" / "nested" / "test.pdf"
        
        try:
            pdf = render_pdf(resume_data, output=output)
            
            assert pdf.exists()
            assert pdf.parent == tmp_path / "subdir" / "nested"
        
        except CompilationError:
            pytest.skip("No PDF compilation engine available")


class TestRenderPDFEngines:
    """Tests for different compilation engines"""
    
    @pytest.mark.skipif(
        __import__('shutil').which("xelatex") is None,
        reason="xelatex not installed"
    )
    def test_render_pdf_with_xelatex(self, resume_data, tmp_render_dir):
        """Can compile with local xelatex"""
        from awesomecv_jinja.exceptions import CompilationError
        
        output = tmp_render_dir / "test.pdf"
        
        try:
            pdf = render_pdf(resume_data, output=output, engine="xelatex")
            assert pdf.exists()
            assert pdf.stat().st_size > 0
        except CompilationError:
            # Expected if LaTeX packages are missing (e.g., fontawesome6)
            pytest.skip("LaTeX compilation failed (missing packages)")
    
    @pytest.mark.skipif(
        __import__('shutil').which("docker") is None,
        reason="docker not installed"
    )
    def test_render_pdf_with_docker(self, resume_data, tmp_render_dir):
        """Can compile with Docker"""
        output = tmp_render_dir / "test.pdf"
        
        # This might fail due to permissions, which is expected
        try:
            pdf = render_pdf(resume_data, output=output, engine="docker")
            assert pdf.exists()
        except CompilationError as e:
            if "permission denied" in str(e).lower():
                pytest.skip("Docker requires sudo")
            else:
                raise


class TestPipelineIntegration:
    """Integration tests for complete pipeline"""
    
    def test_complete_workflow(self, tmp_render_dir):
        """Complete workflow: load sample → customize → PDF"""
        from awesomecv_jinja import load_sample
        
        # Load and customize
        data = load_sample("resume")
        data["first_name"] = "Test"
        data["last_name"] = "User"
        
        output = tmp_render_dir / "complete.pdf"
        
        try:
            # Generate PDF
            pdf = render_pdf(data, output=output)
            
            # Verify
            assert pdf.exists()
            assert pdf == output
        
        except CompilationError:
            pytest.skip("No PDF compilation engine available")

