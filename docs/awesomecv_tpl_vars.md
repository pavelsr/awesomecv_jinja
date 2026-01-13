## Original data structure:

```
dev/upstream/awesome-cv/
├── awesome-cv.cls
└── examples/
    ├── coverletter.tex
    ├── cv.tex
    ├── resume.tex
    ├── cv/
    │   ├── certificates.tex
    │   ├── committees.tex
    │   ├── education.tex
    │   ├── experience.tex
    │   ├── extracurricular.tex
    │   ├── honors.tex
    │   ├── presentation.tex
    │   ├── skills.tex
    │   └── writing.tex
    └── resume/
        ├── certificates.tex
        ├── committees.tex
        ├── education.tex
        ├── experience.tex
        ├── extracurricular.tex
        ├── honors.tex
        ├── presentation.tex
        ├── summary.tex
        └── writing.tex
```

**Bash command to list all .tex and .cls files:**
```bash
find dev/upstream/awesome-cv -type f \( -name "*.tex" -o -name "*.cls" \) | sort
```

**Alternative: using tree command (if available):**
```bash
tree -P '*.tex|*.cls' -I '__pycache__|*.pyc' dev/upstream/awesome-cv
```

> **Note:** These commands are useful for reviewing the structure of a new template that needs to be added to the project. Replace `awesome-cv` with the template name in `dev/upstream/<template-name>/` to explore other templates.


## Processed file structure

```
src/awesomecv_jinja/templates/awesome_cv/
├── awesome-cv.cls               (copied as-is)
├── resume.tex.j2                (main resume file)
├── cv.tex.j2                    (main CV file)
├── coverletter.tex.j2           (main cover letter file)
└── sections/
    ├── summary.tex.j2
    ├── experience.tex.j2
    ├── education.tex.j2
    ├── honors.tex.j2
    ├── certificates.tex.j2
    ├── skills.tex.j2
    ├── presentation.tex.j2
    ├── writing.tex.j2
    ├── committees.tex.j2
    └── extracurricular.tex.j2
```

## Short list of variables

### **resume.tex.j2**
```
first_name
last_name
position
address
mobile
email
homepage
github
linkedin
date_of_birth?
quote?
photo?
awesome_color?
header_alignment?
footer_left?
footer_right?
document_title?
sections:
  summary?
  experience?
  honors?
  certificates?
  presentation?
  writing?
  committees?
  education?
  extracurricular?
```

### **sections/summary.tex.j2**
```
summary
```

### **sections/experience.tex.j2**
```
experience[]:
  title
  organization
  location
  period
  items[]?
```

### **sections/education.tex.j2**
```
education[]:
  degree
  institution
  location
  period
  items[]?
```

### **sections/honors.tex.j2**
```
honor_subsections[]?:
  title
  honors[]:
    award
    event
    location
    date

# or a flat list:
honors[]:
  award
  event
  location
  date
```

### **sections/skills.tex.j2**
```
skills[]:
  category
  items  # comma-separated string
```

### **sections/certificates.tex.j2**
```
certificates[]:
  title
  organization
  location
  date
  description?
```

### **sections/presentation.tex.j2**
```
presentations[]:
  title
  event
  location
  date
```

### **sections/writing.tex.j2**
```
writings[]:
  title
  publication
  year
```

### **sections/committees.tex.j2**
```
committees[]:
  role
  organization
  location
  period
```

### **sections/extracurricular.tex.j2**
```
extracurricular[]:
  title
  organization
  location
  period
  items[]?
```

### **cv.tex.j2**
```
(same fields as resume.tex.j2, but with different sections)
sections:
  education?
  skills?
  experience?
  extracurricular?
  honors?
  certificates?
  presentation?
  writing?
  committees?
```

### **coverletter.tex.j2**
```
first_name
last_name
position
address
mobile
email
homepage
github
linkedin
quote?
photo?
awesome_color?
header_alignment?
recipient_name
recipient_address  # multi-line
letter_date?
letter_title
letter_opening
letter_closing
letter_enclosure?
letter_sections[]:
  title
  content
```

