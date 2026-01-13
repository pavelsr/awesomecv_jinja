"""
Sample data for testing and quick start.

Provides ready-to-use example data for all document types.
Use as a starting point for your own CV data or for testing the library.

Examples:
    Quick start with sample data:
    
    >>> from awesomecv_jinja import render, load_sample
    >>> data = load_sample("resume")
    >>> render(data, output="resume.tex")
    
    Customize sample data:
    
    >>> data = load_sample("cv")
    >>> data["first_name"] = "Jane"
    >>> data["skills"].append({"category": "Languages", "items": "English, Spanish"})
"""

from typing import Literal
import copy


# Master data containing all fields for all document types
MASTER_DATA = {
    # ===== PERSONAL INFO (used in all document types) =====
    "first_name": "John",
    "last_name": "Doe",
    "position": r"Software Engineer{\enskip\cdotp\enskip}DevOps Specialist",
    "address": "123 Main Street, San Francisco, CA 94102, USA",
    "mobile": "(555) 123-4567",
    "email": "john.doe@example.com",
    "homepage": "www.johndoe.com",
    "github": "johndoe",
    "linkedin": "johndoe",
    "quote": "Make it work, make it right, make it fast.",
    
    # ===== RESUME-SPECIFIC =====
    "summary": (
        "Experienced Software Engineer with 10+ years in cloud infrastructure "
        "and DevOps practices. Specialized in AWS, Kubernetes, and Infrastructure "
        "as Code. Passionate about automation, reliability, and scalable systems."
    ),
    
    # ===== EXPERIENCE (used in resume and cv) =====
    "experience": [
        {
            "title": "Senior DevOps Engineer",
            "organization": "Tech Corp Inc.",
            "location": "San Francisco, CA",
            "period": "Jan. 2020 - Present",
            "details": [  # Using 'details' instead of 'items' to avoid conflict with dict.items()
                "Led migration of legacy infrastructure to Kubernetes, reducing costs by 40%",
                "Implemented GitOps workflows with ArgoCD and Terraform",
                "Established comprehensive monitoring with Prometheus and Grafana",
            ],
        },
        {
            "title": "Software Engineer",
            "organization": "Startup Inc.",
            "location": "San Francisco, CA",
            "period": "Jun. 2015 - Dec. 2019",
            "details": [
                "Developed microservices architecture using Docker and Kubernetes",
                "Built CI/CD pipelines with Jenkins and GitHub Actions",
            ],
        },
    ],
    
    # ===== EDUCATION (used in resume and cv) =====
    "education": [
        {
            "degree": "B.S. in Computer Science",
            "institution": "University of California, Berkeley",
            "location": "Berkeley, CA",
            "period": "Sep. 2011 - May 2015",
            "details": [  # Using 'details' instead of 'items' to avoid conflict with dict.items()
                "GPA: 3.8/4.0",
                "Dean's List all semesters",
            ],
        },
    ],
    
    # ===== HONORS (used in resume and cv) =====
    "honor_subsections": [
        {
            "title": "Industry Awards",
            "honors": [
                {
                    "award": "Best DevOps Practice",
                    "event": "DevOps Summit 2023",
                    "location": "San Francisco, CA",
                    "date": "2023",
                },
            ],
        },
    ],
    
    # ===== CERTIFICATES (used in resume) =====
    "certificates": [
        {
            "title": "AWS Certified Solutions Architect - Professional",
            "organization": "Amazon Web Services",
            "location": "",
            "date": "2023",
        },
        {
            "title": "Certified Kubernetes Administrator (CKA)",
            "organization": "The Linux Foundation",
            "location": "",
            "date": "2022",
        },
    ],
    
    # ===== SKILLS (used in cv) =====
    "skills": [
        {
            "category": "Cloud & Infrastructure",
            "list": "AWS, GCP, Azure, Terraform, Ansible, Packer",  # 'list' instead of 'items'
        },
        {
            "category": "Container & Orchestration",
            "list": "Docker, Kubernetes, Helm, ArgoCD, Rancher",
        },
        {
            "category": "Programming",
            "list": "Python, Go, Bash, JavaScript, Node.js",
        },
    ],
    
    # ===== COVER LETTER SPECIFIC =====
    "recipient_name": "Engineering Team",
    "recipient_address": r"Tech Company Inc.\\100 Innovation Drive\\Silicon Valley, CA 94025",
    "letter_title": "Application for Senior DevOps Engineer Position",
    "letter_opening": "Dear Hiring Manager,",
    "letter_closing": "Sincerely,",
    "letter_enclosure": "[Attached]{Resume}",
    "header_alignment": "R",
    "letter_sections": [
        {
            "title": "About Me",
            "content": (
                "I am writing to express my strong interest in the Senior DevOps "
                "Engineer position at Tech Company Inc. With over 10 years of "
                "experience in software engineering and DevOps practices, I am "
                "confident that I can contribute significantly to your team."
            ),
        },
        {
            "title": "Why Your Company",
            "content": (
                "I am particularly impressed by your company's commitment to "
                "innovation and technical excellence. Your recent work on cloud-native "
                "architectures aligns perfectly with my expertise and passion."
            ),
        },
        {
            "title": "What I Bring",
            "content": (
                "Throughout my career, I have successfully led infrastructure "
                "migrations, implemented robust CI/CD pipelines, and established "
                "monitoring systems that improved system reliability. I am excited "
                "about the opportunity to bring these skills to your organization."
            ),
        },
    ],
}


