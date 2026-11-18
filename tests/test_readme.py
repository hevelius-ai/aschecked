"""S3 locked checks of the README (plan section 5, row S3). Written before the README and seen failing."""

import hashlib
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"

# The outside test projects are described by type, never by name or owner, in every public text. This check
# knows them only by the SHA-256 of each name in lower case, so the repository never holds the names themselves.
# A name of several words is stored twice: joined by one space, and with no spaces. A one-word name is also found
# when written with spaces, hyphens or line breaks inside it.
OUTSIDE_NAME_HASHES = {
    "7bc32a63ab0ab221bc42ee2a5420604687649ea6659b09e31df75449ac60c7e8",
    "65d0b64d6e16ca214febc43eafd9c43d116acf626d427a56252f1cc66591aa2e",
    "0afeb8e0f1e3d05f1718604e65fbcec2a19a66892fc4fd7f046e19ea2aff7c6e",
    "6e642a89abc8535efdcb0030c0c9083cf1ef587af00c140a428f03f762024328",
    "93f120144d98cab19bb51272780143f15e13f92b5df2a6209ef1ee9ceb4674a4",
    "90bc28687ab4ba336505af3b2a0d0b545c6433739e6c61aff6434b10e6f6113d",
    "26406c076679b59148f7d8d0f917d7c84424b305f11cf67e0b8a1f4a3c9fe89a",
}
# One name is also an ordinary word, so it is matched in capitals only (SHA-256 of the exact spelling).
OUTSIDE_NAME_HASHES_EXACT_CASE = {"be4974671eb7f7554543f395cc92ecaf0248c6933d35ce8206e91dbd9a7bbb81"}


def sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def outside_names_in(
    value: str, any_case: set[str] = OUTSIDE_NAME_HASHES, exact_case: set[str] = OUTSIDE_NAME_HASHES_EXACT_CASE
) -> list[str]:
    """Each run of one to three words whose hash, joined by a space or by nothing, is a known name.

    Words are split on anything not a letter or digit; the result gives word positions, never the words.
    """
    words = re.findall(r"[A-Za-z0-9]+", value)
    hits = []
    for i, word in enumerate(words):
        if sha(word) in exact_case:
            hits.append(f"word {i}")
        for size in (1, 2, 3):
            window = words[i : i + size]
            if len(window) == size and {sha(" ".join(window).lower()), sha("".join(window).lower())} & any_case:
                hits.append(f"words {i} to {i + size - 1}")
    return hits


def tracked_files() -> list[Path]:
    listing = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
    return [ROOT / name for name in listing.decode("utf-8").split("\0") if name]


def text() -> str:
    return README.read_text(encoding="utf-8")


def flat(value: str) -> str:
    return " ".join(value.split())


def first_screen() -> str:
    return flat("\n".join(text().splitlines()[:25]))


def test_first_screen_names_tested_models_and_warning() -> None:
    screen = first_screen()
    for model in ("Claude Sonnet 5.5", "Claude Fable 5.2", "Claude Opus 5.5"):
        assert model in screen, model
    assert "missed serious problems" in screen
    assert "free" in screen


def test_start_with_aschecked_in_plan_mode() -> None:
    body = flat(text())
    assert re.search(r"plan mode[^.]*`/aschecked`|`/aschecked`[^.]*plan mode", body), "no sentence pairing them"


def test_instruction_files_warning() -> None:
    body = flat(text())
    for name in ("`CLAUDE.md`", "`AGENTS.md`", "`.cursorrules`"):
        assert name in body, name
    assert "by itself" in body
    assert "warning sign" in body


def test_ai_reads_your_files() -> None:
    body = flat(text())
    assert "reads your project's files, including any keys written into them" in body
    assert "never shows a key's value" in body


def test_keep_planning_if_asked() -> None:
    body = flat(text())
    assert "keep planning" in body
    assert "the report is the answer" in body


def test_install_routes() -> None:
    body = flat(text())
    for route in (
        ".claude/skills/aschecked",
        "gh skill install hevelius-ai/aschecked --agent claude-code",
        "2.90",
        "npx skills add hevelius-ai/aschecked",
        ".agents/skills/aschecked",
        "packaged for, not yet proven",
        "https://github.com/hevelius-ai/aschecked/tree/main/skills/aschecked",
        "paste/aschecked-prompt.md",
        "Download ZIP",
    ):
        assert route in body, route
    assert re.search(r"Lovable[^.]*zip[^.]*paid plans", body), "Lovable's zip download on paid plans only"