**Notes:**
- `?` in TypeScript-style notation means required
- `[]` means an array and must be included at every level: `items[]`, `experience[].items[]`.
- Examples are taken from the original files in `dev/upstream/awesome-cv/examples/`.


### resume.tex.j2
| Variable | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `first_name` | string | ✓ | First name | `Byungjin` |
| `last_name` | string | ✓ | Last name | `Park` |
| `position` | string | ✓ | Job position(s) | `Site Reliability Engineer{\enskip\cdotp\enskip}Software Architect` |
| `address` | string | ✓ | Full address | `235, World Cup buk-ro, Mapo-gu, Seoul, 03936, Republic of Korea` |
| `mobile` | string | ✓ | Phone number | `(+82) 10-9030-1843` |
| `email` | string | ✓ | Email address | `posquit0.bj@gmail.com` |
| `homepage` | string | - | Personal website | `www.posquit0.com` |
| `github` | string | - | GitHub username | `posquit0` |
| `linkedin` | string | - | LinkedIn username | `posquit0` |
| `quote` | string | - | Personal quote | `Be the change that you want to see in the world.` |
| `date_of_birth` | string | - | Date of birth | `January 1st, 1970` |
| `photo` | string | - | Photo path with options | `./examples/profile` |
| `awesome_color` | string | - | Color theme | `awesome-red` |
| `header_alignment` | string | - | Header alignment (C/L/R) | `C` |
| `footer_left` | string | - | Footer left text | `\today` |
| `footer_right` | string | - | Footer right text | `\thepage` |
| `document_title` | string | - | Document title in footer | `Résumé` |
| `sections` | object | ✓ | Sections to include | `{summary: true, experience: true, ...}` |

### sections/summary.tex.j2
| Variable | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `summary` | string | ✓ | Summary paragraph text | `DevOps Engineer at fintech & blockchain company Dunamu...` |

### sections/experience.tex.j2
| Variable | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `experience[]` | array | ✓ | List of work experiences | - |
| `experience[].title` | string | ✓ | Job title | `DevOps Engineer` |
| `experience[].organization` | string | ✓ | Company/organization name | `Dunamu Inc.` |
| `experience[].location` | string | ✓ | Work location | `Seoul, S.Korea` |
| `experience[].period` | string | ✓ | Time period | `Sep. 2023 - Present` |
| `experience[].items[]` | array | - | Bullet points describing responsibilities | `["Task 1", "Task 2"]` |

### sections/education.tex.j2
| Variable | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `education[]` | array | ✓ | List of educational entries | - |
| `education[].degree` | string | ✓ | Degree earned | `B.S. in Computer Science and Engineering` |
| `education[].institution` | string | ✓ | Institution name | `POSTECH(Pohang University of Science and Technology)` |
| `education[].location` | string | ✓ | Institution location | `Pohang, S.Korea` |
| `education[].period` | string | ✓ | Study period | `Mar. 2010 - Aug. 2017` |
| `education[].items[]` | array | - | Additional bullet points | `["Got a Chun Shin-Il Scholarship..."]` |

### sections/honors.tex.j2

**Option 1: With subsections**
| Variable | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `honor_subsections[]` | array | - | List of honor subsections | - |
| `honor_subsections[].title` | string | ✓ | Subsection title | `International Awards` |
| `honor_subsections[].honors[]` | array | ✓ | List of honors in subsection | - |
| `honor_subsections[].honors[].award` | string | ✓ | Award title | `2nd Place` |
| `honor_subsections[].honors[].event` | string | ✓ | Event/competition name | `AWS ASEAN AI/ML GameDay` |
| `honor_subsections[].honors[].location` | string | - | Event location (can be empty) | `Online` |
| `honor_subsections[].honors[].date` | string | ✓ | Year or date | `2021` |

