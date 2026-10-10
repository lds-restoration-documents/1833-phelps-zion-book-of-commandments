# Transcription spec — 1833 W. W. Phelps & Co. (Zion) Book of Commandments

These are the instructions for the transcribing agents, one batch of pages at a time.
`<WORKDIR>` is the directory produced by `tools/render_pages.py` (normally `work`).

## The source

The scan is a **photograph of a tiny book**, not a flatbed scan. Each PDF page shows one book page lying open on a dark surface, with
the cloth binding, the stitched gutter and the stacked page edges visible; the text covers only part of the image. The ink is faint and
uneven, some lines are washed out or stained, and **the text of the other side of the leaf often shows through (mirror-image,
fainter)**. PDF pages are not printed pages: the printed folio is recorded as it appears. There is no text layer and no OCR helper.
Pages at the very start and end are covers, bookplates, library stamps, colour targets or rulers.

Inputs for PDF page N (NNNN = 4-digit zero-padded) in `<WORKDIR>/img/`:
- `pNNNN_0_overview.jpg`: whole page, original colour, low-res (layout only: where the text block is, headings, stains)
- `pNNNN_1_top.jpg`, `pNNNN_2_mid.jpg`, `pNNNN_3_bottom.jpg`: three overlapping bands in **contrast-enhanced grayscale** (the binding on the right
  is cropped away). Lines near the band edges appear in two bands; do not duplicate them.
- If a doubtful spot needs more detail, re-render that page larger with `--scale 4` (or `6`) and/or `--color`. The scan's native resolution is
  low (type is about 25 px high), so enlarging helps reading but adds no information; zoom the doubtful spot before deciding.

Output: `book-of-commandments-1833-pages/page-NNN.md` (3-digit zero-padded PDF page number, e.g. `page-020.md`).

Procedure per page: view the overview, then all three bands, then write the page. Read slowly: accuracy matters far more than speed.
Transcribe exactly what is printed: 1833 spelling, punctuation, capitalization, abbreviations, run-together or split words.
Words split across lines by a hyphen are JOINED into the whole word; words hyphenated in the original stay hyphenated.

## What this edition looks like

Single column. A preface and then chapters ("CHAPTER I." etc. in the headings, sometimes with a short printed heading) of **numbered verses**: each verse starts a new
paragraph with its number in ordinary type before the first word (`16 Therefore fear not...`). Long verses wrap over many lines and may run
across pages. Running heads and page numbers appear at the top of many pages (e.g. a small "3"). Signature marks (a letter or numeral, sometimes
with `*`) may appear at the foot of some pages. The type puts a thin space before `: ; ? !`, as in the 1830 Book of Mormon. Read the heading
and verse numbering as printed: numbering errors are part of the text.

**Printed page = PDF page − 3** from the first text page on (PDF 7 prints "4"). PDF 6 is Chapter I (no printed number seen). Only a cross-check: always record the printed number as it appears.

**Chapter openings in this edition:** a short rule above the chapter heading on most chapters; `CHAPTER N.` centred; an italic heading line starting with the verse number "1" (in Chapter LXV no "1" is legible); then the first sentence of the revelation as an unnumbered paragraph opening with a large drop capital and small caps ("HEARKEN", "THE", "BEHOLD"). Write the drop-capital word in full capitals as printed and put the comment `<!-- the next paragraph opens with a large drop-capital X and no verse number -->` in front of it. The next number printed is "2".

**Italic heading lines and dates.** The italic heading line is set in italics, but the year digits (and the mark right after them) are printed upright. Write the year outside the asterisks, e.g. `*A Revelation given to Joseph, in Harmony, Pennsylvania, May,* 1829. *saying:*` or, when the year ends the line, `*A Revelation to David, given in Fayette, New-York, September,* 1830.` When the italics close and reopen around the year, put each marker against the italic word, not the space: `*Revelation to X, given in Ohio, July,* 1828, *after Martin ...*` (never `1828,* after`: a star followed by a space is printed as a literal asterisk). Month names stay italic; a day number and its comma are upright too (`April* 6, 1830.`).

**Faint pages.** About half the pages are faint, with washed-out right-hand line ends and stains. Write words you can read from partial letters (add an `uncertain` comment on the page-level run when a stretch is hard) and `[illegible]` for words that are not there. Never read a washed-out word from memory of the text.

## Markdown format

```
<!-- PDF page NNN -->
**Header:** 3                             <- running head/page number as printed, parts separated by " | " (omit the line if none)

## CHAPTER IV.                            <- chapter headings as ## (and a book title or preface heading as #), exactly as printed

5 Behold I am God and have spoken it: ...  <- one paragraph per verse, verse number first, then a space

<!-- cont --> ... of the world; and before   <- a paragraph continued from the previous page (see below)

---

Footer: B                                 <- signature mark or catchword not already in the Header (omit if none)
```