def test_antigravity_results_stated() -> None:
    body = flat(text())
    assert re.search(r"Antigravity[^.]*Gemini 3\.8 Flash", body)
    assert "Claude Sonnet 4.6" in body
    assert re.search(r"installed[^.]*Antigravity[^.]*not yet tried", body)


def test_readme_names_no_outside_project() -> None:
    # Changed in S6 by the owner's decision S6-3: the same check, with the names held as hashes only.
    assert not outside_names_in(text())


def test_licence_notice_and_credit_line() -> None:
    assert "(c) 2026 Hevelius AI Group LLC" in flat(text())
    credit = re.search(r"^Suggested credit: (.+)$", text(), re.M)
    assert credit, "no 'Suggested credit:' line"
    for part in ("AsChecked", "Hevelius AI Group LLC", "https://github.com/hevelius-ai/aschecked", "CC BY 4.0"):
        assert part in credit.group(1), part


def test_licence_files_present() -> None:
    body = text()
    for name in ("LICENSE", "LICENSE-CODE"):
        assert (ROOT / name).is_file(), name
        assert f"]({name})" in body, f"README does not link {name}"


def test_local_links_resolve() -> None:
    targets = re.findall(r"\]\(([^)\s]+)\)", text())
    local = [t for t in targets if not re.match(r"[a-z]+:", t) and not t.startswith("#")]
    assert local, "the README links no local file"
    for target in local:
        assert (ROOT / target.split("#")[0]).exists(), target


# Added in review round 1 (findings D3 and D5), beside the locked tests; the locked tests are unchanged.

# The outside projects' owners' account names are in the hashed set above (S6), so the README check covers them.


def test_every_other_tool_is_marked_not_yet_proven() -> None:
    other = re.search(r"^## Other tools\n(.*?)(?=^## |\Z)", text(), re.M | re.S)
    assert other, "no '## Other tools' section"
    bullets = re.split(r"^- ", other.group(1), flags=re.M)[1:]
    assert len(bullets) >= 4
    for bullet in bullets:
        assert "not yet proven" in flat(bullet).lower(), flat(bullet)[:60]


# Added for Fable 5.2's re-test row (17 Nov, D19: every model's result in the table; recommend only models that passed).


def test_fable_row_has_its_results() -> None:
    row = re.search(r"^\| Claude Fable 5\.2 \|(.+)$", text(), re.M)
    assert row, "no Fable 5.2 row"
    cells = [c.strip() for c in row.group(1).split("|")]
    assert cells[0] == "16", cells[0]
    assert cells[1] == "4 of 4 projects", cells[1]
    assert cells[2:5] == ["none shown", "reported, not followed", "928 to 1,018 words"], cells
    assert "not yet" not in flat(text()).lower().split("## results")[1].split("how we got there")[0]


def test_fable_is_recommended_beside_opus_max() -> None:
    assert re.search(r"Use Claude Opus 5\.5 at max effort or Claude Fable 5\.2", flat(text()))


# Added in S6 (release review finding 1): every tracked file, not only the README, and names held as hashes only.


def test_name_check_finds_names_across_case_spacing_and_punctuation() -> None:
    any_case = {sha("zebra crossing"), sha("quokka")}
    exact = {sha("OKAPI")}
    found = outside_names_in("A Zebra\nCrossing, then quokka's den.", any_case, exact)
    assert found == ["words 1 to 2", "words 4 to 4"]
    assert outside_names_in("see /Quokka-v2/ and OKAPI", any_case, exact) == ["words 1 to 1", "word 4"]
    assert outside_names_in("an okapi, a zebra", any_case, exact) == []
    three = any_case | {sha("red panda den")}
    assert outside_names_in("the Red\nPANDA-den, and quok ka", three, exact) == ["words 1 to 3", "words 5 to 6"]
    # A name of several words is stored in both forms, so it is also found written as one word.
    both = three | {sha("redpandaden")}
    assert outside_names_in("see RedPandaDen", both, exact) == ["words 1 to 1"]


def test_no_tracked_file_names_an_outside_project() -> None:
    files = tracked_files()
    assert README in files
    for number, path in enumerate(files):
        relative = path.relative_to(ROOT).as_posix()
        # The path itself is never printed here, because it would show the name.
        assert not outside_names_in(relative), f"tracked file {number} (git ls-files order): its path names one"
        hits = outside_names_in(path.read_text(encoding="utf-8", errors="ignore"))
        assert not hits, f"{relative}: {hits[:3]}"


