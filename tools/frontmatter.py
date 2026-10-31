"""Helper for scripts that read book-of-commandments-1833.md: remove its YAML frontmatter."""


def strip_frontmatter(t):
    """Remove the YAML frontmatter block that compile_markdown.py puts at the top of book-of-commandments-1833.md."""
    if t.startswith('---\n'):
        end = t.find('\n---\n', 4)
        if end != -1:
            return t[end + 5:].lstrip('\n')
    return t
