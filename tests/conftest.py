"""
Pytest configuration and shared fixtures.

Provides sample data fixtures for all tests.
"""

import pytest
from pathlib import Path


@pytest.fixture
def resume_data():
    """
    Sample resume data for testing.
    
    Returns a fresh copy for each test to avoid mutations.
    """
    from awesomecv_jinja.samples import load_sample
    return load_sample("resume")


@pytest.fixture
def cv_data():
    """
    Sample CV data for testing.
    
    Returns a fresh copy for each test to avoid mutations.
    """
    from awesomecv_jinja.samples import load_sample
    return load_sample("cv")


@pytest.fixture
def coverletter_data():
    """
    Sample cover letter data for testing.
    
    Returns a fresh copy for each test to avoid mutations.
    """
    from awesomecv_jinja.samples import load_sample
    return load_sample("coverletter")


@pytest.fixture
def master_data():
    """
    Complete master data with all fields.
    
    Returns a fresh copy for each test to avoid mutations.
    """
    from awesomecv_jinja.samples import get_master_data
    return get_master_data()


@pytest.fixture
def base_data():
    """
    Minimal required data for any document.
    
    Useful for testing with minimal setup.
    """
    return {
        "first_name": "John",
        "last_name": "Doe",
        "position": "Engineer",
        "email": "john@example.com",
        "sections": {},
    }


@pytest.fixture
def tmp_render_dir(tmp_path):
    """
    Temporary directory for rendering tests.
    
    Automatically cleaned up after test completes.
    """
    render_dir = tmp_path / "render"
    render_dir.mkdir()
    return render_dir


@pytest.fixture
def template_dir():
    """Path to templates directory."""
    return Path("src/awesomecv_jinja/templates")


@pytest.fixture
def awesome_cv_template_dir(template_dir):
    """Path to Awesome-CV template directory."""
    return template_dir / "awesome_cv"

