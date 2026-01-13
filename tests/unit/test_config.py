"""
Tests for config module.

Tests Jinja2 environment configuration and LaTeX filters.
"""

import pytest
from jinja2 import Environment

from awesomecv_jinja.config import create_latex_environment, latex_escape


class TestLatexEscape:
    """Tests for latex_escape filter"""
    
    def test_escapes_ampersand(self):
        """Escapes & character"""
        assert latex_escape("A & B") == r"A \& B"
    
    def test_escapes_percent(self):
        """Escapes % character"""
        assert latex_escape("100%") == r"100\%"
    
    def test_escapes_dollar(self):
        """Escapes $ character"""
        assert latex_escape("$100") == r"\$100"
    
    def test_escapes_hash(self):
        """Escapes # character"""
        assert latex_escape("#tag") == r"\#tag"
    
    def test_escapes_underscore(self):
        """Escapes _ character"""
        assert latex_escape("file_name") == r"file\_name"
    
    def test_escapes_braces(self):
        """Escapes { and } characters"""
        assert latex_escape("{text}") == r"\{text\}"
    
    def test_escapes_tilde(self):
        """Escapes ~ character"""
        assert latex_escape("~user") == r"\textasciitilde{}user"
    
    def test_escapes_caret(self):
        """Escapes ^ character"""
        assert latex_escape("x^2") == r"x\^{}2"
    
    def test_escapes_backslash(self):
        """Escapes \\ character (must be first!)"""
        assert latex_escape("C:\\Users") == r"C:\textbackslash{}Users"
    
    def test_escapes_multiple_characters(self):
        """Escapes multiple special characters"""
        text = "Price: $100 & 50% off"
        expected = r"Price: \$100 \& 50\% off"
        assert latex_escape(text) == expected
    
    def test_empty_string(self):
        """Handles empty string"""
        assert latex_escape("") == ""
    
    def test_plain_text(self):
        """Doesn't modify plain text"""
        assert latex_escape("Hello World") == "Hello World"
    
    def test_non_string_input(self):
        """Converts non-string to string"""
        assert latex_escape(123) == "123"
        assert latex_escape(None) == "None"
    
    @pytest.mark.parametrize("char,expected", [
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\^{}"),
        ("\\", r"\textbackslash{}"),
    ])
    def test_each_special_character(self, char, expected):
        """Each special character is escaped correctly"""
        assert latex_escape(char) == expected


class TestCreateLatexEnvironment:
    """Tests for create_latex_environment function"""
    
    def test_creates_environment(self):
        """Creates a valid Jinja2 Environment"""
        env = create_latex_environment("awesome_cv")
        assert isinstance(env, Environment)
    
    def test_custom_delimiters(self):
        """Uses custom LaTeX-compatible delimiters"""
        env = create_latex_environment("awesome_cv")
        assert env.block_start_string == '((*'
        assert env.block_end_string == '*))'
        assert env.variable_start_string == '((('
        assert env.variable_end_string == ')))'
        assert env.comment_start_string == '((#'
        assert env.comment_end_string == '#))'
    
    def test_autoescape_disabled(self):
        """Autoescape is disabled for LaTeX"""
        env = create_latex_environment("awesome_cv")
        assert env.autoescape is False
    
    def test_trim_blocks_enabled(self):
        """trim_blocks and lstrip_blocks are enabled"""
        env = create_latex_environment("awesome_cv")
        assert env.trim_blocks is True
        assert env.lstrip_blocks is True
    
    def test_latex_escape_filter_registered(self):
        """latex_escape filter is registered"""
        env = create_latex_environment("awesome_cv")
        assert 'latex_escape' in env.filters
        assert env.filters['latex_escape'] is latex_escape
    
    def test_can_parse_template_with_variables(self):
        """Can parse template with custom variable delimiters"""
        env = create_latex_environment("awesome_cv")
        template_str = r"\name{((( first_name )))}{((( last_name )))}"
        template = env.from_string(template_str)
        result = template.render(first_name="John", last_name="Doe")
        assert result == r"\name{John}{Doe}"
    
    def test_can_parse_template_with_blocks(self):
        """Can parse template with custom block delimiters"""
        env = create_latex_environment("awesome_cv")
        template_str = "((* if name *))\nName: ((( name )))\n((* endif *))"
        template = env.from_string(template_str)
        result = template.render(name="John")
        assert "Name: John" in result
    
    def test_can_parse_template_with_comments(self):
        """Can parse template with custom comment delimiters"""
        env = create_latex_environment("awesome_cv")
        template_str = "((# This is a comment #))\nHello"
        template = env.from_string(template_str)
        result = template.render()
        assert result.strip() == "Hello"
        assert "comment" not in result
    
    def test_latex_escape_filter_works_in_template(self):
        """latex_escape filter works in templates"""
        env = create_latex_environment("awesome_cv")
        template_str = "((( text | latex_escape )))"
        template = env.from_string(template_str)
        result = template.render(text="100% & more")
        assert result == r"100\% \& more"

