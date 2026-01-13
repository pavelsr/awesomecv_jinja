# One-Shot Prompt: Convert LaTeX Template to Jinja2

**Target:** Claude Opus 4.5 in Cursor Agent Mode

---

## Mode Check

> **IMPORTANT:** This prompt requires **Agent Mode** with full tool access.
>
> If you are in **Ask Mode** — STOP immediately and respond:
> "This task requires Agent Mode to clone repositories, create files, and run validation scripts. Please switch to Agent Mode and rerun this prompt."

---

## Input: Template Repository URL

**Repository to convert:**

```
https://github.com/moderncv/moderncv
```

*(Replace with desired template repository)*

---

## Task Overview

Convert a LaTeX CV/resume template repository into Jinja2 templates compatible with the `awesomecv_jinja` Python module.

**Steps:**
1. Clone repository to `dev/upstream/<template_name>/`
2. Analyze template structure (.tex, .cls, .sty files)
3. Convert to `.tex.j2` files with awesomecv_jinja variable schema
4. Place output in `src/awesomecv_jinja/templates/<template_name>/`
5. Validate with `uv run python dev/scripts/check_templates.py`

---

## Jinja2 Configuration

All templates MUST use these custom delimiters (LaTeX-compatible):

```python
Environment(
    block_start_string='((*',
    block_end_string='*))',
    variable_start_string='(((',
    variable_end_string=')))',
    comment_start_string='((#',
    comment_end_string='#))',
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=True,
    autoescape=False
)
```

**Example syntax:**
```latex
((( first_name | latex_escape )))     ((# variable #))
((* if photo *))                       ((# block start #))
\photo{((( photo )))}
((* endif *))                          ((# block end #))
((* for item in skills *))             ((# loop #))
\cvskill{((( item.category )))}{((( item.list )))}
((* endfor *))
```

---

## Canonical Variable Schema (awesomecv_jinja)

**CRITICAL:** Use ONLY these variable names. Map template-specific names to this schema.

### Personal Information (all document types)

**Only 3 variables are required. All others are optional and must be wrapped in conditionals.**

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `first_name` | string | ✓ | First name |
| `last_name` | string | ✓ | Last name |
| `email` | string | ✓ | Email address |
| `position` | string | - | Job title / position |
| `address` | string | - | Full address |
| `mobile` | string | - | Phone number |
| `homepage` | string | - | Personal website |
| `github` | string | - | GitHub username |
| `linkedin` | string | - | LinkedIn username |
| `gitlab` | string | - | GitLab username |
| `stackoverflow` | string | - | StackOverflow ID |
| `twitter` | string | - | Twitter/X username |
| `skype` | string | - | Skype username |
| `reddit` | string | - | Reddit username |
| `medium` | string | - | Medium username |
| `kaggle` | string | - | Kaggle username |
| `hackerrank` | string | - | HackerRank username |
| `telegram` | string | - | Telegram username |
| `googlescholar` | string | - | Google Scholar ID |
| `extrainfo` | string | - | Additional info |
| `quote` | string | - | Personal quote / tagline |
| `date_of_birth` | string | - | Date of birth |
| `photo` | string | - | Photo path with options |

### Document Configuration

| Variable | Type | Description |
|----------|------|-------------|
| `awesome_color` | string | Color theme name |
| `header_alignment` | string | Header alignment (C/L/R) |
| `footer_left` | string | Footer left text |
| `footer_center` | string | Footer center text |
| `footer_right` | string | Footer right text |
| `document_title` | string | Document title in footer |
| `sections` | object | Which sections to include |

### Section: experience[]

```yaml
experience:
  - title: "DevOps Engineer"           # Job title
    organization: "Company Inc."       # Company name
    location: "San Francisco, CA"      # Location
    period: "Jan 2020 - Present"       # Time period
    details:                           # Optional bullet points
      - "Task 1"
      - "Task 2"
```

### Section: education[]

```yaml
education:
  - degree: "B.S. in Computer Science"
    institution: "University Name"
    location: "City, State"
    period: "Sep 2015 - May 2019"
    details:                           # Optional
      - "GPA: 3.8/4.0"
```

### Section: skills[]

```yaml
skills:
  - category: "Programming"
    list: "Python, Go, JavaScript"     # Comma-separated string
```

### Section: honors[] or honor_subsections[]

**Flat list:**
```yaml
honors:
  - award: "Best Paper Award"
    event: "Conference 2023"
    location: "New York"
    date: "2023"
```