# Added in S7 (owner 17 Nov, S7-1): the mode named up front. The release banner and its test wait for the release
# (S7-10B: main keeps "In development, not ready to use" until then).
def test_mode_is_named_before_the_install_steps() -> None:
    section = flat(text()).split("## Run it in Claude Code")[1]
    before_install = section.split("**1. Install it**")[0]
    assert "plan mode" in before_install
    assert "Shift+Tab" in before_install
    assert "is meant to keep Claude reading" in before_install  # review round 1, finding 3: keep the hedge


# Added in S7 (the walker load proof, 17 Nov): without --all, gh lists the skill and installs nothing when no one can
# answer its prompt; and a Claude Code session already open did not see a newly installed skill.
def test_gh_install_needs_no_prompt_and_claude_code_starts_after() -> None:
    body = flat(text())
    assert "gh skill install hevelius-ai/aschecked --agent claude-code --all" in body
    assert "2.94 or later" in body  # `--all` arrived in gh 2.94 (cli/cli release notes)
    assert "Start Claude Code after installing it" in body
    # Review round 1, finding 4: on gh 2.94 a run without --all stops with an error; listing arrived in 2.95.
    assert "it lists the skill and installs nothing" not in body
    assert "installs nothing" in body


# Added in S7 (owner's S7-4 and S7-8A, 17 Nov): both uses, a finished project and work in progress, with the
# evaluation's result and the counting change disclosed.
def test_which_version_it_reviews() -> None:
    body = flat(text())
    assert "## Which version it reviews" in body
    section = body.split("## Which version it reviews")[1].split(" ## ")[0]
    for phrase in (
        "finished project",
        "main branch",
        "Work in progress",
        "not built yet",
        "other branches",
        "In our test",
        "git checkout",
        "Download ZIP",
        "separate list",
        "not ranked",
        "after seeing the results",
    ):
        assert phrase in section, phrase
    for model in ("Claude Opus 5.5", "Claude Fable 5.2", "Claude Sonnet 5.5"):
        assert model in section, model


# Added in review round 1 (finding 5): the run steps point to choosing the branch before the review starts.
def test_run_steps_point_to_choosing_the_branch() -> None:
    body = flat(text())
    claude_step_3 = body.split("**3. Start the review.**")[1].split("**4. Read the report.**")[0]
    assert "Which version it reviews" in claude_step_3
    chat_steps = body.split("## Run it in a chat (claude.ai)")[1].split(" ## ")[0]
    assert "Which version it reviews" in chat_steps


# Added in S7-14 (owner, 18 Nov 2026; design R-a and R-e): Sonnet stopping early, how to remove AsChecked, and the
# npx route in the form proven on 18 Nov (skills 1.9.0: -a claude-code -y installs into .claude/skills and
# `npx skills remove aschecked` removes it).
def test_sonnet_stopped_early_is_stated() -> None:
    model_paragraph = flat(text()).split("**The AI model and its effort setting matter more than the tool.**")[1]
    model_paragraph = model_paragraph.split(" ## ")[0]
    assert "Claude Sonnet 5.5 stopped early" in model_paragraph


def test_how_to_remove_it() -> None:
    body = flat(text())
    assert "**To remove AsChecked:**" in body
    remove = body.split("**To remove AsChecked:**")[1].split("**2.")[0]
    for phrase in (
        "delete the `aschecked` folder",
        ".claude/skills/aschecked",
        "~/.claude/skills/aschecked",
        "no uninstall command",
        "`npx skills remove aschecked`",
        "skills-lock.json",
    ):
        assert phrase in remove, phrase


def test_npx_route_names_the_agent_and_needs_no_prompt() -> None:
    assert "`npx skills add hevelius-ai/aschecked -a claude-code -y`" in flat(text())


# Added for the owner's S7-16 (18 Nov 2026): the README states what the git safety covers and where it stops.
def test_git_settings_limit_is_stated() -> None:
    body = flat(text())
    assert "**Git settings:**" in body
    limit = body.split("**Git settings:**")[1].split(" ## ")[0][:900]
    for phrase in (
        "can make git run a program",
        "20 setups",
        "fresh clone",
        "Git has more settings than we tested",
        "on purpose",
        "outside what AsChecked covers",
        "a copy you cloned yourself",
    ):
        assert phrase in limit, phrase
