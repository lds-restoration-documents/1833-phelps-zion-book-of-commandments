#!/usr/bin/env python3
"""Build printer-typos.md: a catalog of the likely printer's typos and misspellings in the 1833 Book of Commandments.

The list of forms is curated below (triaged from a dictionary scan of the compiled text, the transcribers' and auditors'
notes, and a check of each candidate in the page images by the main session); this script finds every occurrence of each
form in book-of-commandments-1833.md, with its PDF page and a snippet of context, so the page numbers and contexts always
come from the current text. Spellings that were normal or intentional for the period or the edition (shew, recompence, strait,
...) are deliberately NOT cataloged; see NOT_INCLUDED at the end of the output.

The "Chapter headings without a verse number 1" table is computed from the page files (it is a pattern of the edition, not a typo).

Usage:  python3 tools/make_typo_catalog.py [--md FILE] [--pages-dir DIR] [--out FILE]
"""
import argparse
import glob
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORN = 'worn-type reading: the letter looks like the printed one; the audits kept it as printed'

# (printed, should be, note). `printed` is matched as a whole word, case-sensitive; a tuple (text, highlight) matches a literal text.
SECTIONS = [
    ('Letter or letters dropped or added', [
        ('concering', 'concerning', 'the same verse prints "concerning" a few words earlier'),
        ('cofirming', 'confirming', 'faint at the dropped letter'),
        ('unchangable', 'unchangeable', '"unchang-" / "able" at a line end; may be a period spelling rather than a slip'),
        ('viewe', 'view', 'extra e'),
    ]),
    ('Wrong letter (one letter printed for another)', [
        ('baing', 'being', ''),
        ('begioning', 'beginning', 'the letter after "gi" is an o at zoom'),
        ('reien', 'reign', 'printed twice'),
        ('discipies', 'disciples', 'the l reads like i; the e is worn'),
        ('aposties', 'apostles', 'an i for l; printed twice'),
        ('fuil', 'full', 'a dotted i for l'),
        ('tho', 'the', 'printed on PDF 48 and 145; the o is clear at zoom on PDF 145'),
        ('iu', 'in', '"even iu lands for their inheritance"'),
        (('hands end feet', 'end'), 'and', '"the prints of the nails in my hands end feet"'),
        (('as a ben gathereth', 'ben'), 'hen', '"a ben gathereth her chickens"; ' + WORN),
        ('Zien', 'Zion', 'the vowel reads like e; ' + WORN),
        ('glore', 'glory', 'no descender on the last letter'),
        (('even 6o:', '6o'), 'so', 'the first glyph looks like the digit 6; confirmed at zoom by the main session'),
        ('anp', 'and', '"mine anp and mine indignation"; ' + WORN),
        ('begotton', 'begotten', WORN),
        ('setond', 'second', 'a crossbar on the c; ' + WORN),
        ('hoose', 'house', 'the second vowel is a closed round o; ' + WORN),
        ('lood', 'loud', '"a lood voice"; ' + WORN),
        ('accorping', 'according', 'the letter after the break has a descender; ' + WORN),
        ('tribulatiou', 'tribulation', 'the last letter is closed at the bottom like a u; ' + WORN),
        (('as the rese:', 'rese'), 'rose', 'the vowel reads e at zoom 6; ' + WORN),
    ]),
]

# Misspellings that recur (the same slip printed several times): listed in their own section, with all pages.
RECURRING = [
    ('decieve / decieved', ['decieve', 'decieved'], 'deceive / deceived', 'ie for ei (all three on PDF 27)'),
]

# Numbering and heading irregularities: (literal text, highlight, label, expected, note)
NUMBERING = [
    ('10. And after you have done', '10.', '`10.`', '10', 'a verse number printed with a full stop after it; every other verse number has none'),
    ('## CHAPTER XVIII..', 'CHAPTER XVIII..', '`CHAPTER XVIII..`', 'CHAPTER XVIII.', 'a doubled full stop'),
    ('## CHAPTER XXXII, ', 'CHAPTER XXXII,', '`CHAPTER XXXII,`', 'CHAPTER XXXII.', 'a comma for the full stop'),
    ('## CHAPTER XXVI 1', 'CHAPTER XXVI', '`CHAPTER XXVI`', 'CHAPTER XXVI.', 'no full stop printed'),
    ('September,* 1839.', '1839', '`1839`', '1830', 'the date of the Chapter XXXII heading; the last figure is a 9 with a loop and tail (the Chapter XXXI heading prints "1830" with an oval 0); the other chapters of this group are dated September 1830'),
]

