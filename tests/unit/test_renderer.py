"""
Tests for renderer module.

Tests Renderer class and render function.
"""

import pytest
from pathlib import Path

from awesomecv_jinja import Renderer, render
from awesomecv_jinja.exceptions import (
    TemplateNotFoundError,
    DocumentTypeNotFoundError,
)


class TestRendererInit:
    """Tests for Renderer initialization"""
    
    def test_init_with_default_template(self):
        """Initializes with default awesome_cv template"""
        renderer = Renderer()
        assert renderer.template == "awesome_cv"
    
    def test_init_with_explicit_template(self):
        """Initializes with explicit template"""
        renderer = Renderer(template="awesome_cv")
        assert renderer.template == "awesome_cv"
    
    def test_init_with_invalid_template_raises_error(self):
        """Raises TemplateNotFoundError for invalid template"""
        with pytest.raises(TemplateNotFoundError, match="not found"):
            Renderer(template="nonexistent")
    
    def test_creates_jinja_environment(self):
        """Creates Jinja2 environment on init"""
        renderer = Renderer()
        assert renderer.env is not None
        # Check custom delimiters
        assert renderer.env.variable_start_string == '((('


class TestRendererListDocumentTypes:
    """Tests for list_document_types method"""
    
    def test_lists_available_types(self):
        """Lists available document types"""
        renderer = Renderer()
        types = renderer.list_document_types()
        
        assert isinstance(types, list)
        assert len(types) > 0
    
    def test_includes_resume(self):
        """Includes resume in available types"""
        renderer = Renderer()
        types = renderer.list_document_types()
        assert "resume" in types
    
    def test_includes_cv(self):
        """Includes cv in available types"""
        renderer = Renderer()
        types = renderer.list_document_types()
        assert "cv" in types
    
    def test_includes_coverletter(self):
        """Includes coverletter in available types"""
        renderer = Renderer()
        types = renderer.list_document_types()
        assert "coverletter" in types


class TestRendererGetTemplateInfo:
    """Tests for get_template_info method"""
    
    def test_returns_template_info(self):
        """Returns dictionary with template information"""
        renderer = Renderer()
        info = renderer.get_template_info()
        
        assert isinstance(info, dict)
        assert 'name' in info
        assert 'custom' in info
        assert 'document_types' in info
    
    def test_info_contains_correct_name(self):
        """Template name matches initialization"""
        renderer = Renderer(template="awesome_cv")
        info = renderer.get_template_info()
        assert info['name'] == "awesome_cv"
    
    def test_info_custom_false_for_builtin(self):
        """custom flag is False for built-in templates"""
        renderer = Renderer()
        info = renderer.get_template_info()
        assert info['custom'] is False


class TestRendererRender:
    """Tests for render method"""
    
    def test_render_returns_string(self, resume_data):
        """render() returns a string"""
        renderer = Renderer()
        result = renderer.render("resume", resume_data)
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_render_contains_data(self, resume_data):
        """Rendered output contains input data"""
        renderer = Renderer()
        result = renderer.render("resume", resume_data)
        
        # Should contain personal info
        assert resume_data["first_name"] in result
        assert resume_data["last_name"] in result
    
    def test_render_produces_latex(self, resume_data):
        """Rendered output is LaTeX document"""
        renderer = Renderer()
        result = renderer.render("resume", resume_data)
        
        # Should have LaTeX structure
        assert r"\documentclass" in result
        assert r"\begin{document}" in result
        assert r"\end{document}" in result
    
    def test_render_with_invalid_doc_type_raises_error(self, resume_data):
        """Raises DocumentTypeNotFoundError for invalid document type"""
        renderer = Renderer()
        with pytest.raises(DocumentTypeNotFoundError, match="not found"):
            renderer.render("invalid", resume_data)
    
    def test_render_to_file(self, resume_data, tmp_render_dir):
        """Saves rendered output to file"""
        renderer = Renderer()
        output_path = tmp_render_dir / "test.tex"
        
        renderer.render("resume", resume_data, output=output_path)
        
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        
        # Content should be same as non-file render
        content = output_path.read_text()
        expected = renderer.render("resume", resume_data)
        assert content == expected
    
    def test_render_creates_output_directory(self, resume_data, tmp_render_dir):
        """Creates output directory if it doesn't exist"""
        renderer = Renderer()
        output_path = tmp_render_dir / "subdir" / "test.tex"
        
        renderer.render("resume", resume_data, output=output_path)
        
        assert output_path.exists()
    
    def test_render_different_doc_types(self, resume_data, cv_data, coverletter_data):
        """Can render different document types"""
        renderer = Renderer()
        
        resume = renderer.render("resume", resume_data)
        cv = renderer.render("cv", cv_data)
        letter = renderer.render("coverletter", coverletter_data)
        
        # All should be different
        assert resume != cv
        assert resume != letter
        assert cv != letter
        
        # All should be LaTeX
        for output in [resume, cv, letter]:
            assert r"\documentclass" in output


class TestRenderFunction:
    """Tests for convenience render() function"""
    
    def test_render_function_works(self, resume_data):
        """render() function works"""
        result = render(resume_data)
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_render_function_default_doc_type(self, resume_data):
        """Defaults to resume document type"""
        result = render(resume_data)
        assert resume_data["first_name"] in result
    
    def test_render_function_with_doc_type(self, cv_data):
        """Can specify document type"""
        result = render(cv_data, doc_type="cv")
        assert cv_data["first_name"] in result
    
    def test_render_function_with_output(self, resume_data, tmp_render_dir):
        """Can save to file"""
        output_path = tmp_render_dir / "test.tex"
        render(resume_data, output=output_path)
        
        assert output_path.exists()
    
    def test_render_function_with_template(self, resume_data):
        """Can specify template"""
        result = render(resume_data, template="awesome_cv")
        assert isinstance(result, str)

