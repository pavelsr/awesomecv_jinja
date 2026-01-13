"""
PDF compilation from LaTeX sources.

Supports multiple compilation methods with automatic fallback:
- Local xelatex (fastest)
- Docker with texlive/texlive:latest (no local LaTeX needed)
- Docker with sudo (for systems requiring elevated privileges)
"""

from enum import Enum
from pathlib import Path
from typing import Optional, Union, Literal
import subprocess
import shutil
import os

from .exceptions import CompilationError


class CompilationEngine(Enum):
    """Available PDF compilation engines."""
    
    AUTO = "auto"                # Auto-detect best available
    XELATEX = "xelatex"         # Local xelatex
    DOCKER = "docker"            # Docker with texlive
    DOCKER_SUDO = "docker-sudo"  # Docker with sudo


class PDFCompiler:
    """
    Compiles LaTeX files to PDF.
    
    Supports multiple compilation engines with automatic fallback.
    
    Examples:
        Auto-detection (recommended):
        
        >>> compiler = PDFCompiler()
        >>> pdf = compiler.compile_file("resume.tex")
        
        Specific engine:
        
        >>> compiler = PDFCompiler(engine="docker")
        >>> pdf = compiler.compile_file("resume.tex", output="resume.pdf")
        
        Keep intermediate files:
        
        >>> pdf = compiler.compile_file("resume.tex", keep_artifacts=True)
    """
    
    def __init__(
        self,
        engine: Literal["auto", "xelatex", "docker", "docker-sudo"] = "auto",
        timeout: int = 60,
    ):
        """
        Initialize PDF compiler.
        
        Args:
            engine: Compilation engine to use (default: auto-detect)
            timeout: Maximum compilation time in seconds (default: 60)
        """
        self.engine = CompilationEngine(engine)
        self.timeout = timeout
    
    def is_available(self, engine: CompilationEngine) -> bool:
        """
        Check if compilation engine is available.
        
        Args:
            engine: Engine to check
        
        Returns:
            True if engine is available, False otherwise
        """
        if engine == CompilationEngine.XELATEX:
            return shutil.which("xelatex") is not None
        elif engine in [CompilationEngine.DOCKER, CompilationEngine.DOCKER_SUDO]:
            return shutil.which("docker") is not None
        return False
    
    def detect_engine(self) -> CompilationEngine:
        """
        Auto-detect best available compilation engine.
        
        Priority: xelatex > docker > error
        
        Returns:
            Best available CompilationEngine
        
        Raises:
            CompilationError: If no engine is available
        """
        if self.is_available(CompilationEngine.XELATEX):
            return CompilationEngine.XELATEX
        elif self.is_available(CompilationEngine.DOCKER):
            return CompilationEngine.DOCKER
        else:
            raise CompilationError(
                "No PDF compilation engine available.\n"
                "Install one of:\n"
                "  - texlive-xetex: sudo apt install texlive-xetex\n"
                "  - Docker: https://docs.docker.com/get-docker/"
            )
    
    def compile_file(
        self,
        tex_file: Union[str, Path],
        output: Optional[Union[str, Path]] = None,
        keep_artifacts: bool = False,
    ) -> Path:
        """
        Compile .tex file to PDF.
        
        Args:
            tex_file: Path to .tex file
            output: Optional output PDF path (default: same name with .pdf)
            keep_artifacts: Keep auxiliary files (.aux, .log, etc.)
        
        Returns:
            Path to generated PDF file
        
        Raises:
            FileNotFoundError: If tex file doesn't exist
            CompilationError: If compilation fails
        
        Examples:
            >>> compiler = PDFCompiler()
            >>> pdf = compiler.compile_file("resume.tex")
            >>> print(pdf)
            PosixPath('resume.pdf')
        """
        tex_path = Path(tex_file)
        if not tex_path.exists():
            raise FileNotFoundError(f"TeX file not found: {tex_path}")
        
        # Determine engine to use
        if self.engine == CompilationEngine.AUTO:
            engine = self.detect_engine()
        else:
            engine = self.engine
            if not self.is_available(engine):
                raise CompilationError(
                    f"Compilation engine '{engine.value}' is not available"
                )
        
        # Compile with selected engine
        if engine == CompilationEngine.XELATEX:
            pdf_path = self._compile_with_xelatex(tex_path)
        elif engine == CompilationEngine.DOCKER:
            pdf_path = self._compile_with_docker(tex_path, use_sudo=False)
        elif engine == CompilationEngine.DOCKER_SUDO:
            pdf_path = self._compile_with_docker(tex_path, use_sudo=True)
        else:
            raise CompilationError(f"Unknown engine: {engine}")
        
        # Move to output location if specified
        if output:
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            if pdf_path != output_path:
                shutil.move(str(pdf_path), str(output_path))
                pdf_path = output_path
        
        # Clean up artifacts
        if not keep_artifacts:
            self._cleanup_artifacts(tex_path)
        
        return pdf_path
    
    def _compile_with_xelatex(self, tex_file: Path) -> Path:
        """Compile using local xelatex."""
        result = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", tex_file.name],
            cwd=tex_file.parent,
            capture_output=True,
            timeout=self.timeout,
            text=True
        )
        
        pdf_file = tex_file.with_suffix(".pdf")
        
        # Check if PDF was generated - this is the real success criteria
        if not pdf_file.exists():
            error = self._extract_latex_error(tex_file.with_suffix(".log"))
            raise CompilationError(
                f"xelatex compilation failed:\n{error}\n\n"
                f"See {tex_file.with_suffix('.log')} for details"
            )
        
        return pdf_file
    
    def _compile_with_docker(self, tex_file: Path, use_sudo: bool = False) -> Path:
        """Compile using Docker with texlive image."""
        uid = os.getuid()
        gid = os.getgid()
        
        cmd = [
            "docker", "run",
            "--rm",
            "--user", f"{uid}:{gid}",
            "-i",
            "-w", "/doc",
            "-v", f"{tex_file.parent.absolute()}:/doc",
            "texlive/texlive:latest",
            "xelatex", "-interaction=nonstopmode", tex_file.name
        ]
        
        if use_sudo:
            # Use sudo to run docker as root
            # Root has access to docker socket
            # Try to refresh sudo cache first
            try:
                subprocess.run(
                    ["sudo", "-v"],
                    check=False,
                    timeout=5,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except:
                pass  # Ignore if sudo -v fails
            
            cmd = ["sudo"] + cmd
        
        try:
            if use_sudo:
                # For sudo: allow full terminal access
                # This will allow password prompt if needed
                result = subprocess.run(
                    cmd,
                    cwd=tex_file.parent,
                    timeout=self.timeout,
                    text=True,
                    check=False
                )
                # Manually create result for consistency
                result = subprocess.CompletedProcess(
                    args=cmd,
                    returncode=result.returncode if hasattr(result, 'returncode') else 0,
                    stdout="",
                    stderr=""
                )
            else:
                # For non-sudo: capture output normally
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.DEVNULL,
                    cwd=tex_file.parent,
                    timeout=self.timeout,
                    text=True
                )
        except subprocess.TimeoutExpired as e:
            raise CompilationError(
                f"Docker compilation timed out after {self.timeout}s"
            ) from e
        
        pdf_file = tex_file.with_suffix(".pdf")
        
        # Check if PDF was generated - this is the real success criteria
        # LaTeX may return non-zero even if PDF was created (warnings, overfull boxes, etc.)
        if not pdf_file.exists():
            error_msg = result.stderr or result.stdout
            raise CompilationError(
                f"Docker compilation failed - no PDF generated:\n{error_msg}\n\n"
                f"Command: {' '.join(cmd)}"
            )
        
        return pdf_file
    
    def _extract_latex_error(self, log_file: Path) -> str:
        """Extract readable error message from LaTeX log."""
        if not log_file.exists():
            return "No log file generated"
        
        try:
            content = log_file.read_text()
            errors = [
                line for line in content.split('\n')
                if line.startswith('!')
            ]
            return '\n'.join(errors[:5]) if errors else "Unknown LaTeX error"
        except Exception:
            return "Could not read log file"
    
    def _cleanup_artifacts(self, tex_file: Path):
        """Remove auxiliary files generated by LaTeX."""
        artifacts = ['.aux', '.log', '.out', '.toc', '.fls', '.fdb_latexmk', '.synctex.gz']
        
        for ext in artifacts:
            artifact = tex_file.with_suffix(ext)
            if artifact.exists():
                try:
                    artifact.unlink()
                except Exception:
                    pass  # Ignore cleanup errors