NOT_INCLUDED = """## Not included: spellings that were normal or intentional

These are non-standard by modern rules but are **not** counted as printer's slips, and are left out of the catalog:

- **The edition's own forms:** `-eth` and `-est` verb forms (`saith`, `hast`, `doeth`, `lieth`, `sheweth`, `desiredst`, `deliveredst`, `shouldst`, `canst`), `spake`, `wo`, `whosoever`, `whoso`, `forgiven`, `has`.
- **Period spellings:** `recompence`, `strait` and `straitway`, `intrusted`, `fulness`, `offence`, `organised`, `centre`, `benefitted`, `counsellors` / `counselled`, `travelling`, `rereward`, `fulfil`, `incircle`, `engraven`, `to-day` forms, `New-York`.
- **Names:** `Hyrum`, `Kirtland`, `Fayette`, `Colesville`, `Canandaigua`, `Heman`, `Zebidee`, `Northrop`, `Lemuelites` and the like are not checked against a standard form. (`Cotesville` is listed because the same name is printed `Colesville` twice.)
- **Grammar of the revelations:** `I willeth`, `ye ... hath`, `that that which cometh from above` (PDF 159: grammatical, with "that" as conjunction and as demonstrative), `my servant ... hast`.
- **Faint or damaged print** that the transcription records as `[illegible]` or as a flagged reading: words that are only partly visible are not listed.
- **Printed folios and signature marks** are not part of the compiled text; see the notes below for the one folio that looks wrong.
"""

FOLIO_NOTE = """## Printed page numbers (not in the compiled text)

The running head is kept in the page files but not in the compiled text. One printed number looks wrong: PDF 162 prints `158` (the last digit is over-inked, a 9 cannot be excluded) where the sequence expects 159, and PDF 161 already prints 158. All other folios read PDF page − 3. PDF 74's folio and a few others are too faint to read and are recorded as `[illegible]`.
"""


def load(md):
    raw = md.read_text(encoding='utf-8')
    raw = re.sub(r'(?m)^(\d+)\\\.', r'\1.', raw)  # undo the list-marker escape written by compile_markdown.py
    parts = re.split(r'<!-- page (\d+) -->', raw)
    segs, cur = [], 0
    for i, t in enumerate(parts):
        if i % 2 == 1:
            cur = int(t)
            continue
        t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
        segs.append((cur, re.sub(r'\s+', ' ', t)))
    return segs


def find(segs, spec):
    """Yield (page, snippet) for each occurrence."""
    if isinstance(spec, tuple):
        pat, hit = spec
        rx = re.compile(re.escape(pat))
        hl = hit
    else:
        rx = re.compile(r'(?<![A-Za-z])' + re.escape(spec) + r'(?![A-Za-z])')
        hl = spec
    for pg, t in segs:
        if pg < 4 or pg > 163:
            continue
        for m in rx.finditer(t):
            a = max(0, m.start() - 38)
            b = min(len(t), m.end() + 30)
            s = t[a:b]
            i = s.find(hl) if hl in s else 0
            s = s[:i] + '**' + s[i:i + len(hl)] + '**' + s[i + len(hl):]
            yield pg, ('…' if a else '') + s.strip() + ('…' if b < len(t) else '')


def printed(pg):
    return str(pg - 3) if 6 <= pg <= 163 else '—'


def row(spec, should, note, segs):
    out = []
    for pg, snip in find(segs, spec):
        label = spec[1] if isinstance(spec, tuple) else spec
        out.append((pg, '| `%s` | %s | %d | %s | %s%s |' % (label, should, pg, printed(pg), snip.replace('|', '\\|'),
                                                           (' (' + note + ')') if note else '')))
    return out


