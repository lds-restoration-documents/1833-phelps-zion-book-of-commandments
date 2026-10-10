# 1833 Phelps Zion Book of Commandments
[Markdown](#what-is-markdown) & Plain Text extractions of the content of *A Book of Commandments, for the Government of the Church of Christ*, the 1833 compilation of Joseph Smith's revelations printed by W. W. Phelps & Co. at Zion (Independence), Jackson County, Missouri. Extracted using AI.

## Background
The Book of Commandments was the first attempt to publish Joseph Smith's revelations as a book. Printing began in Independence in 1833 and was cut short that July when the press was destroyed, so the work was never completed and only a small number of copies were bound from the surviving sheets. The text in the scan breaks off in the middle of Chapter LXV, at verse 47 on printed page 160.
* Wikipedia: [Book of Commandments](https://en.wikipedia.org/wiki/Book_of_Commandments)
* Library of Congress: [A Book of Commandments (item 08025600)](https://www.loc.gov/item/08025600/)

## Files
* [book-of-commandments-1833.md](book-of-commandments-1833.md): the whole text in a single [Markdown](#what-is-markdown) file (about 43,000 words): the title page, the title-page verso, and Chapters I to LXV. A `<!-- page NNN -->` comment marks where each PDF page begins.
* [book-of-commandments-1833.txt](book-of-commandments-1833.txt): the same text as plain text, with no [Markdown](#what-is-markdown).
* [book-of-commandments-1833-sparse.txt](book-of-commandments-1833-sparse.txt): plain text of the work only: the title page (PDF page 4) followed by the chapters (PDF pages 6–163, from Chapter I to the break in Chapter LXV). It leaves out the imprint lines at the foot of the title page (place, publisher and year), the title-page verso, and the covers and endpapers.
* [book-of-commandments-1833-pages/](book-of-commandments-1833-pages/): one [Markdown](#what-is-markdown) file per page of the scan (`page-001.md` to `page-166.md`), with running heads, chapter headings, verses and signature marks. File numbers are PDF page numbers (printed page number = PDF page − 3 in the text). These are the source of truth; the three files above are generated from them.
* [printer-typos.md](printer-typos.md): a catalog of the likely printer's slips in the text (37 occurrences, each with its page and context), the irregular verse numbers and chapter headings, and the chapters whose heading has no verse number. It leaves out spellings that were normal or intentional for the period, such as "recompence", "strait" and "sheweth".
* [transcription-notes.md](transcription-notes.md): how the text was produced, the conventions used, what the audits found, and the readings that remain doubtful.

## What is in the 1833 edition
The 1833 printing is a small book with a layout of its own, and the transcription keeps it:
* The text is divided into **65 chapters**, numbered in Roman numerals, with **numbered verses**. There is no separate preface or index: Chapter I is itself headed "A Preface or instruction unto the Book of Commandments".
* Most chapters open with an italic line naming the revelation, its recipient, place and date (for example "A Revelation to Emma, given in Harmony, Pennsylvania, July, 1830."), followed by a paragraph that opens with a large drop capital and has no verse number. In Chapters I to XXX the italic line carries the verse number "1"; from Chapter XXXI on no "1" is printed.
* The text is set in a single column, with the page number at the top and a signature mark (A, B, C, D, E and a number) at the foot of some pages. The type puts a thin space before `;`, `:`, `?` and `!`, which is not reproduced.
* Spelling, capitalization, punctuation and grammar are kept exactly as printed, **printer's errors included**; nothing has been corrected from the Doctrine and Covenants, later editions or the manuscripts.
* The printing stops partway through Chapter LXV, so the last page of text (printed page 160) ends at verse 47.

## Source
Extracted from the [PDF scan](https://www.loc.gov/item/08025600/) of the physical book at the Library of Congress. The scan has 166 pages and is a photograph of a very small book, with its cloth binding and page edges visible: the ink is faint and uneven, many pages are stained, and the text of the other side of the leaf often shows through. The pages are the spine strip, front cover and front endpaper (PDF pages 1–3), the title page and its verso (4–5), the text (6–163, printed pages 3–160), the rear endpaper and back cover (164–165), and a colour-calibration target (166). The PDF has no text layer and is not included in this repository.

## What is Markdown?
Markdown is a simple way of writing formatted text using plain characters, such as `#` for headings and `*asterisks*` for *italics*. A Markdown file is still readable as ordinary text, and can also be displayed with formatting.
* Learn more at [markdown.org](https://markdown.org/).
* Tools for displaying, editing, or converting Markdown files: [https://markdown.org/tools/](https://markdown.org/tools/)

## Artificial Intelligence
Extracted with Claude Code from Anthropic using the Sonnet 5.5 model.

The scan has no text layer, so each page was read from contrast-enhanced images of the scan and written out by AI. Every text page was then checked a second time against the scan by a separate AI agent, and a third time by another agent working blind from fresh high-resolution renders. The text is meant to show what the page shows, so the printer's spellings and errors, odd verse numbers, punctuation and hyphenation are kept as they appear, and a word is never filled in from the Doctrine and Covenants or from memory. Where a mark was too worn to tell a comma from a period, the gap after it and whether the next word starts with a capital letter were used to decide. A few things are deliberately **not** reproduced: the thin space the type puts before `;`, `:`, `?` and `!`, ink specks and stains, the show-through of the other side of the leaf, and the handwriting and stamps on the endpapers (they are described in comments).

**This is an AI transcription, and the scan is hard to read.** Faint ink and show-through mean that many words could be read only in part. Unclear readings are marked in the page files with `<!-- uncertain: … -->` (about 1,700 of them) or `[illegible]` where too few letters are visible to read the word (about 120), and the compiled text keeps the `[illegible]` marks. The second and third readings found and fixed a small number of silently "corrected" printer's errors and filled-in words, and the third reading found almost nothing more to change, but the readers are all the same kind of AI, and no page has been proofread by a person. The faintest pages (for example PDF pages 14, 18, 20–21, 51–52, 74, 106, 136 and 163) and worn letters that could be either of two readings are the most likely places for a remaining error. A few printer's slips in the catalog (such as "begotton" and "hoose") may be worn type in this one copy rather than errors of the press. For anything that matters, check the scan.

See [transcription-notes.md](transcription-notes.md) for how the text was extracted, the conventions used, what the audits found, and the readings that remain doubtful.

The scripts and the instructions given to the AI agents (transcription, audit and proofread specifications, and the page renderer) are in [tools/](tools/).

## Rebuilding the combined files
The page files are the source of truth. After editing any of them, regenerate the combined files and the typo catalog (Python 3, standard library only; run from the repository root):
```
python3 tools/compile_markdown.py     # book-of-commandments-1833.md
python3 tools/make_plaintext.py       # book-of-commandments-1833.txt
python3 tools/make_sparse.py          # book-of-commandments-1833-sparse.txt
python3 tools/make_typo_catalog.py    # printer-typos.md
python3 tools/check_structure.py      # checks the page files (verse and chapter sequence, markers, italics)
```
The scan itself is not in the repository; to re-render pages for checking, `tools/render_pages.py` needs the PDF and the `pypdfium2` and `pillow` packages. See [tools/README.md](tools/README.md).