def load_sample(
    doc_type: Literal["resume", "cv", "coverletter", "master"] = "resume"
) -> dict:
    """
    Load sample data for a specific document type.
    
    Args:
        doc_type: Type of document to load data for.
            - 'resume': Resume with summary, experience, education
            - 'cv': Academic CV with skills, publications
            - 'coverletter': Cover letter with recipient info
            - 'master': Complete data with all fields
    
    Returns:
        Dictionary with sample data for the specified document type.
        Returns a deep copy to avoid mutations of the original data.
    
    Raises:
        ValueError: If doc_type is not recognized
    
    Examples:
        >>> from awesomecv_jinja.samples import load_sample
        >>> 
        >>> # Load resume data
        >>> resume = load_sample("resume")
        >>> print(resume["first_name"])
        'John'
        >>> 
        >>> # Load and customize
        >>> cv = load_sample("cv")
        >>> cv["first_name"] = "Jane"
        >>> cv["skills"].append({"category": "Languages", "items": "English, French"})
        >>> 
        >>> # Get all data
        >>> all_data = load_sample("master")
    """
    if doc_type == "resume":
        return get_resume_data()
    elif doc_type == "cv":
        return get_cv_data()
    elif doc_type == "coverletter":
        return get_coverletter_data()
    elif doc_type == "master":
        return copy.deepcopy(MASTER_DATA)
    else:
        available = ["resume", "cv", "coverletter", "master"]
        raise ValueError(
            f"Unknown doc_type: '{doc_type}'. "
            f"Available: {', '.join(available)}"
        )


def get_resume_data() -> dict:
    """
    Get sample data for resume document type.
    
    Resume typically includes: summary, experience, education, skills (brief).
    
    Returns:
        Dictionary with resume data (deep copy)
    
    Examples:
        >>> from awesomecv_jinja.samples import get_resume_data
        >>> data = get_resume_data()
        >>> data["sections"]
        {'summary': True, 'experience': True, 'education': True, ...}
    """
    data = copy.deepcopy(MASTER_DATA)
    data["sections"] = {
        "summary": True,
        "experience": True,
        "education": True,
        "honors": True,
        "certificates": True,
    }
    # Remove cover letter specific fields
    data.pop("header_alignment", None)
    return data


def get_cv_data() -> dict:
    """
    Get sample data for CV (Curriculum Vitae) document type.
    
    CV typically includes: full experience, education, skills (detailed),
    publications, presentations.
    
    Returns:
        Dictionary with CV data (deep copy)
    
    Examples:
        >>> from awesomecv_jinja.samples import get_cv_data
        >>> data = get_cv_data()
        >>> len(data["skills"])
        3
    """
    data = copy.deepcopy(MASTER_DATA)
    data["sections"] = {
        "education": True,
        "skills": True,
        "experience": True,
        "honors": True,
    }
    # Remove cover letter specific fields
    data.pop("header_alignment", None)
    return data


def get_coverletter_data() -> dict:
    """
    Get sample data for cover letter document type.
    
    Cover letter uses personal info + letter-specific fields.
    
    Returns:
        Dictionary with cover letter data (deep copy)
    
    Examples:
        >>> from awesomecv_jinja.samples import get_coverletter_data
        >>> data = get_coverletter_data()
        >>> data["recipient_name"]
        'Engineering Team'
    """
    # Cover letter only needs specific fields
    data = copy.deepcopy(MASTER_DATA)
    
    # Keep only relevant fields for cover letter
    relevant_fields = [
        "first_name", "last_name", "position", "address",
        "mobile", "email", "homepage", "github", "linkedin",
        "recipient_name", "recipient_address",
        "letter_title", "letter_opening", "letter_closing",
        "letter_sections", "letter_enclosure", "header_alignment",
    ]
    
    return {k: v for k, v in data.items() if k in relevant_fields}


def get_master_data() -> dict:
    """
    Get complete master data with all fields.
    
    This is useful when you want to customize which fields
    go into which document type, or create custom combinations.
    
    Returns:
        Dictionary with all available sample data (deep copy)
    
    Examples:
        >>> from awesomecv_jinja.samples import get_master_data
        >>> master = get_master_data()
        >>> 
        >>> # Create custom resume with skills (normally in CV only)
        >>> custom_data = {
        ...     **master,
        ...     "sections": {
        ...         "summary": True,
        ...         "experience": True,
        ...         "skills": True,  # Not typical for resume
        ...     }
        ... }
    """
    return copy.deepcopy(MASTER_DATA)


# Convenience exports for backward compatibility and quick access
resume_data = get_resume_data()
cv_data = get_cv_data()
coverletter_data = get_coverletter_data()

