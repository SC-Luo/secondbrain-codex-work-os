# Selection rubric and DESIGN.md contract

Use this reference only when selecting a new design language or materially redesigning a web UI.

## Candidate scoring

Score each candidate from 0 to 5 on every criterion, then apply the listed weight.

| Criterion | Weight | Evaluate |
|---|---:|---|
| Product and information architecture | 30% | Fit for marketing site, commerce, editorial, documentation, dashboard, workflow app, or portal |
| Brand and audience | 25% | Trust level, emotional tone, industry expectations, and user sophistication |
| Content and media density | 15% | Text density, imagery, data visualization, catalogs, and long-form reading |
| Interaction model | 15% | Navigation depth, forms, tables, search, task flows, and motion |
| Responsive usability and accessibility | 15% | Mobile behavior, touch targets, contrast, legibility, focus states, and reduced motion |

Reject a candidate rather than merely lowering its score when its defining structure conflicts with the product, depends on unavailable assets, or would make accessibility materially worse.

## Selection sequence

1. Use the library README summaries to shortlist five plausible styles.
2. Inspect only the relevant portions of each shortlisted `design-md/<slug>/DESIGN.md`.
3. Rank all five and present the best three. Resolve close scores in favor of accessibility, maintainability, and content fit.

Use this concise presentation:

| Rank | Style | Why it fits | What will be adapted | Main risk |
|---:|---|---|---|---|
| 1 | `<style>` | `<reason>` | `<brand changes>` | `<risk>` |
| 2 | `<style>` | `<reason>` | `<brand changes>` | `<risk>` |
| 3 | `<style>` | `<reason>` | `<brand changes>` | `<risk>` |

End with one recommended option and wait for the user's choice unless they already delegated the decision.

## Project DESIGN.md metadata

Every newly created project design contract must begin with:

```yaml
---
design_source_repository: voltagent/awesome-design-md
design_source_style: <directory-slug>
design_source_commit: <full-git-commit>
adaptation_mode: brand-adapted
---
```

Do not invent the commit. Read it from the local mirror with `git rev-parse HEAD`.

## Required design contract

The adapted `DESIGN.md` must be implementation-ready and cover:

- Visual direction and the intended emotional tone.
- Semantic color tokens, including foreground/background pairings and interaction states.
- Typography using fonts the project may legally and technically load, plus fallbacks.
- Spacing, sizing, radius, border, shadow, and elevation rules where relevant.
- Page grid, section rhythm, content width, and responsive behavior.
- Core components and hover, focus, active, disabled, loading, empty, and error states as applicable.
- Accessibility constraints, including contrast, keyboard focus, touch targets, and reduced motion.
- Explicit do/don't rules and a short list of deliberate deviations from the source style.

## Brand-safety boundary

- Do not copy source logos, wordmarks, trademark shapes, product screenshots, branded illustration systems, or marketing copy.
- Do not assume a proprietary font is licensed. Replace it with an available licensed or system alternative while preserving the intended typographic character.
- Do not reproduce a source brand so literally that users could mistake the project for that company.
- Attribution metadata records design-system provenance; it does not transfer trademark or asset rights.
- User-provided brand rules and the existing project contract override this reference.