**Option 2: Flat list**
| Variable | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `honors[]` | array | ✓ | List of all honors | - |
| `honors[].award` | string | ✓ | Award title | `Finalist` |
| `honors[].event` | string | ✓ | Event/competition name | `DEFCON 28th CTF Hacking Competition World Final` |
| `honors[].location` | string | - | Event location | `Las Vegas, U.S.A` |
| `honors[].date` | string | ✓ | Year or date | `2020` |

### sections/skills.tex.j2
| Variable | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `skills[]` | array | ✓ | List of skill categories | - |
| `skills[].category` | string | ✓ | Skill category name | `DevOps` |
| `skills[].items` | string | ✓ | Comma-separated skills | `AWS, Docker, Kubernetes, Rancher, Vagrant, Packer, Terraform` |

### sections/certificates.tex.j2
| Variable | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `certificates[]` | array | ✓ | List of certificates | - |
| `certificates[].title` | string | ✓ | Certificate name | `Certified Kubernetes Administrator` |
| `certificates[].organization` | string | ✓ | Issuing organization | `Cloud Native Computing Foundation` |
| `certificates[].location` | string | - | Location | `Online` |
| `certificates[].date` | string | ✓ | Issue date | `2021` |
| `certificates[].description` | string | - | Additional description | `Validation details...` |

### sections/presentation.tex.j2
| Variable | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `presentations[]` | array | ✓ | List of presentations | - |
| `presentations[].title` | string | ✓ | Presentation title | `Introduction to Terraform` |
| `presentations[].event` | string | ✓ | Event name | `HashiCorp User Group Meetup` |
| `presentations[].location` | string | - | Event location | `Seoul, S.Korea` |
| `presentations[].date` | string | ✓ | Presentation date | `Jan. 2020` |

### sections/writing.tex.j2
| Variable | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `writings[]` | array | ✓ | List of publications/writings | - |
| `writings[].title` | string | ✓ | Publication title | `Mastering Infrastructure as Code` |
| `writings[].publication` | string | ✓ | Publication venue | `Tech Blog` |
| `writings[].year` | string | ✓ | Publication year | `2022` |

### sections/committees.tex.j2
| Variable | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `committees[]` | array | ✓ | List of committee roles | - |
| `committees[].role` | string | ✓ | Committee role | `Program Committee Member` |
| `committees[].organization` | string | ✓ | Organization/event name | `DevOps Days Korea` |
| `committees[].location` | string | - | Location | `Seoul, S.Korea` |
| `committees[].period` | string | ✓ | Time period | `2021 - 2022` |

### sections/extracurricular.tex.j2
| Variable | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `extracurricular[]` | array | ✓ | List of extracurricular activities | - |
| `extracurricular[].title` | string | ✓ | Role/title in activity | `President` |
| `extracurricular[].organization` | string | ✓ | Organization name | `Computer Science Club` |
| `extracurricular[].location` | string | ✓ | Location | `POSTECH, S.Korea` |
| `extracurricular[].period` | string | ✓ | Time period | `2015 - 2016` |
| `extracurricular[].items[]` | array | - | Activity descriptions | `["Organized weekly coding sessions"]` |

### cv.tex.j2
Same base fields as `resume.tex.j2`, but with a different section order:
```
sections:
  education: true
  skills: true
  experience: true
  extracurricular: true
  honors: true
  certificates: true
  presentation: true
  writing: true
  committees: true
```