**With subsections:**
```yaml
honor_subsections:
  - title: "International Awards"
    honors:
      - award: "1st Place"
        event: "Competition"
        location: ""
        date: "2023"
```

### Section: certificates[]

```yaml
certificates:
  - title: "AWS Solutions Architect"
    organization: "Amazon Web Services"
    location: ""                       # Optional
    date: "2023"
    description: ""                    # Optional
```

### Section: presentations[]

```yaml
presentations:
  - title: "Talk Title"
    event: "Conference Name"
    location: "City"
    date: "Mar 2023"
```

### Section: writings[]

```yaml
writings:
  - title: "Article Title"
    publication: "Journal/Blog Name"
    year: "2023"
```

### Section: committees[]

```yaml
committees:
  - role: "Program Committee Member"
    organization: "Conference Name"
    location: "Online"
    period: "2022 - 2023"
```

### Section: extracurricular[]

```yaml
extracurricular:
  - title: "President"
    organization: "Student Club"
    location: "University"
    period: "2018 - 2019"
    details:
      - "Activity description"
```

### Section: summary

```yaml
summary: "Experienced engineer with 10+ years..."  # Plain text
```

### Cover Letter Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `recipient_name` | string | ✓ | Recipient name |
| `recipient_address` | string | ✓ | Multi-line with `\\` |
| `letter_date` | string | - | Letter date |
| `letter_title` | string | ✓ | Letter title |
| `letter_opening` | string | ✓ | Opening greeting |
| `letter_closing` | string | ✓ | Closing |
| `letter_enclosure` | string | - | Enclosure |
| `letter_sections[]` | array | ✓ | `{title, content}` |

---

## Variable Mapping Rules

### 1. Map Template Variables to Canonical Names

When the source template uses different variable names, map them to the canonical schema:

| Source Template Variable | → | Canonical Variable |
|--------------------------|---|---------------------|
| `cell_phone`, `phone`, `telephone` | → | `mobile` |
| `firstname`, `givenname` | → | `first_name` |
| `lastname`, `surname`, `familyname` | → | `last_name` |
| `jobtitle`, `title` (personal) | → | `position` |
| `company`, `employer` | → | `organization` |
| `degree`, `qualification` | → | `degree` |
| `school`, `university` | → | `institution` |
| `date`, `dates`, `duration` | → | `period` |
| `city`, `place` | → | `location` |
| `responsibilities`, `tasks`, `bullets` | → | `details` |
| `skills_list`, `skill_items` | → | `list` |

### 2. Check GitHub Issues for Semantic Clarity

Before mapping ambiguous variables, check the template's GitHub issues for usage examples:

```bash
# Use gh CLI or MCP GitHub tools to search issues
gh search issues --repo <owner>/<repo> "variable_name"
```

### 3. Document All Mappings

At the TOP of each `.tex.j2` file, add a comment block listing:
- All variables the file supports
- Any non-obvious mappings

Example:

```latex
((# ============================================================ #))
((# Template: moderncv/resume.tex.j2                             #))
((# Source: https://github.com/moderncv/moderncv                 #))
((#                                                              #))
((# Supported variables:                                         #))
((#   first_name, last_name, position, address, mobile, email    #))
((#   homepage?, github?, linkedin?, photo?, quote?              #))
((#   sections: {experience, education, skills, ...}             #))
((#                                                              #))
((# Variable mappings from original template:                    #))
((#   \firstname → first_name                                    #))
((#   \familyname → last_name                                    #))
((#   \phone[mobile] → mobile                                    #))
((# ============================================================ #))
```

---

## Conversion Rules

### Rule 1: Required vs Optional Variables

**ONLY THREE variables are required:**
- `first_name`
- `last_name`
- `email`

**ALL other variables are optional** and MUST be wrapped in existence checks:

```latex
((# REQUIRED - output directly #))
\name{((( first_name | latex_escape )))}{((( last_name | latex_escape )))}
\email{((( email | latex_escape )))}

((# OPTIONAL - wrap in conditional #))
((* if position *))
\position{((( position | latex_escape )))}
((* endif *))

((* if address *))
\address{((( address | latex_escape )))}
((* endif *))

((* if mobile *))
\mobile{((( mobile | latex_escape )))}
((* endif *))

((* if homepage *))
\homepage{((( homepage | latex_escape )))}
((* endif *))
```

### Rule 2: Wrap All Optional Variables in Conditionals

Every variable except `first_name`, `last_name`, and `email` MUST be checked:

```latex
((* if date_of_birth *))
\dateofbirth{((( date_of_birth | latex_escape )))}
((* endif *))

((* if photo *))
\photo{((( photo )))}
((* endif *))

((* if quote *))
\quote{``((( quote | latex_escape )))"}
((* endif *))
```

