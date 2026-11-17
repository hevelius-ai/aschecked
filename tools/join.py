"""Build the one-file paste version of AsChecked from the skill folder (MIT, see LICENSE-CODE).

Usage:
    python tools/join.py           rebuild paste/aschecked-prompt.md from skills/aschecked/
    python tools/join.py --check   release check: fail if the paste file differs from a fresh build

The join drops SKILL.md's frontmatter, turns each pointer to a references/ file (in SKILL.md or in a reference,
quoted in backticks or not) into the name of the section it joins, and adds every reference file as a section, one
heading level down (code blocks untouched), in the order of their file names compared as plain text. A paste file
has no SKILL.md beside it, so the references' mentions of SKILL.md become "the method above". The build stops if a
pointer names a missing file or anything still reads "references/". Output uses LF line endings on every system,
so the same skill gives the same bytes on Windows and Linux.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = Path("skills") / "aschecked"
PASTE_FILE = Path("paste") / "aschecked-prompt.md"
POINTER = re.compile(r"`?(references/[A-Za-z0-9_-]+\.md)`?")
FRONTMATTER = re.compile(r"---\n.*?\n---\n+", re.S)
TITLE = re.compile(r"# (.+)\n")
FENCE = re.compile(r" {0,3}(`{3,}|~{3,})")


def read(path: Path) -> str:
    return path.read_bytes().decode("utf-8").replace("\r\n", "\n")


def demote_headings(text: str) -> str:
    """Add one '#' to every heading line outside fenced code blocks (backtick or tilde fences, as in CommonMark)."""
    lines, fence = [], ""
    for line in text.split("\n"):
        marker = FENCE.match(line)
        if marker and not fence:
            fence = marker.group(1)
        elif (
            marker
            and fence
            and marker.group(1)[0] == fence[0]
            and len(marker.group(1)) >= len(fence)
            and not line[marker.end() :].strip()
        ):
            fence = ""
        elif not fence and re.match(r"#+ ", line):
            line = "#" + line
        lines.append(line)
    return "\n".join(lines)


def reference_files(skill_dir: Path) -> list[Path]:
    """The reference files, ending exactly in '.md', in name order compared as plain text, the same on any system."""
    folder = skill_dir / "references"
    if not folder.is_dir():
        return []
    files = [path for path in folder.iterdir() if path.name.lower().endswith(".md")]
    for path in files:
        if not path.name.endswith(".md"):
            raise ValueError(f"references/{path.name}: rename it to end in '.md' (lower case)")
    return sorted(files, key=lambda path: path.name)


def build(skill_dir: Path) -> str:
    skill = read(skill_dir / "SKILL.md")
    front = FRONTMATTER.match(skill)
    if not front:
        raise ValueError("SKILL.md must open with a frontmatter block between two '---' lines")
    parts = [skill[front.end() :]]

    titles: dict[str, str] = {}
    for ref in reference_files(skill_dir):
        text = read(ref)
        title = TITLE.match(text)
        if not title:
            raise ValueError(f"references/{ref.name} must open with a '# ' title line")
        titles[f"references/{ref.name}"] = title.group(1).strip()
        parts.append(demote_headings(text).replace("SKILL.md", "the method above"))

    def section_name(match: re.Match[str]) -> str:
        rel = match.group(1)
        if rel not in titles:
            raise ValueError(f"a pointer names {rel}, which does not exist")
        return f'the section "{titles[rel]}" below'

    out = "\n".join(POINTER.sub(section_name, part).rstrip("\n") + "\n" for part in parts)
    if "references/" in out:
        raise ValueError("the paste file would still contain 'references/'; write pointers as references/<name>.md")
    return out


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    args = sys.argv[1:] if argv is None else argv
    built = build(root / SKILL_DIR)
    paste = root / PASTE_FILE
    if "--check" in args:
        if paste.is_file() and read(paste) == built and b"\r" not in paste.read_bytes():
            print(f"release check: {PASTE_FILE.as_posix()} matches a fresh build")
            return 0
        print(
            f"release check failed: {PASTE_FILE.as_posix()} differs from a fresh build of {SKILL_DIR.as_posix()}/. "
            "Run: python tools/join.py",
            file=sys.stderr,
        )
        return 1
    paste.parent.mkdir(parents=True, exist_ok=True)
    paste.write_bytes(built.encode("utf-8"))
    print(f"wrote {PASTE_FILE.as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
