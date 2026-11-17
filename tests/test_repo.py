"""S0 checks of the repository's fixed files. Written before the files and seen failing first."""

import hashlib
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


def test_readme_says_in_development_until_release() -> None:
    first_screen = "\n".join(read("README.md").splitlines()[:10])
    assert "In development, not ready to use" in first_screen


def test_line_endings_are_forced_to_lf() -> None:
    assert "* text=auto eol=lf" in read(".gitattributes")
