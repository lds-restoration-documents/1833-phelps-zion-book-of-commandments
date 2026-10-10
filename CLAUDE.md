# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this repo is

A text corpus, not software: AI-assisted transcription of the 1833 *A Book of Commandments, for the Government of the Church of Christ*
(W. W. Phelps & Co., Independence, Jackson County, Missouri), from the Library of Congress scan
https://www.loc.gov/item/08025600/ (`public-rbc-2015gen25600-2015gen25600.pdf`, 166 pages, one JPEG per page, **no text layer**; gitignored). The scan is a *photograph of a tiny book*: faint, uneven ink, stains, and
mirror-image show-through from the other side of the leaf; the last PDF page is a colour target. Expect many `[illegible]` marks, and never fill them from memory
(the Doctrine and Covenants text is memorized by every model; the 1833 print differs from it).
Methodology and tooling are adapted from the siblings `../1830-grandin-palmyra-book-of-mormon` (process; the more mature one) and
`../1828-phinney-cooperstown-bible` (numbered verses). Read their `transcription-notes.md` "gotchas" before changing the method.

There is **no OCR**: agents read contrast-enhanced page-image bands (`tools/render_pages.py`) and write one Markdown file per page; scripts in `tools/` only
rebuild the combined files. The plan is in `~/.claude/plans/this-is-a-new-silly-zebra.md`.

## Files

- `book-of-commandments-1833-pages/page-NNN.md`: **source of truth**, one file per PDF page, named by PDF page number (3 digits).
- Derived (never hand-edit; rebuild after any page edit): `book-of-commandments-1833.md`, `.txt`, `-sparse.txt`, `printer-typos.md` (`python3 tools/make_typo_catalog.py`, run after the three compile scripts).
- `transcription-notes.md`: method, judgment calls, audit table. `logs/`: local audit and proofread logs (gitignored, not part of the repo; kept so interrupted batches can resume).
- `work/`: gitignored scratch (renders).

Rebuild (standard library only): `python3 tools/compile_markdown.py && python3 tools/make_plaintext.py && python3 tools/make_sparse.py`.
Rendering needs `~/.venvs/lds-transcribe/bin/python` (pypdfium2 + pillow).

## Rules (from the siblings' hard-won lessons)

- **Write what the scan shows, never what you think it should say.** Printer's errors, odd spellings, wrong numbers and wrong running heads
  stay as printed. Do not correct from the Doctrine and Covenants, later editions, the Joseph Smith Papers or memory. A page that looks
  clean is not evidence of a clean transcription: silent normalization ("against" for "againt") was the main error in the siblings.
- Verses are one paragraph each, number first; verse numbers are copied as printed (errors kept, none added or fixed).
- Never complete faded, clipped or damaged text from memory; write the visible fragment (a letter is kept if about half or more is visible).
- Doubtful readings stay in place with `<!-- uncertain: ... -->`; unreadable text is `[illegible]`.
- The page image is authoritative. If the image cannot be read, stop and report that page; never guess from memory.
- Flush-left first line on a page = continuation: start the paragraph with `<!-- cont -->`.
- Comma vs period (owner's rule): more space + capital next word = period; less space + lowercase next word = comma; if they disagree use the shape.
- Specks are ignored; the thin space before `; : ? !` is not transcribed.
- Never run git commit/push: leave all changes in the working tree for the owner to review and commit.
- Batches of 16 pages; write each file right after reading its page; skip existing files so runs resume.
- Record the model that wrote each page range and which ranges were audited/proofread in `transcription-notes.md`. Never claim a check that was not done.
- Keep the first-line page comment in sync with the filename.
