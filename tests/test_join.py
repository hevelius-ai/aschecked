"""S2 locked checks of the join script and the release check (plan section 5, row S2). Written before the script.

The join builds `paste/aschecked-prompt.md` from `skills/aschecked/`: it drops SKILL.md's frontmatter, turns each
pointer to a `references/` file into the name of the section it joins, and adds every reference file as a section.
The release check rebuilds the paste file and fails on any difference.
"""

import importlib.util
import runpy
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
JOIN_PATH = ROOT / "tools" / "join.py"


def load_join():
    spec = importlib.util.spec_from_file_location("join", JOIN_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SKILL = (
    "---\n"
    "name: demo\n"
    "description: A demo skill.\n"
    "---\n"
    "\n"
    "# Demo\n"
    "\n"
    "## Steps\n"
    "\n"
    "1. Check the stacks; detail: `references/alpha.md`.\n"
)
ALPHA = "# Alpha checks\n\nSee SKILL.md for the rules.\n\n## One\n\n- first\n"
BETA = "# Beta scans\n\n## Two\n\n- second\n"


def make_skill(tmp_path: Path, newline: str = "\n") -> Path:
    skill_dir = tmp_path / "skills" / "aschecked"
    (skill_dir / "references").mkdir(parents=True)
    for rel, text in (("SKILL.md", SKILL), ("references/alpha.md", ALPHA), ("references/beta.md", BETA)):
        (skill_dir / rel).write_bytes(text.replace("\n", newline).encode("utf-8"))
    return skill_dir


def test_join_drops_frontmatter(tmp_path: Path) -> None:
    out = load_join().build(make_skill(tmp_path))
    assert out.startswith("# Demo\n")
    assert "name: demo" not in out
    assert "description:" not in out
    assert "---" not in out


def test_join_turns_pointers_into_section_names(tmp_path: Path) -> None:
    out = load_join().build(make_skill(tmp_path))
    assert 'detail: the section "Alpha checks" below.' in out
    assert "references/" not in out
    # A paste file has no SKILL.md beside it: the references' mentions of it name the method instead.
    assert "SKILL.md" not in out
    assert "See the method above for the rules." in out


def test_join_includes_every_reference(tmp_path: Path) -> None:
    out = load_join().build(make_skill(tmp_path))
    # Every reference file is joined, pointed at or not, in name order, one heading level down.
    alpha, beta = out.index("\n## Alpha checks\n"), out.index("\n## Beta scans\n")
    assert out.index("1. Check the stacks") < alpha < beta
    assert "\n### One\n\n- first\n" in out and "\n### Two\n\n- second\n" in out
    assert out.endswith("- second\n")


def test_join_output_identical_on_windows_and_linux(tmp_path: Path) -> None:
    join = load_join()
    lf = join.build(make_skill(tmp_path / "lf"))
    crlf = join.build(make_skill(tmp_path / "crlf", newline="\r\n"))
    assert lf == crlf
    root = tmp_path / "crlf"
    assert join.main([], root=root) == 0
    written = (root / "paste" / "aschecked-prompt.md").read_bytes()
    assert b"\r" not in written
    assert written.decode("utf-8") == lf


def test_release_check_rebuild_matches(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    join = load_join()
    # The committed paste file is exactly what the join builds from the committed skill.
    committed = (ROOT / "paste" / "aschecked-prompt.md").read_bytes()
    assert committed.decode("utf-8") == join.build(ROOT / "skills" / "aschecked")
    assert join.main(["--check"], root=ROOT) == 0
    # Any difference fails the check, and the message says how to fix it.
    root = tmp_path / "repo"
    make_skill(root)
    assert join.main(["--check"], root=root) == 1  # no paste file yet
    assert join.main([], root=root) == 0
    assert join.main(["--check"], root=root) == 0
    paste = root / "paste" / "aschecked-prompt.md"
    paste.write_text(paste.read_text(encoding="utf-8") + "edited by hand\n", encoding="utf-8")
    assert join.main(["--check"], root=root) == 1
    assert "python tools/join.py" in capsys.readouterr().err


# Further checks for the error paths and the command line (100% line and branch coverage of tools/join.py).


def test_join_refuses_a_skill_without_frontmatter(tmp_path: Path) -> None:
    skill_dir = make_skill(tmp_path)
    (skill_dir / "SKILL.md").write_text("# Demo\n", encoding="utf-8")
    with pytest.raises(ValueError, match="frontmatter"):
        load_join().build(skill_dir)


def test_join_refuses_a_pointer_to_a_missing_reference(tmp_path: Path) -> None:
    skill_dir = make_skill(tmp_path)
    (skill_dir / "references" / "alpha.md").unlink()
    with pytest.raises(ValueError, match="references/alpha.md"):
        load_join().build(skill_dir)


def test_join_refuses_a_reference_without_a_title(tmp_path: Path) -> None:
    skill_dir = make_skill(tmp_path)
    (skill_dir / "references" / "beta.md").write_text("no title\n", encoding="utf-8")
    with pytest.raises(ValueError, match="beta.md"):
        load_join().build(skill_dir)


def test_join_runs_as_a_script(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["join.py", "--check"])
    with pytest.raises(SystemExit) as exit_info:
        runpy.run_path(str(JOIN_PATH), run_name="__main__")
    assert exit_info.value.code == 0


# Added in review round 1 (findings J1 to J4), beside the locked tests; the locked tests are unchanged.


def test_join_rewrites_plain_pointers_and_pointers_in_references(tmp_path: Path) -> None:
    skill_dir = make_skill(tmp_path)
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    (skill_dir / "SKILL.md").write_text(skill + "2. Scans: references/beta.md.\n", encoding="utf-8")
    alpha = (skill_dir / "references" / "alpha.md").read_text(encoding="utf-8")
    (skill_dir / "references" / "alpha.md").write_text(alpha + "\nScans: `references/beta.md`.\n", encoding="utf-8")
    out = load_join().build(skill_dir)
    assert '2. Scans: the section "Beta scans" below.' in out
    assert '\nScans: the section "Beta scans" below.\n' in out
    assert "references/" not in out


def test_join_refuses_a_pointer_in_a_reference_to_a_missing_file(tmp_path: Path) -> None:
    skill_dir = make_skill(tmp_path)
    (skill_dir / "references" / "beta.md").write_text("# Beta scans\n\nSee `references/gone.md`.\n", encoding="utf-8")
    with pytest.raises(ValueError, match="references/gone.md"):
        load_join().build(skill_dir)


def test_join_refuses_leftover_references_text(tmp_path: Path) -> None:
    skill_dir = make_skill(tmp_path)
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    (skill_dir / "SKILL.md").write_text(skill + "2. See the references/ folder.\n", encoding="utf-8")
    with pytest.raises(ValueError, match="references/"):
        load_join().build(skill_dir)


def test_join_orders_references_by_plain_name(tmp_path: Path) -> None:
    # Compared as plain text, "Beta.md" sorts before "alpha.md" on every system; Windows paths would not.
    skill_dir = make_skill(tmp_path)
    (skill_dir / "references" / "beta.md").unlink()
    (skill_dir / "references" / "Beta.md").write_text(BETA, encoding="utf-8")
    out = load_join().build(skill_dir)
    assert out.index("\n## Beta scans\n") < out.index("\n## Alpha checks\n")


def test_join_leaves_code_blocks_alone(tmp_path: Path) -> None:
    skill_dir = make_skill(tmp_path)
    fenced = "# Beta scans\n\n```sh\n# offline mode\nosv-scanner -r .\n```\n\n## Two\n"
    (skill_dir / "references" / "beta.md").write_text(fenced, encoding="utf-8")
    out = load_join().build(skill_dir)
    assert "```sh\n# offline mode\nosv-scanner -r .\n```" in out
    assert "\n### Two\n" in out


def test_paste_file_has_no_pointer() -> None:
    assert "references/" not in (ROOT / "paste" / "aschecked-prompt.md").read_text(encoding="utf-8")


# Added in review round 2 (findings J5 and J6), beside the locked tests; the locked tests are unchanged.


def test_join_refuses_a_reference_not_ending_in_lower_case_md(tmp_path: Path) -> None:
    # Windows would join "Gamma.MD" and Linux would leave it out; the build stops on both instead.
    skill_dir = make_skill(tmp_path)
    (skill_dir / "references" / "Gamma.MD").write_text("# Gamma\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Gamma.MD"):
        load_join().build(skill_dir)


def test_join_builds_a_skill_without_references(tmp_path: Path) -> None:
    skill_dir = tmp_path / "skills" / "aschecked"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: demo\ndescription: d\n---\n\n# Demo\n", encoding="utf-8")
    assert load_join().build(skill_dir) == "# Demo\n"


def test_join_leaves_tilde_code_blocks_alone(tmp_path: Path) -> None:
    skill_dir = make_skill(tmp_path)
    fenced = "# Beta scans\n\n~~~~sh\n# offline mode\n```\n~~~\n# still code\n~~~~\n\n## Two\n"
    (skill_dir / "references" / "beta.md").write_text(fenced, encoding="utf-8")
    out = load_join().build(skill_dir)
    assert "~~~~sh\n# offline mode\n```\n~~~\n# still code\n~~~~" in out
    assert "\n### Two\n" in out
