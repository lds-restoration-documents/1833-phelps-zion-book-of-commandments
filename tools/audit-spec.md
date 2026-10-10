# Audit spec — restoring silent corrections in an existing transcription

Used when a batch of pages needs a second pass against the scan. `<WORKDIR>` is the directory produced by `tools/render_pages.py`.

Context: `book-of-commandments-1833-pages/page-NNN.md` are transcriptions of the 1833 W. W. Phelps & Co. (Zion) Book of Commandments (public domain), from a photographic scan of a tiny book with faint ink and show-through from the other side of the leaf.
A model transcribing this text is likely to SILENTLY CORRECT what the scan shows toward what it remembers of later editions
(the later Doctrine and Covenants wording, modern punctuation and spelling, "corrected" grammar, names, verse numbers). The rule is: the file
must show EXACTLY what is printed on the page image, including printer's errors, odd spellings, odd punctuation and capitalization,
and the 1833 verse numbering and paragraphing. See `tools/transcription-spec.md` for the file format.

Inputs per PDF page N (NNNN = 4-digit, NNN = 3-digit) in `<WORKDIR>/img/`: `pNNNN_1_top.jpg`, `pNNNN_2_mid.jpg`, `pNNNN_3_bottom.jpg` (contrast-enhanced grayscale bands, slight overlap), `pNNNN_0_overview.jpg` (colour, layout only). There is no OCR text.
If the crops are too small to settle a doubtful spot, re-render the page larger: `~/.venvs/lds-transcribe/bin/python tools/render_pages.py public-rbc-2015gen25600-2015gen25600.pdf --out work --pages N --scale 4`.

## Per-page procedure

1. View all three bands (and the overview if the layout is unclear). Read the existing `page-NNN.md`.
2. Compare line by line. Look especially for:
   - words, spellings, names, capitalization and punctuation changed from print (printer's typos silently fixed, modern spellings substituted);
   - punctuation added, removed or "normalized" ; the thin space the type puts before `; : ? !` is NOT checked: the files have none;
   - **verse numbers** added, fixed, dropped or invented (a number printed wrongly or out of sequence stays as printed; a missing number stays missing);
   - **text completed from memory** where the scan is faded or cut off (check every such spot: it must read as the visible letters, or `[illegible]`);
   - **show-through** (mirror text from the other side of the leaf) or stains transcribed as text;
   - paragraph breaks added or removed, or a paragraph split/merged at a page break without the correct `<!-- cont -->` marker;
   - words dropped, repeated or added, whole lines missing, lines out of order;
   - headings, chapter numbers, running heads, signature marks and folios changed from what is printed;
   - other specks and blemishes transcribed as if they were text (ignore marks that do not read as a deliberate mark or letter; see the transcription spec);
   - italics missing/added;
   - line-end hyphenations not joined, or compound hyphens wrongly joined.
3. For every discrepancy, edit the page file (minimal change, never rewrite the whole file) so it matches the scan exactly.
   If the scan is genuinely unreadable at that spot, leave the existing reading and make sure it carries an
   `<!-- uncertain: ... -->` comment (add one if missing). Do not add uncertain comments to readings you can read clearly.
   Do NOT fix real errors by "improving" them: if the scan prints "assemby", the file must say "assemby".
   Keep existing uncertain/layout comments unless you verified them and they are now wrong.
4. If a change log was requested, append an entry after each page: `## Page NNN`, then either `- no changes` or one line per
   change: `- <where>: was "<old>" -> now "<new>" (<reason>)`. A log also lets an interrupted run resume by skipping logged pages.

CRITICAL: if the image tool fails or errors for a page, do not guess from memory of the text; skip that page, do not record it as audited,
and list it as failed. If you hit an API/usage-limit error, just stop. Do not run git commands. Final reply: pages audited, total changes, pages failed (brief).