### Rule 3: Always Use latex_escape Filter

Escape user input to prevent LaTeX errors:

```latex
\name{((( first_name | latex_escape )))}{((( last_name | latex_escape )))}
\email{((( email | latex_escape )))}
```

**Exception:** Do NOT escape values that contain intentional LaTeX commands (like `position` with `\enskip`).

### Rule 4: Convert Repeated Entries to Loops

**Before (hardcoded):**
```latex
\cventry{2020--Present}{Engineer}{Company A}{City}{}{}
\cventry{2018--2020}{Developer}{Company B}{City}{}{}
```

**After (dynamic):**
```latex
((* for entry in experience *))
\cventry
  {((( entry.period | latex_escape )))}
  {((( entry.title | latex_escape )))}
  {((( entry.organization | latex_escape )))}
  {((( entry.location | latex_escape )))}
  {}
  {((* if entry.details *))
    \begin{itemize}
      ((* for item in entry.details *))
      \item ((( item | latex_escape )))
      ((* endfor *))
    \end{itemize}
  ((* endif *))}
((* endfor *))
```

### Rule 5: Convert \input to Jinja Includes

```latex
% Original
\input{sections/experience.tex}

% Converted
((* if sections.experience *))
((* include "sections/experience.tex.j2" *))
((* endif *))
```

### Rule 6: Handle Whitespace with - Modifier

Use `-` to control whitespace in output:

```latex
((* for entry in experience -*))
\cventry{...}
((*- endfor *))
```

### Rule 7: Use default Filter for Fallbacks

```latex
\makecvfooter
  {((( footer_left | default("\\today") )))}
  {((( first_name ))) ((( last_name )))}
  {((( footer_right | default("\\thepage") )))}
```

---

## File Handling Rules

### .cls Files (Class Files)

- Copy to output directory **unchanged**
- Do NOT convert to Jinja2

### .sty Files (Style Files)

1. **Analyze** the .sty file for variable definitions or overrides
2. **If NO variables found:** Copy to output directory unchanged
3. **If variables found:** Inline the relevant parts into the main .tex.j2 file

### Section Files

Create separate `.tex.j2` files in `sections/` subdirectory:

```
src/awesomecv_jinja/templates/<template_name>/
├── <template>.cls           # Copied unchanged
├── resume.tex.j2            # Main document
├── cv.tex.j2                # Main document (if exists)
├── coverletter.tex.j2       # Main document (if exists)
└── sections/
    ├── experience.tex.j2
    ├── education.tex.j2
    ├── skills.tex.j2
    └── ...
```

---

## Execution Steps

### Step 1: Clone Repository

```bash
# Extract template name from URL
REPO_URL="https://github.com/moderncv/moderncv"
TEMPLATE_NAME=$(basename "$REPO_URL")

# Clone to dev/upstream/
git clone "$REPO_URL" "dev/upstream/$TEMPLATE_NAME"
```

### Step 2: Analyze Structure

List all .tex, .cls, and .sty files:

```bash
find dev/upstream/<template_name> -type f \( -name "*.tex" -o -name "*.cls" -o -name "*.sty" \) | sort
```

Identify:
- Main document files (resume.tex, cv.tex, etc.)
- Section/include files
- Class and style files
- Example/sample files

### Step 3: Identify Variables

For each .tex file, find:
1. Personal info commands (`\name`, `\address`, `\phone`, etc.)
2. Repeated entries (`\cventry`, `\cvitem`, etc.)
3. Section structures
4. Customization options

### Step 4: Create Variable Mapping Table

If template uses non-standard variable names, create a mapping table:

```markdown
## Variable Mapping: <template_name> → awesomecv_jinja

| Original Command | Original Variable | → | Canonical Variable | Notes |
|------------------|-------------------|---|---------------------|-------|
| `\firstname{}` | firstname | → | first_name | Direct mapping |
| `\phone[mobile]{}` | phone | → | mobile | Type modifier ignored |
| `\social[github]{}` | github | → | github | Extracted from social |

**⚠️ Warnings:**
- `\extrainfo{}` has no direct equivalent; mapped to `extrainfo`
- `\photo[64pt]{}` size parameter ignored; use `photo` variable
```

### Step 5: Convert Templates

For each identified file:
1. Create corresponding `.tex.j2` file
2. Add header comment with variable documentation
3. Replace hardcoded values with Jinja2 variables
4. Wrap optional fields in conditionals
5. Convert repeated entries to loops
6. Apply `latex_escape` filter to user input

