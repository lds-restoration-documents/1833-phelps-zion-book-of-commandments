# Transcription notes — 1833 Book of Commandments (Phelps, Zion)

Companion to `book-of-commandments-1833-pages/` (one Markdown file per PDF page). Structure follows the siblings'
`transcription-notes.md`. **Status: all 166 PDF pages are transcribed (Claude Sonnet 5.5), audited once against the images (PDF 4, 6–163), and then read a third time, blind, at 4x (PDF 4–163; §6b). PDF 1–3, 5 and 164–166 (covers, endpapers, verso, colour target) had their descriptions re-checked. No human proofread yet.**

## 1. Source and method

- **Source:** `public-rbc-2015gen25600-2015gen25600.pdf` (gitignored) from https://www.loc.gov/item/08025600/ (Library of Congress,
  Rare Book and Special Collections). 166 PDF pages, each a single JPEG about 1080–1190 x 1600 px; page 1 is a narrow strip (467 px) and
  the last page is landscape (1600 x 1265). No text layer.
- **The scan is a photograph of a tiny book** (cloth binding, stitched gutter and page edges visible; the text covers part of the image). The
  ink is faint and uneven; many pages show stains and mirror-image show-through from the other side of the leaf, and roughly every other
  page is much fainter than its neighbour. Native type height is about 25 px, so enlarging helps reading but adds no information; a
  flat-field + CLAHE test on the faintest page (163) did not help beyond the plain auto-contrast bands, so `render_pages.py` uses auto-contrast only.
- **Layout (PDF pages):** 1 spine strip; 2 front cover; 3 front endpaper; 4 title page (a paper strip hides the top, so the title begins
  at "COMMANDMENTS,"); 5 title-page verso, printed "(Copy Right Secured according to Law.)"; **6–163 the text** (Chapter I opens on 6,
  printed p. 3; printed page = PDF − 3, e.g. PDF 7 prints "4", PDF 160 prints "157"); 163 prints "160" and ends mid-chapter at
  Chapter LXV verse 47 (the printing was never finished; the rest of the page is blank); 164 rear endpaper; 165 back cover;
  166 a GretagMacbeth colour target. There is no separate preface or index: Chapter I is itself "A Preface" (D&C 1).
- **Verse numbering conventions seen:** each verse is a paragraph starting with its number. A chapter's italic heading line carries
  "1" (Chapters I, II) and the first sentence of the revelation follows as an unnumbered paragraph opening with a drop capital and
  small caps ("HEARKEN", "THE works", "BEHOLD"); the next number printed is "2". In Chapter LXV (PDF 160) no "1" is legible before
  the italic heading (only a fleck). Verse numbers are copied as printed.
- **Signature marks** (Footer lines) seen so far: "A2" (PDF 6), "A3" (8), "A4" (10): leaves 2–4 of gathering A; none on 7, 9. Page numbers
  are in the top centre. Pages that open a chapter (PDF 6, 10) carry the page number or none.
- **Sparse range:** `PAGE_RANGES = [(4, 4), (6, 163)]`; the title-page imprint lines (ZION, PUBLISHED BY..., 1833) are dropped, as in the 1830 repo.
- **Process:** each page is rendered at 2x and cut into two overlapping crops plus an overview (`tools/render_pages.py`); an agent reads the
  crops and writes the page. Batches of 16.

## 2. Conventions

See `tools/transcription-spec.md` (to be adapted to this edition in plan step 2).

## 3. Silent corrections and judgment calls

Pilot (main session). Items for the audits to re-check:

- **Printed forms kept:** "recompence", "strait", "intrusted", "willeth", "beareth record", "can not" (two words), "organised", "Idumea", "forgiveth".
  "doe[illegible]h" (PDF 9: a letter is blank between "doe" and "h", probably t) and "earth- and in heaven" (PDF 7: a hyphen is printed at the
  line end after "earth") are kept as seen.
- **Faint pages:** PDF 6, 8, 10 and 163 have washed-out stretches (right-hand line ends, lower thirds, stains). Words readable from partial letters
  are written with an `uncertain` comment; wholly hidden words are `[illegible]`. PDF 163 is the faintest. These are the most likely to differ between readers.
- **PDF 162:** the printed folio is over-inked (last digit 8 or 9), written `15[illegible]`; a pencil "79" at the top right is handwriting, not transcribed.
  The page text ends at verse 34 with the lower part blank; verse 35 begins PDF 163.
- **Written from the images only**, but the transcriber knows the later Doctrine and Covenants text; all faint readings are therefore the first thing to check in the blind pass.

## 4. Totals

(none yet)

## 5. Per-page log

(none yet)

## 6. Audits

