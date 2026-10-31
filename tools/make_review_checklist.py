#!/usr/bin/env python3
"""Build review-checklist.md: every place in the transcription that needs a human look against the scan.

Sources (all read from the page files, so the list stays current after edits):
  * every `[illegible]` mark (letters or words that could not be read);
  * every `<!-- uncertain: ... -->` comment that names two possible readings, or concerns a numeral, folio, running head or
    signature mark (the many other uncertain comments only say that print is faint; they are counted per page, not listed).
Plus a short curated list of judgment calls and convention questions for the owner (see EXTRA below).

Usage:  python3 tools/make_review_checklist.py [--pages-dir DIR] [--out FILE]
"""
import argparse
import glob
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OFFSET = 3  # printed page = PDF page - 3 in the text

ALT = re.compile(r'\bvs\b|\bversus\b|\bor\b.{0,40}\b(could|might|may)\b|\b(could|might|may) (be|read)\b|cannot be excluded|'
                 r'\breads (like|as)\b|\blooks? like|\bor a\b|either|ambiguous|not certain|can ?not (be )?(tell|judge|settle|decide)', re.I)
NUM = re.compile(r'numeral|verse number|digit|folio|header|running head|signature|footer', re.I)
PUNCT = re.compile(r'comma|period|semicolon|colon|full stop|mark after|punctuation', re.I)

EXTRA = """
## Judgment calls and conventions for the owner

These are decisions rather than misreadings; each is recorded in `transcription-notes.md`.

- [ ] **Signature marks.** The series is A (PDF 6–18), B (36–50), C (68–82), D (100–114), E (132–146); one mark every other page. The C marks are written lowercase (`c1`–`c4`, PDF 68–74) and capital (`C5`–`C7`, PDF 76–80) although they look like the same ornate mark; the case is unsettled. PDF 82's mark is smudged and not transcribed. PDF 44 and 46 (`B5`, `B6`) could be `D5`, `D6`.
- [ ] **Worn type versus printer's slip.** These rows of `printer-typos.md` rest on how a worn letter was read at zoom: `begotton` (PDF 52), `setond` (78), `hoose` and `lood` (89), `ben gathereth` (102), `accorping` (104), `rese` (121), `anp` (134), `tribulatiou` (136), `Zien` (157), and `6o` for `so` (126; the first glyph looks like the digit 6). Decide for each whether it is printed so or only looks so in this copy.
- [ ] **PDF 162 running head.** It reads `158` (the last digit is over-inked; 9 cannot be excluded), where the sequence expects 159 and PDF 161 already prints 158. Folios of PDF 74 and a few others are too faint and are recorded as `[illegible]`.
- [ ] **Lost or hidden text.** The top of PDF 20 and the upper left of PDF 21 are lost (a tear or fold), including the heading of Chapter VI; the transcription has no Chapter VI heading. A paper strip hides the top of the title page (PDF 4).
- [ ] **The verse number 1 before the italic heading.** Chapters I–XXX print it (Chapter VI lost); Chapters XXXI–LXV do not. Confirm this is the printing and not a change in the scan.
- [ ] **Heading dates.** The year digits (and the day number) in the italic heading lines are written upright, the month italic. Confirm the convention on a few headings (for example PDF 31, 46, 72).
- [ ] **Printed irregularities kept:** verse number `10.` with a full stop (PDF 132); `CHAPTER XVIII..` (PDF 46); `CHAPTER XXXII,` (72); `CHAPTER XXVI` without a stop (61); the date `September, 1839` in the Chapter XXXII heading (72); `15[8]` folio on PDF 162.
- [ ] **PDF 5 verso.** The printed line is enclosed in curly braces `{Copy Right Secured according to Law.}`; the full stop is partly hidden by the closing brace.
- [ ] **Not reproduced on purpose.** The thin space before `; : ? !`, specks and stains, show-through of the reverse, and the handwriting and stamps (described in comments only).
"""