def chapter_one_table(pages_dir):
    """Chapters whose italic heading line has / has not a printed verse number 1."""
    rows = []
    for f in sorted(glob.glob(str(Path(pages_dir) / 'page-*.md'))):
        n = int(f[-6:-3])
        lines = Path(f).read_text(encoding='utf-8').split('\n')
        for i, l in enumerate(lines):
            m = re.match(r'^## CHAPTER ([IVXLC]+)', l)
            if not m:
                continue
            j = i + 1
            while j < len(lines) and (not lines[j].strip() or re.fullmatch(r'\s*(<!--.*?-->\s*)+', lines[j])):
                j += 1
            nxt = re.sub(r'<!--.*?-->', '', lines[j]).strip() if j < len(lines) else ''
            rows.append((n, m.group(1), bool(re.match(r'^1\s+\*', nxt))))
    with_one = [c for n, c, h in rows if h]
    without = [(c, n) for n, c, h in rows if not h]
    return with_one, without


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--md', default=str(ROOT / 'book-of-commandments-1833.md'))
    ap.add_argument('--pages-dir', default=str(ROOT / 'book-of-commandments-1833-pages'))
    ap.add_argument('--out', default=str(ROOT / 'printer-typos.md'))
    args = ap.parse_args()
    segs = load(Path(args.md))
    total, missing = 0, []
    header = '| Printed | Should be | PDF p. | Printed p. | In context |\n|---|---|---|---|---|'
    body = []
    for title, items in SECTIONS:
        rows = []
        for spec, should, note in items:
            r = row(spec, should, note, segs)
            if not r:
                missing.append(spec)
            rows += r
        rows.sort(key=lambda x: x[0])
        total += len(rows)
        body.append('\n## %s (%d)\n\n%s\n%s' % (title, len(rows), header, '\n'.join(r for _, r in rows)))

    rec = []
    for label, forms, should, why in RECURRING:
        hits = sorted(h for f in forms for h in find(segs, f))
        total += len(hits)
        if not hits:
            missing.append(label)
        pages = ', '.join(str(p) for p, _ in hits)
        rec.append('| `%s` | %s | %d | %s | %s |' % (label, should, len(hits), why, pages))
    recsec = ('\n## Misspellings that recur\n\nThe same slip printed more than once.\n\n'
              '| Printed | Should be | Times | Slip | PDF pages |\n|---|---|---|---|---|\n' + '\n'.join(rec))

    names = row('Cotesville', 'Colesville', '`Colesville` is printed twice (PDF 58, 62); the third letter has a crossbar at zoom', segs)
    if not names:
        missing.append('Cotesville')
    total += len(names)
    namesec = '\n## Names printed in a variant spelling (%d)\n\n%s\n%s' % (len(names), header, '\n'.join(r for _, r in names))

    num = []
    for text, hit, label, expected, note in NUMBERING:
        found = list(find(segs, (text, hit)))
        if not found:
            missing.append(label)
        for pg, snip in found:
            num.append((pg, '| %s | %s | %d | %s | %s (%s) |' % (label, expected, pg, printed(pg), snip.replace('|', '\\|'), note)))
    num.sort()
    total += len(num)
    numsec = '\n## Numbering, dates and chapter headings (%d)\n\n%s\n%s' % (len(num), header, '\n'.join(r for _, r in num))

    with_one, without = chapter_one_table(args.pages_dir)
    first_without = without[0][0] if without else '?'
    chap = f"""
## Chapter headings without a verse number 1

In Chapters I to XXX (except Chapter VI, whose heading is lost at the torn top of PDF 21) the italic heading line is numbered `1`, and the drop-capital paragraph that follows has no number, so verse 2 follows. From Chapter {first_without} on (Chapters {first_without} to LXV, {len(without)} chapters, first on PDF {without[0][1] if without else '?'}) no `1` is printed before the heading line. The transcription records this as printed. It is a change of style in the edition, not counted above as a slip.
"""
    intro = f"""# Printer's typos and misspellings in the 1833 Book of Commandments

A catalog of the places where the 1833 print itself has a slip of the type, a misspelling, a doubled mark or an irregular number, as the
transcription records it. {total} occurrences, grouped by the kind of slip, each with its PDF page, printed page (PDF − 3 in the text) and context.

**What is and is not here.** The transcription keeps every printed error exactly as printed (nothing was corrected from the Doctrine and
Covenants, later editions or the manuscripts), so all of these are in the page files as printed. This list leaves out spellings that were normal
or intentional for the period or the edition (`recompence`, `strait`, `sheweth` and the like; see the end of the file). It was built from a dictionary scan of the whole text,
the notes of the transcribers and auditors, and a check of each candidate by the main session, so it is **likely, not exhaustive**: a slip that
happens to produce another real word (`he` for `be`) is only caught where it was noticed. The scan is a photograph of one tiny copy with faint, uneven ink, so
**many rows are worn-type readings**: the scan shows a letter that looks like the printed one (`begotton`, `setond`, `hoose`), which the audits kept as printed. Whether such a
row is a slip of the type or only worn or inked-in type in this one copy cannot be told from the scan alone; they are marked in the notes. Words that are only partly visible and are
recorded as `[illegible]` are not listed.

**Not yet checked in a separate pass.** The rows were checked against the page images by the audits and, for the 6o / begotton / hoose / concering / tho forms, by the main session at zoom, but they have
not had the independent blind re-read that the 1830 catalog had.

Generated by `tools/make_typo_catalog.py` from the live text, so page numbers and contexts stay current if the pages are edited.
"""
    Path(args.out).write_text(intro + '\n'.join(body) + '\n' + namesec + '\n' + recsec + '\n' + numsec + '\n' + chap + '\n' + FOLIO_NOTE + '\n' + NOT_INCLUDED,
                              encoding='utf-8')
    print(f'{total} occurrences -> {args.out}')
    if missing:
        print('NOT FOUND in the text:', missing)


if __name__ == '__main__':
    main()
