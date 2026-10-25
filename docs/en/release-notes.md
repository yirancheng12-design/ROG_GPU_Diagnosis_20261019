# Initial toolkit release notes — draft

[Home](../../README.md) · [Change log](../../CHANGELOG.md) · [Contribution rules](../../CONTRIBUTING.md)

**Status: unpublished.** This file does not create a Git tag or GitHub Release. Choose a version only after the candidate commit and checks have been reviewed.

## Proposed description

An evidence-led laptop GPU diagnosis toolkit, starting with a G635LX / RTX 5090 Laptop case. Inspect the 55W standby interval, separate the 175W/225W configuration claims, and reuse a read-only CSV analysis workflow.

## Included

- Short English case studies, detailed reports, and a Chinese quick-start entry.
- Standard-library-only CSV/ZIP analysis and a compact demo using the real evidence archive.
- Original-file and archive-member integrity verification, tests, and Windows/Linux CI.
- Blank measurement templates, a case-submission form, MIT license for original code/documentation, and source/evidence limitations.

No stable 225W workload result, automatic hardware tuning, or newly measured FPS increase is shipped.

## Quick start

Download or clone the full repository, then use Python 3.11+ from its root:

```console
python tools/demo.py
python tools/verify_repository.py
python -m unittest discover -s tests -v
```

The demo reads the included tuning ZIP and does not query the GPU. The full repository contains historical third-party evidence whose rights remain separate; it is not an executable tuning bundle.

## Maintainer checklist

- [ ] Confirm the candidate commit is on `main` and the Windows/Linux checks pass for that commit.
- [ ] Run the documented demo from a clean download; preserve any known limitations in the release description.
- [ ] Check the chart provenance and distinguish sample statistics from sustained-load or benchmark results.
- [ ] Review third-party rights and source descriptions before attaching any separate asset; do not package firmware or registry scripts as recommended tools.
- [ ] Choose an appropriate version/tag, then create a release with these edited notes. GitHub automatically supplies source archives for a tag; see [GitHub releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases).
- [ ] Update the change log with the actual date, version, and release link; do not prefill download or user counts.

Missing post-restart 225W evidence and the single-machine scope remain known limitations. A first release makes the existing material easier to obtain, not more conclusive.