def strip(s):
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    return re.sub(r'\s+', ' ', s.replace('*', '')).strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--pages-dir', default=str(ROOT / 'book-of-commandments-1833-pages'))
    ap.add_argument('--out', default=str(ROOT / 'review-checklist.md'))
    args = ap.parse_args()

    chapter, verse = None, None
    pages = {}          # pdf page -> list of (location, tags, context, note)
    counts = {}         # pdf page -> (uncertain total, illegible total)
    for f in sorted(glob.glob(str(Path(args.pages_dir) / 'page-*.md'))):
        n = int(f[-6:-3])
        if n < 4 or n > 163:
            continue
        raw = Path(f).read_text(encoding='utf-8')
        counts[n] = (len(re.findall(r'<!--\s*uncertain', raw)), raw.count('[illegible]'))
        items = []
        for line in raw.split('\n'):
            if not line.strip() or line.startswith('<!-- PDF page'):
                continue
            plain = re.sub(r'<!--.*?-->', '', line)
            m = re.match(r'^\s*(?:<!--.*?-->\s*)*## CHAPTER ([IVXLC]+)', line)
            if m:
                chapter, verse = m.group(1), None
                loc = f'Ch. {chapter} heading'
            elif re.match(r'^\s*\*\*Header:\*\*', line):
                loc = 'running head'
            elif re.match(r'^\s*Footer:', line):
                loc = 'signature mark'
            else:
                mv = re.match(r'^\s*(?:<!--.*?-->\s*)*(\d+)[ .]', line)
                if mv:
                    verse = int(mv.group(1))
                loc = f'Ch. {chapter} v. {verse}' if chapter and verse else (f'Ch. {chapter} heading line' if chapter else 'front matter')
            # walk the line: comments and [illegible] marks in order
            for m in re.finditer(r'<!--\s*uncertain:(.*?)-->|\[illegible\]', line, flags=re.S):
                before = strip(line[:m.start()])[-70:]
                after = strip(line[m.end():])[:35]
                if m.group(0) == '[illegible]':
                    # merge neighbouring marks
                    if items and items[-1][4] == line and items[-1][5] and m.start() - items[-1][5] < 6 and items[-1][1] == ['missing']:
                        items[-1] = items[-1][:5] + (m.end(),) + items[-1][6:]
                        continue
                    items.append((loc, ['missing'], f'…{before} **[illegible]** {after}…', 'letters or words not readable', line, m.end()))
                else:
                    note = re.sub(r'\s+', ' ', m.group(1)).strip()
                    tags = []
                    if ALT.search(note):
                        tags.append('two readings')
                    if NUM.search(note):
                        tags.append('number/head/foot')
                    if tags and PUNCT.search(note):
                        tags.append('punctuation')
                    if not tags:
                        continue
                    items.append((loc, tags, f'…{before} **⟨here⟩** {after}…', note[:260] + ('…' if len(note) > 260 else ''), line, None))
        if items:
            pages[n] = items

    total = sum(len(v) for v in pages.values())
    miss = sum(1 for v in pages.values() for i in v if i[1] == ['missing'])
    head = f"""# Review checklist: places in the transcription that need a human look

The text was transcribed, audited and proofread by AI from a faint photograph of one small book, and no page has been proofread by a person.
This file lists **{total} places** where the scan was doubtful: {miss} stretches marked `[illegible]` (letters or words that could not be read) and {total - miss} readings where the transcription keeps one reading but names another
(including doubtful punctuation marks, numerals, running heads and signature marks). Each is listed under its PDF page with the chapter and verse, the surrounding text and the doubt as recorded in the page file.
The hundreds of other `uncertain` comments only say that the print is faint (the reading was made from partial letters); they are not listed, but each page's count is given, and a page with many of them deserves a full read.

**How to check.** Open the scan at the PDF page (printed page = PDF page − 3). To enlarge a page for reading: `~/.venvs/lds-transcribe/bin/python tools/render_pages.py public-rbc-2015gen25600-2015gen25600.pdf --out work --pages N --scale 4`. A reading is only worth changing if the letters can be seen; never fill in a word from the Doctrine and Covenants or from memory.
After editing a page file, rebuild the combined files and this list (see the README).

Generated by `tools/make_review_checklist.py` from the page files.

## Pages by amount of doubt

PDF pages with at least 25 faint-print flags or at least one `[illegible]` mark (flags = all `uncertain` comments on the page; "listed items" = the entries below for that page).

| PDF | printed | flags | `[illegible]` | listed items |
|---|---|---|---|---|
"""
    rank = sorted(((n, c) for n, c in counts.items() if c[0] >= 25 or c[1] > 0), key=lambda x: (-x[1][1], -x[1][0], x[0]))
    # order by page for readability of the table, but mark the heaviest first in a short list
    table = ''.join(f'| {n} | {n - OFFSET if n >= 6 else "—"} | {c[0]} | {c[1]} | {len(pages.get(n, []))} |\n' for n, c in sorted(rank))
    heavy = ', '.join(f'{n} ({c[0]}/{c[1]})' for n, c in sorted(counts.items(), key=lambda x: -(x[1][0] + 5 * x[1][1]))[:12])
    sec = f'\nHeaviest pages (flags/illegible): {heavy}.\n\n## Items by page\n'
    body = []
    for n in sorted(pages):
        pr = n - OFFSET if n >= 6 else '—'
        body.append(f'\n### PDF {n} (printed {pr})\n')
        for loc, tags, ctx, note, _line, _end in pages[n]:
            body.append(f'- [ ] **{loc}** [{", ".join(tags)}] {ctx}' + ('' if tags == ['missing'] else f'  \n  {note}'))
    Path(args.out).write_text(head + table + sec + '\n'.join(body) + '\n' + EXTRA, encoding='utf-8')
    print(f'{total} items on {len(pages)} pages -> {args.out}')


if __name__ == '__main__':
    main()