Rules:
- **One paragraph per verse**, the number as printed, then a space, then the text. A verse starts where a number is printed in the text.
  Text that merely wraps is the same verse. If the printing has a paragraph break inside a verse (an indented line with no number), write a new paragraph.
- **Verse numbers are text.** Copy them as printed even if wrong, out of sequence, repeated, or missing; add a short comment
  `<!-- verse number printed "13", sequence expects 14 -->` for a number out of sequence, and **never** insert a missing number or fix a wrong one. If a chapter's
  first verse has no printed number, write none.
- **Continuations across pages.** If the first paragraph on the page continues the previous page's verse (the page opens flush-left, or with a word fragment, with no verse number),
  start that line with `<!-- cont -->`, e.g. `<!-- cont --> ing covenant might be established;`. `tools/compile_markdown.py` uses it to rejoin
  the verse. A page that opens with a verse number or a heading is a new paragraph: no marker. If the page ends mid-verse, write the fragment as is.
  A flush-left first line is a continuation even after a full stop. Check every page top.
- **Hyphens.** A hyphen at a line end inside the page is joined by you (`mighty` for `migh-`/`ty`). If it splits an already hyphenated word or compound, let the rest of the
  printing decide (grep the existing page files for the word); if nothing settles it, close it up and, only if truly ambiguous, add a one-line comment. A hyphen at the end of the
  **last line of a page** is kept (`vis-`) and the next page starts `<!-- cont --> ions ...`; the compile script closes it up.
- Italic type is `*italic*`; check for it. Small caps are written as capitals; a word that is merely capitalized in ordinary type keeps its printed case.
- **Headings, summaries, running heads, signature marks:** write as printed. The running head goes on the `Header:` line (left/centre/right parts separated by ` | `); the printed page number is recorded as it appears, even if wrong. Pages that open a section may have no running head.
- **Decorative rules and ornaments:** note them in a one-line HTML comment only where actually printed (e.g. a rule above a chapter heading). Do not invent them.
- **Spacing before `: ; ? !` is NOT transcribed:** write no space (`more: perform`). The marks themselves, their order and capitals after them are kept as printed.
- **Specks, stains and show-through.** Foxing, stains, ink specks, the binding, and the **mirror-image text of the other side of the leaf are not text**. Do not transcribe show-through. A mark that does not read as a deliberate punctuation mark or letter is ignored without a comment.
  Use `<!-- uncertain: ... -->` only when a real mark or letter is genuinely in doubt.
- **Comma versus period when uncertain:** use the gap after the mark and the next word's case: more space and a capital = period; less space and a lowercase word = comma. If the two signals disagree, use the shape. A mark that is plainly one or the other is written as printed.
- **Faded, stained or cut-off text.** Write only the letters you can see. **Never complete or guess text from memory**, from the Doctrine and Covenants, the Book of Mormon, the Bible, later editions, or the manuscripts: you know these texts and the scan is the only authority. Where a word or part of a word cannot be read, write `[illegible]` in its place (one per unreadable word; `[illegible]` inside a word for missing letters, e.g. `er in my [illegible]`); for a washed-out stretch write `[illegible]` once and describe the extent in a comment (`<!-- last 4 words of line unreadable (water stain) -->`). If a word is readable but a letter is doubtful, write your best reading with an `uncertain` comment. A letter is kept if about half or more of it is visible; a mere sliver is dropped. If the scan itself trims a page edge, write the visible fragments and say which edge in a comment at the top.
- **Covers, bookplates, library stamps, colour targets, rulers, blank pages, handwriting:** describe briefly in an HTML comment. Transcribe any legible printed text (title page as stacked lines in printed order and capitalization, with a layout comment); handwritten notes, shelfmarks and stamps are described only.
- Do not add commentary, summaries, modern punctuation or corrections.

## Addenda

Never silently "correct" a reading to what you think it should be. Printer's errors, odd spellings, missing or doubled words, damaged type and wrong running heads, folios
and verse numbers are all kept as printed, e.g. a verse that reads `end feet` is written `end feet` if that is what the page prints. If a reading is doubtful, keep your best reading
and add an HTML comment right after it, e.g. `Zarahemla <!-- uncertain: maybe Zarahenla -->`.

A page that comes out looking exactly like the modern Doctrine and Covenants text deserves suspicion: re-check it against the image word by word. This edition differs from the later
text in wording and spelling in many small ways, and a transcriber who "knows" the text will read the remembered words instead of the printed ones.

## How the agents are run (not part of the spec they see)

- The agent must view the images for every page. If the image tool fails, it stops and reports the page as failed; there is no OCR to fall back on and memory of the text is not an allowed source.
- Pages are processed in batches of 16, one page at a time, writing each file right after reading it; a batch skips pages whose output file already exists, so an interrupted batch can resume.
- The agent must not run git commands.