### coverletter.tex.j2
| Variable | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `first_name` | string | ✓ | First name | `Claud D.` |
| `last_name` | string | ✓ | Last name | `Park` |
| `position` | string | ✓ | Job position | `Site Reliability Engineer{\enskip\cdotp\enskip}Software Architect` |
| `address` | string | ✓ | Full address | `235, World Cup buk-ro, Mapo-gu, Seoul, 03936, Republic of Korea` |
| `mobile` | string | ✓ | Phone number | `(+82) 10-9030-1843` |
| `email` | string | ✓ | Email address | `posquit0.bj@gmail.com` |
| `homepage` | string | - | Personal website | `www.posquit0.com` |
| `github` | string | - | GitHub username | `posquit0` |
| `linkedin` | string | - | LinkedIn username | `posquit0` |
| `quote` | string | - | Personal quote | `Be the change that you want to see in the world.` |
| `photo` | string | - | Photo with options | `[circle,noedge,left]{./examples/profile}` |
| `recipient_name` | string | ✓ | Recipient name | `Company Recruitment Team` |
| `recipient_address` | string | ✓ | Recipient address (multi-line with \\) | `Google Inc.\\1600 Amphitheatre Parkway\\Mountain View, CA 94043` |
| `letter_date` | string | - | Letter date | `\today` |
| `letter_title` | string | ✓ | Letter title | `Job Application for Software Engineer` |
| `letter_opening` | string | ✓ | Opening greeting | `Dear Mr./Ms./Dr. LastName,` |
| `letter_closing` | string | ✓ | Closing | `Sincerely,` |
| `letter_enclosure` | string | - | Enclosure with optional text | `[Attached]{Curriculum Vitae}` |
| `letter_sections[]` | array | ✓ | Letter content sections | - |
| `letter_sections[].title` | string | ✓ | Section title | `About Me` |
| `letter_sections[].content` | string | ✓ | Section content (paragraph text) | `Lorem ipsum dolor sit amet...` |
| `header_alignment` | string | - | Header alignment (C/L/R) | `R` |
| `footer_left` | string | - | Footer left text | `\today` |
| `footer_center` | string | - | Footer center text | `Claud D. Park~~~·~~~Cover Letter` |
| `footer_right` | string | - | Footer right text | (empty) |
```

## Section Differences by Document Type

The following table shows which sections are available and in what order they appear in each document type:

| Section | Resume | CV | Cover Letter |
|---------|--------|----|--------------|
| `summary` | 1 (only) | — | — |
| `education` | 9 | 1 | — |
| `skills` | 2 | 2 | — |
| `experience` | 3 | 3 | — |
| `extracurricular` | 10 | 4 | — |
| `honors` | 4 | 5 | — |
| `certificates` | 5 | 6 | — |
| `presentation` | 6 | 7 | — |
| `writing` | 7 | 8 | — |
| `committees` | 8 | 9 | — |
| `letter_sections` | — | — | ✓ (only) |

**Notes:**
- Numbers indicate the order in which sections appear in the document (1 = first section)
- "—" means the section is not used in that document type
- Resume starts with `summary` (unique to resume) and ends with `education` and `extracurricular`
- CV starts with `education` and follows a different order optimized for academic/professional CVs
- Cover Letter uses only `letter_sections` (custom content sections) and does not use standard resume/CV sections

## Standard vs User-defined LaTeX Commands

Classification of LaTeX commands used in Awesome-CV template.

| Type | Command | Description |
|------|---------|-------------|
| **Standard** | `\documentclass` | Document class declaration |
| **Standard** | `\begin`, `\end` | Environment delimiters |
| **Standard** | `\input` | File inclusion |
| **Standard** | `\item` | List item |
| **Standard** | `\today`, `\thepage` | Date and page number |
| **Standard** | `\geometry` | Page margins (geometry pkg) |
| **Standard** | `\colorlet`, `\definecolor` | Colors (xcolor pkg) |
| **Standard** | `\setbool` | Boolean variables (etoolbox) |
| **Standard** | `\renewcommand` | Command redefinition |
| **Standard** | `\href` | Hyperlinks (hyperref pkg) |
| **Standard** | `\quad`, `\textbar`, `\enskip`, `\cdotp` | Standard spacing/symbols |
| **User-defined** | `\name` | First and last name |
| **User-defined** | `\position` | Job position |
| **User-defined** | `\address` | Address |
| **User-defined** | `\mobile` | Phone number |
| **User-defined** | `\email` | Email address |
| **User-defined** | `\homepage` | Website |
| **User-defined** | `\github`, `\linkedin`, `\gitlab`, ... | Social networks |
| **User-defined** | `\photo` | Photo |
| **User-defined** | `\quote` | Quote |
| **User-defined** | `\makecvheader` | Generate CV header |
| **User-defined** | `\makecvfooter` | Generate CV footer |
| **User-defined** | `\cvsection` | Resume section |
| **User-defined** | `\cvsubsection` | Subsection |
| **User-defined** | `\cventry` | Entry (experience/education) |
| **User-defined** | `\cvhonor` | Honor/award entry |
| **User-defined** | `\cvskill` | Skill entry |
| **User-defined** | `cventries` (env) | Entries environment |
| **User-defined** | `cvhonors` (env) | Honors environment |
| **User-defined** | `cvskills` (env) | Skills environment |
| **User-defined** | `cvitems` (env) | Bullet points environment |
| **User-defined** | `cvletter` (env) | Cover letter environment |
| **User-defined** | `cvparagraph` (env) | Paragraph environment |
| **User-defined** | `\recipient` | Letter recipient |
| **User-defined** | `\lettertitle` | Letter title |
| **User-defined** | `\letterdate` | Letter date |
| **User-defined** | `\letteropening` | Letter greeting |
| **User-defined** | `\letterclosing` | Letter closing |
| **User-defined** | `\letterenclosure` | Letter enclosure |
| **User-defined** | `\lettersection` | Letter section |
| **User-defined** | `\makelettertitle` | Generate letter title |
| **User-defined** | `\makeletterclosing` | Generate letter closing |

### Full List of User-defined Commands

**Personal information:**
`\photo`, `\name`, `\firstname`, `\lastname`, `\familyname`, `\address`, `\position`, `\mobile`, `\email`, `\dateofbirth`, `\homepage`, `\github`, `\gitlab`, `\bitbucket`, `\stackoverflow`, `\linkedin`, `\orcid`, `\twitter`, `\x`, `\mastodon`, `\researchgate`, `\skype`, `\reddit`, `\xing`, `\medium`, `\kaggle`, `\hackerrank`, `\telegram`, `\googlescholar`, `\extrainfo`, `\quote`

**CV structure:**
`\makecvheader`, `\makecvfooter`, `\cvsection`, `\cvsubsection`, `\cventry`, `\cvsubentry`, `\cvhonor`, `\cvskill`

**Environments:**
`cventries`, `cvsubentries`, `cvhonors`, `cvskills`, `cvitems`, `cvparagraph`, `cvletter`

**Cover letter:**
`\recipient`, `\recipientname`, `\recipientaddress`, `\lettertitle`, `\letterdate`, `\letteropening`, `\letterclosing`, `\letterenclname`, `\letterenclosure`, `\lettersection`, `\makelettertitle`, `\makeletterclosing`

**Configuration:**
`\fontdir`, `\acvHeaderNameDelim`, `\acvHeaderAfterNameSkip`, `\acvHeaderAfterPositionSkip`, `\acvHeaderAfterAddressSkip`, `\acvHeaderIconSep`, `\acvHeaderSocialSep`, `\acvHeaderAfterSocialSkip`, `\acvHeaderAfterQuoteSkip`, `\acvSectionTopSkip`, `\acvSectionContentTopSkip`

---

### One-shot Prompt to Generate This Table

```
Analyze the LaTeX class file `awesome-cv.cls` and example `.tex` files from the Awesome-CV template.

Classify all LaTeX commands into two categories:
1. **Standard** — commands from LaTeX kernel, base classes, or common packages (geometry, xcolor, hyperref, etoolbox, fontawesome, etc.)
2. **User-defined** — commands defined in `awesome-cv.cls` using `\newcommand`, `\renewcommand`, `\newenvironment`

Output:
1. A markdown table with columns: Type | Command | Description
2. A comma-separated list of all user-defined commands grouped by purpose:
   - Personal information commands
   - CV structure commands
   - Environments
   - Cover letter commands
   - Configuration commands

Files to analyze:
- awesome-cv.cls (main class file with command definitions)
- examples/resume.tex, cv.tex, coverletter.tex (usage examples)
- examples/resume/*.tex, examples/cv/*.tex (section files)
```
