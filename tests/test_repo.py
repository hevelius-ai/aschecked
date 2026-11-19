"""S0 checks of the repository's fixed files. Written before the files and seen failing first."""

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# SHA-256 of the official CC BY 4.0 legal code, https://creativecommons.org/licenses/by/4.0/legalcode.txt
# (18,657 bytes, fetched 15 Nov 2026).
CC_BY_4_LEGALCODE_SHA256 = "9ba9550ad48438d0836ddab3da480b3b69ffa0aac7b7878b5a0039e7ab429411"


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def test_licence_is_the_cc_by_4_legal_code() -> None:
    text = read("LICENSE")
    assert text.lstrip().startswith("Attribution 4.0 International")
    assert "Creative Commons Attribution 4.0 International Public License" in text


def test_licence_is_the_official_text_byte_for_byte() -> None:
    assert hashlib.sha256((ROOT / "LICENSE").read_bytes()).hexdigest() == CC_BY_4_LEGALCODE_SHA256


def test_licence_code_is_mit_with_the_hevelius_notice() -> None:
    text = read("LICENSE-CODE")
    assert text.startswith("MIT License")
    assert "Copyright (c) 2026 Hevelius AI Group LLC" in text
    assert 'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND' in text


# Locked S0 check changed under the owner's decision S7-9 (17 Nov 2026, "yes"): on the release-candidate branch,
# which merges with the release tag, `test_readme_says_in_development_until_release` becomes this check.
def test_readme_carries_the_release_banner() -> None:
    first_screen = "\n".join(read("README.md").splitlines()[:10])
    assert "In development, not ready to use" not in first_screen
    assert "> **Version 1.**" in first_screen
    assert "cannot confirm that anything is secure" in first_screen
    # PR #5 review round 1 (MEDIUM): the banner names where and with which setting the benchmark was passed.
    flat_screen = " ".join(re.sub(r"^> ?", "", line) for line in first_screen.splitlines()).split()
    flat_screen = " ".join(flat_screen)
    assert "passed its benchmark in Claude Code with Claude Fable 5.2 at medium effort" in flat_screen


def test_line_endings_are_forced_to_lf() -> None:
    assert "* text=auto eol=lf" in read(".gitattributes")


# S7 Tier 4 (parked item from the S0 review, taken in under S7-12 Plan 3): the CI install pins pip by hash
# and refuses source builds, so no build tool is fetched without a hash check.
def test_ci_pins_pip_and_refuses_source_builds() -> None:
    ci = read(".github/workflows/ci.yml")
    installs = [line for line in ci.splitlines() if "pip install" in line]
    assert installs, "no pip install in CI"
    for line in installs:
        assert "--require-hashes" in line and "--only-binary :all:" in line, line
    assert any("requirements-pip.txt" in line for line in installs)
    assert installs.index(next(line for line in installs if "requirements-pip.txt" in line)) == 0
    pins = read("requirements-pip.txt")
    assert "pip==" in pins and "--hash=sha256:" in pins


# Added in PR #2 review round 1 (H1): an unquoted value holding ": " or " #" is not valid plain YAML, and GitHub then
# runs no job at all. The pinning test above read the lines as text and passed on the broken file.
def test_workflow_plain_values_are_valid_yaml() -> None:
    for path in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            match = re.match(r"^\s*(?:- )?[A-Za-z_-]+: (.+)$", line)
            if not match:
                continue
            value = match.group(1)
            if value[0] in "'\"|>[{&*!":
                continue
            assert ": " not in value and " #" not in value.split(" # ")[0] and not value.endswith(":"), (
                f"{path.name}:{number}: quote this value: {value}"
            )
