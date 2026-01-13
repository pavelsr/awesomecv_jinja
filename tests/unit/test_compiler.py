"""
Tests for compiler module.

Tests PDF compilation functionality.
"""

import pytest
from pathlib import Path

from awesomecv_jinja.compiler import PDFCompiler, CompilationEngine
from awesomecv_jinja.exceptions import CompilationError


class TestCompilationEngine:
    """Tests for CompilationEngine enum"""
    
    def test_enum_values(self):
        """All engines have correct values"""
        assert CompilationEngine.AUTO.value == "auto"
        assert CompilationEngine.XELATEX.value == "xelatex"
        assert CompilationEngine.DOCKER.value == "docker"
        assert CompilationEngine.DOCKER_SUDO.value == "docker-sudo"


class TestPDFCompilerInit:
    """Tests for PDFCompiler initialization"""
    
    def test_init_with_defaults(self):
        """Initializes with default values"""
        compiler = PDFCompiler()
        assert compiler.engine == CompilationEngine.AUTO
        assert compiler.timeout == 60
    
    def test_init_with_custom_engine(self):
        """Can specify custom engine"""
        compiler = PDFCompiler(engine="xelatex")
        assert compiler.engine == CompilationEngine.XELATEX
    
    def test_init_with_custom_timeout(self):
        """Can specify custom timeout"""
        compiler = PDFCompiler(timeout=120)
        assert compiler.timeout == 120


class TestPDFCompilerAvailability:
    """Tests for engine availability checking"""
    
    def test_is_available_xelatex(self):
        """Can check if xelatex is available"""
        compiler = PDFCompiler()
        result = compiler.is_available(CompilationEngine.XELATEX)
        assert isinstance(result, bool)
    
    def test_is_available_docker(self):
        """Can check if docker is available"""
        compiler = PDFCompiler()
        result = compiler.is_available(CompilationEngine.DOCKER)
        assert isinstance(result, bool)
    
    def test_detect_engine_returns_valid_engine(self):
        """detect_engine returns a valid engine or raises error"""
        compiler = PDFCompiler()
        
        try:
            engine = compiler.detect_engine()
            assert isinstance(engine, CompilationEngine)
            assert engine in [CompilationEngine.XELATEX, CompilationEngine.DOCKER]
        except CompilationError:
            # Expected if neither xelatex nor docker is available
            pass


class TestPDFCompilerCompile:
    """Tests for compile_file method"""
    
    def test_compile_file_requires_existing_file(self):
        """Raises FileNotFoundError for non-existent file"""
        compiler = PDFCompiler()
        
        with pytest.raises(FileNotFoundError, match="not found"):
            compiler.compile_file("nonexistent.tex")
    
    def test_compile_file_with_invalid_engine_raises_error(self):
        """Raises CompilationError if specified engine not available"""
        import shutil
        
        compiler = PDFCompiler(engine="xelatex")
        
        # Only test if xelatex is actually not available
        if not shutil.which("xelatex"):
            # Create dummy tex file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
                f.write("\\documentclass{article}\\begin{document}test\\end{document}")
                tex_file = f.name
            
            try:
                with pytest.raises(CompilationError, match="not available"):
                    compiler.compile_file(tex_file)
            finally:
                Path(tex_file).unlink(missing_ok=True)


class TestPDFCompilerCleanup:
    """Tests for artifact cleanup"""
    
    def test_cleanup_artifacts(self, tmp_path):
        """Cleanup removes auxiliary files"""
        compiler = PDFCompiler()
        
        # Create dummy artifacts
        tex_file = tmp_path / "test.tex"
        tex_file.write_text("test")
        
        for ext in ['.aux', '.log', '.out']:
            (tmp_path / f"test{ext}").write_text("dummy")
        
        # Run cleanup
        compiler._cleanup_artifacts(tex_file)
        
        # Artifacts should be removed
        assert not (tmp_path / "test.aux").exists()
        assert not (tmp_path / "test.log").exists()
        assert not (tmp_path / "test.out").exists()
        
        # Original tex should still exist
        assert tex_file.exists()