| PDF pages | Written by | Audited by | Edits | Notes |
|---|---|---|---|---|
| 4, 6–10, 160, 162, 163 (pilot) | Sonnet 5.5 (main session) | Sonnet 5.5 subagent | 3 content edits + ~70 uncertain comments added | 163 "forbidden, to" -> "forbidden to"; 163 "this p[illegible]"; 162 header `15[illegible]` -> `158` (8 vs 9 doubt). Settled: 9 "doe[illegible]h" kept, 7 "earth-" is a faint printed hyphen, 160 has no "1" before the italic heading. PDF 1–3, 5 and 164–166 (covers/endpapers/target) written but not audited |
| 11–26 | Sonnet 5.5 subagent | Sonnet 5.5 subagent | 3 | 21 "desirest" -> "desiredst" (blotted e, flagged); 14 "hardness" vs "hardiness" comment; 15 period/comma comment. Open: 17/25 mark after "Harmony" (comma vs semicolon), 12 footer A5/A6 |
| 27–42 | Sonnet 5.5 subagent | Sonnet 5.5 subagent | 1 | 36 comment on worn "d" of "Redeemer". Main-session re-read of 41 verses 41–48 agreed with the file |
| 43–58 | Sonnet 5.5 subagent | Sonnet 5.5 subagents (43–51; then 52–58 after a rate-limit stop) | 5 | 45 "Amen." -> "Amen" (no mark visible); 51 verse 6 start gained "e,"; 52 verse 17 "[illegible]her[illegible]fore" -> "Th[illegible]fore" (the "her" was not visible); 44/46 footer B-vs-D comments; 48 header digit 5 vs 3 comment. Main session earlier restored 52 "begotten" -> "begotton" |
| 59–74 | Sonnet 5.5 subagent | Sonnet 5.5 subagent | 24 (13 content, 11 italics) | Filled-in words replaced by `[illegible]` partials: 65 v14, 66 v22, 67 v32, 71 v14; 74 header `71` -> `[illegible]` (it had come from the sequence); chapter heading marks 61 "XXVI" (no stop), 72 "XXXII," (comma). Chapter XXXII date on 72 reads "1839" (9 with a loop and tail, not the 0 of "1830" in XXXI). Open: 67 v33 "declared" vs "eeciared", 67 v40 number 40 vs 49, 65 v14 smudge |
| 75–90 | Sonnet 5.5 subagent | Sonnet 5.5 subagent | 9 | Printed forms restored: 78 "setond", 89 "hoose", 89 "lood" (main session re-read "hoose" at zoom and agrees); 80 v17 "be" -> "he"; 85 v18 invented word removed; 76 last word "re-". Confirmed "begioning" (78), "Cotesville" (83). Open: setond/second, hoose/house, lood/loud, he/be, time/tine |
| 91–106 | Sonnet 5.5 subagent | Sonnet 5.5 subagent | 8 text + 8 comment | 106 "souls not saved" and "Saying" restored from visible letters; 104 "accorping" (worn d vs p); 91 punctuation (3). Chapters XLIII–XLVIII print no "1" before the heading. Footers D1–D4 (100–106). Open: 106 v4–6 washed out, 91 v5 period/comma, 93 and 101 "he/be" |
| 107–122 | Sonnet 5.5 subagent | Sonnet 5.5 subagent | 0 text; 11 comments added, 4 reworded, 1 spacing | Re-check of 107, 109, 113 (almost no flags) found them genuinely clear (main session re-read 109 too). Open: 119 v3 numeral 3 vs 8, 121 "unto/unte" "rese/rose" v26 numeral, 118 "brethren,;" is real, 116 God/Gcd |
| 123–135 | Sonnet 5.5 subagent (cut off by a rate limit, no report) | Sonnet 5.5 subagent | 0 | First pass was more accurate than feared. Printed: "aposties" (127, 129), "iu lands" (135), "anp" (134, worn) |
| 126, 132, 136–138 | Sonnet 5.5 subagents | Sonnet 5.5 subagent (123–138) | 2 text + 3 comments | 126 "so" -> "6o" (a digit-6-like glyph before "o"; main session confirmed at zoom, a printer's wrong-character slip); 136 "tribulation" -> "tribulatiou"; 132 verse number "10." keeps its period. Footers E3 (136), E4 (138) confirmed |
| 139–150 | Sonnet 5.5 subagent | Sonnet 5.5 subagent | 0 text; 1 join, 1 comment removed, 5 reworded | 145 "tho" is a printed error (confirmed); open: 142 "uttermost/nttermost", 140 "churches/chruches", 149 "forewarn", 148 drop-cap word reads F-like |
| 151–159, 161 | Sonnet 5.5 subagents | Sonnet 5.5 subagent | 0 text; 3 comments added, 5 reworded | Open: 161 v15 "he/be", 161 v22 numeral 22/23, 159 v63 numeral, 157 "Newel/Newei" |

**Main-session consistency edits after the audits:** (1) In the italic heading lines the year digits are printed upright; the first 58 pages had them inside the italics. All 45 such headings were normalized to the 59–74 audit convention (month italic, year upright), checked against the images of PDF 31, 72 and 160. (2) Chapters I–XXV print "1" before the italic heading; XXXI–XLVIII print none (Chapters XXVI–XXX not yet re-checked for the cut-over; the audits of 59–106 confirmed the missing "1" from XXXI on).

## 6b. Blind third reading (proofread)

PDF 4–163 (160 pages) were read a third time by Sonnet 5.5 subagents in 10 batches (4–21, 22–37, 38–53, 54–69, 70–85, 86–101, 102–117, 118–133, 134–149, 150–163), working blind (they did not see the audit logs, this file beyond its method section, the typo catalog or the compiled text) from their own 4x renders, under `tools/proofread-spec.md`. The logs are kept locally in `logs/proof-log-*.md` (gitignored, not part of the repository).

**Result: 1 edit in 160 pages** (PDF 34, a heading comma written "1829 ," printed tight "1829,"), plus 28 logged disagreements where the reader saw a borderline letter or mark differently and the file's reading was kept with its existing uncertain comment. Zero spelling restorations, zero filled-in or dropped words, zero verse-number or cont-marker changes. Read with care: the readers are the same model as the transcribers and auditors, so a shared blind spot is possible; the main session re-read PDF 41, 74, 94, 99 and 109 against the images (and zoomed single spots on 19, 20, 52, 89, 126) and found no error beyond those the passes had already caught. The only things that need a human eye are the washed-out stretches (PDF 14, 18, 20–21, 51–52, 74, 106, 136, 163 and others), where the scan simply does not contain the letters.

Disagreements worth a human look (none changed): 43 v12 "Eternal/Eterial" and v19 "shrink/shrine"; 60 v31 "past term" vs "pat-/tern"; 61 chapter heading stop; 66 "again[illegible]t me"; 67 v33 "declared/eeciared"; 14 v6 "hardness/hardiness"; 17 and 25 mark after "Harmony"; 121 v26 mark after "hills"; 140 v61 "churches/chruches"; 149 v19 "forewarn"; 157 v48 "discipies/discipics"; 161 v15 "he/be", v21 "behold/beholo", v22 numeral; 107 v9 comma; 106 v4–6 partial letters in `[illegible]` stretches. The audits' flipped printed forms (`setond`, `hoose`, `lood`, `6o`, `tribulatiou`, `accorping`, `begotton`) are worn-type calls and appear in the catalog as such.

**Other findings during the proofread stage**
- Signature marks: the series A (PDF 6–18), B (36–50), C (68–82?), D (100–114), E (132–146) fall every 32 PDF pages, each leaf signed on its first recto. The C marks are written `c1`–`c4` on PDF 68–74 and `C5`–`C7` on 76–80: an ornate mark whose case could not be settled; the proofread suggested the same mark throughout. PDF 82's mark is smudged and not transcribed. Treat footer case as uncertain.
- PDF 5: the printed verso line is enclosed in curly braces, now `{Copy Right Secured according to Law.}`.
- Heading dates: month italic; the day number and year upright (`April* 6, 1830.`).
- Operational: the 4x/6x renders of eight parallel proofreaders filled the disk once; keep scratch renders small and delete `work/proof*`, `work/zoom*` after use. Rate limits stopped three batches; all agents skip finished pages, so reruns resume.

## 7. Compiled text and catalog

`book-of-commandments-1833.md` (about 43,300 words) is generated by `tools/compile_markdown.py` from the 166 page files: it removes comments, running heads and footers and rejoins verses marked `<!-- cont -->` (89 joins); a `<!-- page NNN -->` comment marks the start of each page. `[illegible]` marks stay in the text. `book-of-commandments-1833.txt` is the same with all markup removed. `book-of-commandments-1833-sparse.txt` is the title page (PDF 4, without the imprint lines ZION / PUBLISHED BY / 1833) plus PDF 6–163, i.e. the text of the work from Chapter I through the break in Chapter LXV; the covers, endpapers, title-page verso, rear endpaper, back cover and colour target are left out. Rebuild all three after any page edit.

`printer-typos.md` (37 occurrences) is generated by `tools/make_typo_catalog.py` from a curated list (dictionary scan of the compiled text, transcriber and auditor notes, main-session checks at zoom). Many rows are worn-type readings (`begotton`, `setond`, `hoose`, `lood`, ...): the copy is one photographed volume with faint ink, so a letter that looks like a slip may be worn type. It also lists the numbering irregularities (a verse number `10.`, three chapter-heading marks, the `1839` date in Chapter XXXII) and the table of chapters without a verse number 1 (Chapters XXXI–LXV; Chapters I–XXX print it, VI is lost). It has not had an independent blind re-read.

**Markdown check of the compiled file (2026-10-10).** Parsed with Python-Markdown: 64 `##` chapter headings, 76 italic spans (every chapter heading line plus the title-page lines), 2 bold title lines, no unbalanced asterisks, no leftover comments, rules, headers or footers, no control characters, no double or trailing spaces, no space before `; : ? !`, 160 page markers (PDF 4–163) with none missing. One rendering problem was found and fixed: a paragraph starting `10.` (PDF 132) rendered as a list item and lost its number, so the compiled `.md` now escapes it (`10\.`, as it does `1833\.`); the `.txt` and sparse files keep the plain `10.`.
