# tools

The scripts and instructions used to produce the files in this repository. The page files in
`../book-of-commandments-1833-pages/` are the source of truth; the combined text files are generated from them.
(Adapted from the tooling in the sibling `1828-phinney-cooperstown-bible` repo.)

## Pipeline

1. **Render the scan** (needs the scan PDF, which is not tracked in git, and `pypdfium2` + `pillow`; use the venv at `~/.venvs/lds-transcribe`, i.e. `~/.venvs/lds-transcribe/bin/python tools/render_pages.py ...`; recreate it with `python3 -m venv ~/.venvs/lds-transcribe && ~/.venvs/lds-transcribe/bin/pip install pypdfium2 pillow`. Keep it outside /tmp: a scratch venv broke after an idle spell in the sibling project):
   `python3 tools/render_pages.py public-rbc-2015gen25600-2015gen25600.pdf --out work [--pages 1-16,302] [--scale 4]`
   writes three overlapping enhanced-grayscale bands (top/mid/bottom, binding cropped off), plus a low-resolution colour overview; `--color` also keeps colour bands. The LOC scan has no text layer, so there is no OCR helper text.
2. **Transcribe**: AI agents (Claude) read the crops and write one `page-NNN.md` per page following
   [transcription-spec.md](transcription-spec.md). Pages may then be audited against the scan per
   [audit-spec.md](audit-spec.md). This step is done by agents, not by a script.
3. **Rebuild the combined files** from the page files (Python 3, standard library only; run from anywhere):
   ```
   python3 tools/compile_markdown.py     # -> book-of-commandments-1833.md
   python3 tools/make_plaintext.py       # -> book-of-commandments-1833.txt        (from book-of-commandments-1833.md)
   python3 tools/make_sparse.py          # -> book-of-commandments-1833-sparse.txt (from book-of-commandments-1833.md)
   ```
   Each script writes to the repo root by default; `--out` redirects the output. Run in that order.

## Notes on the scripts

- `compile_markdown.py` strips comments, running heads, footers and any marginal-notes section, and rejoins paragraphs
  that run across a page break. The join is driven by the `<!-- cont -->` marker the transcriber puts at the start of a
  continued paragraph (a verse can run across a page break, and punctuation heuristics are not reliable).
  It aborts if a `<!-- cont -->` has no paragraph to continue. A paragraph that starts with a bare number and a full stop (the verse printed `10.` on PDF 132, the title-page year `1833.`) would render as a Markdown list item, so the compiled `.md` writes it as `10\.`; `make_plaintext.py`, `make_sparse.py` and `make_typo_catalog.py` undo the escape.
- `make_sparse.py` keeps only the PDF page ranges in `PAGE_RANGES` (empty until the pilot settles them; the script refuses to run while empty).
- Differences from the 1830 tooling: this edition has numbered verses (one paragraph per verse). Differences from the Phinney tooling: single-column pages cut into three contrast-enhanced bands (the scan is a photo of a tiny book with faint ink), no reference letters, no Apocrypha logic.

## Typo catalog and structure check

- `make_typo_catalog.py` (standard library only) builds `../printer-typos.md` from a curated list of forms in the script, finding each in
  `../book-of-commandments-1833.md` with its PDF page, printed page (PDF - 3) and context; it also computes the table of chapters whose
  heading line has no verse number 1. Run it after the combined files are rebuilt: `python3 tools/make_typo_catalog.py`.
- `check_structure.py` is the mechanical check run after every batch (see its docstring).

## Not yet ported from the 1830 repo

`review/review_app.py` (human review of close calls) is copied/adapted if a human review is wanted. `proofread-spec.md` and `audit-spec.md` are the instructions for the audit and blind
proofread agents (adapted to 1833).