### Step 6: Validate Templates

```bash
uv run python dev/scripts/check_templates.py
```

All templates MUST pass syntax validation.

### Step 7: Report Variable Mappings

Output a summary table of all variable mappings made:

```markdown
## Conversion Summary: <template_name>

### Files Created
- `src/awesomecv_jinja/templates/<template_name>/resume.tex.j2`
- `src/awesomecv_jinja/templates/<template_name>/sections/experience.tex.j2`
- ...

### Variable Mappings Applied

| File | Original | Mapped To | Reason |
|------|----------|-----------|--------|
| resume.tex.j2 | `\phone[mobile]` | `mobile` | Standard phone variable |
| resume.tex.j2 | `\firstname` | `first_name` | Name standardization |
| experience.tex.j2 | `\cventry{dates}` | `entry.period` | Date field normalization |

### ⚠️ Potential Issues
- `\photo` in source accepts size parameter; awesomecv uses path only
- `\quote` placement differs from Awesome-CV
```

---

## Complete Conversion Example

### Source: moderncv \cventry

```latex
\cventry{2020--Present}{Software Engineer}{Tech Corp}{San Francisco}{}{
  \begin{itemize}
    \item Developed microservices
    \item Led team of 5 engineers
  \end{itemize}
}
```

### Converted: experience.tex.j2

```latex
((# ============================================================ #))
((# Template: moderncv/sections/experience.tex.j2                #))
((# Source: https://github.com/moderncv/moderncv                 #))
((#                                                              #))
((# Supported variables:                                         #))
((#   experience[]:                                              #))
((#     - title (string): Job title                              #))
((#     - organization (string): Company name                    #))
((#     - location (string): City, Country                       #))
((#     - period (string): Date range                            #))
((#     - details[]? (array): Bullet points                      #))
((#                                                              #))
((# Variable mappings:                                           #))
((#   moderncv arg1 (dates) → period                             #))
((#   moderncv arg2 (title) → title                              #))
((#   moderncv arg3 (employer) → organization                    #))
((#   moderncv arg4 (city) → location                            #))
((#   moderncv arg5 (grade) → (not used)                         #))
((#   moderncv arg6 (description) → details[]                    #))
((# ============================================================ #))

\section{Experience}

((* for entry in experience *))
\cventry
  {((( entry.period | latex_escape )))}
  {((( entry.title | latex_escape )))}
  {((( entry.organization | latex_escape )))}
  {((( entry.location | latex_escape )))}
  {}
  {((* if entry.details -*))
\begin{itemize}
    ((* for item in entry.details -*))
\item ((( item | latex_escape )))
    ((* endfor -*))
\end{itemize}
  ((*- endif *))}
((* endfor *))
```

---

## Checklist Before Completion

- [ ] Repository cloned to `dev/upstream/<template_name>/`
- [ ] All .cls files copied unchanged to output
- [ ] All main document files converted to .tex.j2
- [ ] All section files converted to .tex.j2 in `sections/`
- [ ] Each .tex.j2 has header comment with variable documentation
- [ ] Only `first_name`, `last_name`, `email` are used without conditionals
- [ ] ALL other variables wrapped in `((* if var *))...((* endif *))`
- [ ] All user input uses `| latex_escape` filter
- [ ] Repeated entries converted to `((* for *))` loops
- [ ] `\input` commands converted to `((* include *))` with conditionals
- [ ] Variable mapping table documented in conversion summary
- [ ] `uv run python dev/scripts/check_templates.py` passes
- [ ] No .tex files committed (only .tex.j2)

---

## Output Location

```
src/awesomecv_jinja/templates/<template_name>/
├── <template>.cls              # Class file (unchanged)
├── *.sty                       # Style files (if no variables)
├── resume.tex.j2               # Main resume template
├── cv.tex.j2                   # Main CV template (if applicable)
├── coverletter.tex.j2          # Cover letter template (if applicable)
└── sections/
    ├── experience.tex.j2
    ├── education.tex.j2
    ├── skills.tex.j2
    ├── honors.tex.j2
    ├── certificates.tex.j2
    ├── presentations.tex.j2
    ├── writings.tex.j2
    ├── committees.tex.j2
    ├── extracurricular.tex.j2
    └── summary.tex.j2
```

---

## Begin Conversion

Now execute the conversion for the repository specified at the top of this prompt.

1. Clone the repository
2. Analyze the structure
3. Create the variable mapping
4. Convert all templates
5. Validate with check_templates.py
6. Report the conversion summary with any warnings
