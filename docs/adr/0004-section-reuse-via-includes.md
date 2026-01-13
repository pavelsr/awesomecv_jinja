# ADR-0004: Section Reuse via Jinja Includes

## Status

Accepted

## Date

2024-10-18

## Context

The same sections (education, experience, skills) are used in multiple document types (resume, cv). Without a reuse mechanism, we would duplicate code:

```
templates/awesome_cv/
├── resume.tex.j2          # Contains education section
├── cv.tex.j2              # Contains same education section (duplicated)
└── ...
```

This violates DRY (Don't Repeat Yourself) and makes maintenance difficult.

## Options Considered

### Option 1: Template Inheritance

Use Jinja2's `{% extends %}` mechanism.

**Pros:**

- Standard Jinja2 pattern
- Flexible override system

**Cons:**

- Requires complex base template design
- May be overkill for simple sections
- Harder to understand for LaTeX-focused users

### Option 2: Jinja Includes

Use `{% include %}` for reusable sections.

**Pros:**

- Simple and intuitive
- Each section is a standalone file
- Easy to add/remove sections
- Familiar pattern

**Cons:**

- Less flexible than inheritance
- No automatic block overrides

### Option 3: Macros

Define sections as Jinja2 macros.

**Pros:**

- Can accept parameters
- More control over rendering

**Cons:**

- More complex syntax
- Overkill for static sections

## Decision

Use Jinja includes for section reuse:

```jinja
((# resume.tex.j2 #))
\begin{document}
((* include "sections/education.tex.j2" *))
((* include "sections/experience.tex.j2" *))
\end{document}

((# cv.tex.j2 #))
\begin{document}
((* include "sections/education.tex.j2" *))  ((# same section #))
((* include "sections/publications.tex.j2" *))
\end{document}
```

## Consequences

### Positive

- Single source of truth for each section
- Easy to understand and modify
- Follows DRY principle
- Simple mental model

### Negative

- All sections share the same data context
- No parameterized sections (use macros if needed later)

## Structure

```
templates/awesome_cv/
├── resume.tex.j2
├── cv.tex.j2
├── coverletter.tex.j2
└── sections/
    ├── education.tex.j2
    ├── experience.tex.j2
    ├── skills.tex.j2
    ├── honors.tex.j2
    └── ...
```

## References

- [Jinja2 Include](https://jinja.palletsprojects.com/en/3.1.x/templates/#include)
- [DRY Principle](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)
