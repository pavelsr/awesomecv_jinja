# Prompt for converting Awesome-CV to Jinja2 templates

> ⚠️ **WIP (Work in Progress)** — This document is under active development and may be incomplete or subject to changes.

> **Note:** This prompt can be used to regenerate `*.tex.j2` files for the awesomecv template if tests fail after updating the awesomecv repository. The current list of supported variables is stored in `docs/awesomecv_tpl_vars.md`.

## Task
Convert all `.tex` files from `dev/upstream/awesome-cv/examples/` into Jinja2 templates (`.tex.j2`).
Replace hard-coded values with variables and loops.

## Custom Jinja2 delimiters
```
((( variable )))             # variables
((* block *))...((* end *))  # blocks (for, if)
((# comment #))              # comments
```

## Conversion rules

### 1. Personal information (in main files)
```latex
\name{Byungjin}{Park}               → \name{((( first_name )))}{((( last_name )))}
\position{Software Engineer}        → \position{((( position )))}
\address{235, World Cup...}         → \address{((( address )))}
\mobile{(+82) 10-9030-1843}        → \mobile{((( mobile )))}
\email{posquit0.bj@gmail.com}      → \email{((( email )))}
\homepage{www.posquit0.com}         → \homepage{((( homepage )))}
\github{posquit0}                   → \github{((( github )))}
\linkedin{posquit0}                 → \linkedin{((( linkedin )))}
\quote{``Be the change..."}         → ((* if quote *))\quote{``((( quote )))"}((* endif *))
```

### 2. Optional fields
If a field is commented out in the upstream file or may be missing in user data:
```latex
%\dateofbirth{January 1st, 1970}  → ((* if date_of_birth *))
                                     \dateofbirth{((( date_of_birth )))}
                                     ((* endif *))
```

### 3. Repeated blocks → `for` loops

**Experience (cventry):**
```latex
\cventry
  {DevOps Engineer} % Job title
  {Dunamu Inc.} % Organization
  {Seoul, S.Korea} % Location
  {Sep. 2023 - Present} % Date(s)
  {
    \begin{cvitems}
      \item {Task 1}
      \item {Task 2}
    \end{cvitems}
  }
```
→
```latex
((* for entry in experience *))
\cventry
  {((( entry.title )))} % Job title
  {((( entry.organization )))} % Organization
  {((( entry.location )))} % Location
  {((( entry.period )))} % Date(s)
  {
    ((* if entry.items *))
    \begin{cvitems}
      ((* for item in entry.items *))
      \item {((( item )))}
      ((* endfor *))
    \end{cvitems}
    ((* endif *))
  }
((* endfor *))
```

**Education (cventry):**
```latex
((* for entry in education *))
\cventry
  {((( entry.degree )))} % Degree
  {((( entry.institution )))} % Institution
  {((( entry.location )))} % Location
  {((( entry.period )))} % Date(s)
  {
    ((* if entry.items *))
    \begin{cvitems}
      ((* for item in entry.items *))
      \item {((( item )))}
      ((* endfor *))
    \end{cvitems}
    ((* endif *))
  }
((* endfor *))
```

**Honors (cvhonor):**
```latex
((* for honor in honors *))
\cvhonor
  {((( honor.award )))} % Award
  {((( honor.event )))} % Event
  {((( honor.location )))} % Location
  {((( honor.date )))} % Date(s)
((* endfor *))
```

**Skills (cvskill):**
```latex
((* for skill in skills *))
\cvskill
  {((( skill.category )))} % Category
  {((( skill.items )))} % Skills (comma-separated string)
((* endfor *))
```

### 4. Subsections
```latex
\cvsubsection{International Awards}
\begin{cvhonors}
  ...honors list...
\end{cvhonors}
```
→
```latex
((* for subsection in honor_subsections *))
\cvsubsection{((( subsection.title )))}
\begin{cvhonors}
  ((* for honor in subsection.honors *))
  \cvhonor{...}
  ((* endfor *))
\end{cvhonors}
((* endfor *))
```

### 5. Plain text (Summary, Cover Letter)
```latex
\begin{cvparagraph}
DevOps Engineer at fintech...
\end{cvparagraph}
```
→
```latex
\begin{cvparagraph}
((( summary )))
\end{cvparagraph}
```

### 6. Footer
```latex
\makecvfooter
  {\today}
  {Byungjin Park~~~·~~~Résumé}
  {\thepage}
```
→
```latex
\makecvfooter
  {((( footer_left | default("\\today") )))}
  {((( first_name ))) ((( last_name )))~~~·~~~((( document_title | default("Résumé") )))}
  {((( footer_right | default("\\thepage") )))}
```

### 7. Section includes (`input`)
```latex
\input{resume/summary.tex}
\input{resume/experience.tex}
```
→
```latex
((* if sections.summary *))
((* include "sections/summary.tex.j2" *))
((* endif *))
((* if sections.experience *))
((* include "sections/experience.tex.j2" *))
((* endif *))
```

## Output file structure

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

## 

**Notes:**
- `?` in TypeScript-style notation becomes `Required: -` in the table.
- `[]` means an array and must be included at every level: `items[]`, `experience[].items[]`.
- Examples are taken from the original files in `dev/upstream/awesome-cv/examples/`.

## Additional guidelines

1. **File headers**: Add this block at the top of each `.tex.j2`:
```latex
((# Auto-generated from Awesome-CV #))
((# License: CC BY-SA 4.0 #))
((# Source: https://github.com/posquit0/Awesome-CV #))
```

2. **Preserve comments**: keep LaTeX comments (`%`) as-is to document fields.

3. **Whitespace**: use `trim_blocks=True` and `lstrip_blocks=True`. Keep output formatting clean.

4. **Escaping**: do not escape values inside `(((  )))`. Do it via the `latex_escape` filter.

---

**This prompt is ready to convert all Awesome-CV files into Jinja2 templates with full variable documentation.**
