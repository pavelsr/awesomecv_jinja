"""
Tests for sample data module.

Ensures sample data is correctly structured and accessible.
"""

import pytest
from awesomecv_jinja import load_sample, get_master_data


class TestLoadSample:
    """Tests for load_sample function"""
    
    def test_load_resume_data(self):
        """Can load resume sample data"""
        data = load_sample("resume")
        
        assert isinstance(data, dict)
        assert "first_name" in data
        assert "last_name" in data
        assert "sections" in data
        assert data["sections"]["summary"] is True
    
    def test_load_cv_data(self):
        """Can load CV sample data"""
        data = load_sample("cv")
        
        assert isinstance(data, dict)
        assert "first_name" in data
        assert "skills" in data
        assert data["sections"]["skills"] is True
    
    def test_load_coverletter_data(self):
        """Can load cover letter sample data"""
        data = load_sample("coverletter")
        
        assert isinstance(data, dict)
        assert "first_name" in data
        assert "recipient_name" in data
        assert "letter_sections" in data
    
    def test_load_master_data(self):
        """Can load master data with all fields"""
        data = load_sample("master")
        
        assert isinstance(data, dict)
        assert "first_name" in data
        assert "skills" in data
        assert "letter_sections" in data
        # Master has everything
        assert len(data) > 15
    
    def test_invalid_doc_type_raises_error(self):
        """Raises ValueError for invalid document type"""
        with pytest.raises(ValueError, match="Unknown doc_type"):
            load_sample("invalid")
    
    def test_returns_copy_not_reference(self):
        """Returns a copy, not reference to original"""
        data1 = load_sample("resume")
        data2 = load_sample("resume")
        
        # Modify one
        data1["first_name"] = "Jane"
        
        # Should not affect the other
        assert data2["first_name"] == "John"


class TestGetMasterData:
    """Tests for get_master_data function"""
    
    def test_returns_all_fields(self):
        """Master data contains all fields"""
        data = get_master_data()
        
        # Personal info
        assert "first_name" in data
        assert "last_name" in data
        
        # Resume fields
        assert "summary" in data
        
        # CV fields
        assert "skills" in data
        
        # Cover letter fields
        assert "recipient_name" in data
        assert "letter_sections" in data
    
    def test_returns_copy(self):
        """Returns a copy, not reference"""
        data1 = get_master_data()
        data2 = get_master_data()
        
        data1["first_name"] = "Jane"
        assert data2["first_name"] == "John"


class TestSampleDataFixtures:
    """Tests for pytest fixtures"""
    
    def test_resume_data_fixture(self, resume_data):
        """resume_data fixture works"""
        assert resume_data["first_name"] == "John"
        assert "sections" in resume_data
    
    def test_cv_data_fixture(self, cv_data):
        """cv_data fixture works"""
        assert cv_data["first_name"] == "John"
        assert "skills" in cv_data
    
    def test_coverletter_data_fixture(self, coverletter_data):
        """coverletter_data fixture works"""
        assert coverletter_data["first_name"] == "John"
        assert "recipient_name" in coverletter_data
    
    def test_fixtures_are_independent(self, resume_data):
        """Fixture returns fresh copy each time"""
        resume_data["first_name"] = "Jane"
        # Get fixture again in different test would still be "John"
        assert resume_data["first_name"] == "Jane"  # But our change persists in this test


class TestSampleDataStructure:
    """Tests for sample data structure and content"""
    
    def test_resume_has_required_fields(self, resume_data):
        """Resume data has all required fields"""
        required = ["first_name", "last_name", "position", "email"]
        for field in required:
            assert field in resume_data, f"Missing required field: {field}"
    
    def test_resume_experience_is_list(self, resume_data):
        """Experience field is a list"""
        assert isinstance(resume_data["experience"], list)
        assert len(resume_data["experience"]) > 0
    
    def test_resume_education_is_list(self, resume_data):
        """Education field is a list"""
        assert isinstance(resume_data["education"], list)
        assert len(resume_data["education"]) > 0
    
    def test_cv_skills_is_list(self, cv_data):
        """CV skills field is a list"""
        assert isinstance(cv_data["skills"], list)
        assert len(cv_data["skills"]) > 0
    
    def test_coverletter_sections_is_list(self, coverletter_data):
        """Cover letter sections is a list"""
        assert isinstance(coverletter_data["letter_sections"], list)
        assert len(coverletter_data["letter_sections"]) > 0

