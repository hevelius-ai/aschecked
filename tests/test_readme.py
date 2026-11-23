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


# Locked check changed under S7-31 (owner, 23 Nov 2026, "S7-31 all leans"; design DESIGN-S7-31.md, test table):
# the first screen names the recommended models (R5.1 reworded); Sonnet is named on docs/how-we-tested.md.
def test_first_screen_names_tested_models_and_warning() -> None:
    screen = first_screen()
    for model in ("Claude Fable 5.2", "Claude Opus 5.5"):
        assert model in screen, model
    assert "missed serious problems" in screen
    assert "free" in screen
    assert "Claude Sonnet 5.5" in flat(doc("how-we-tested.md"))


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


# Locked check changed under S7-25 A (owner, 22 Nov 2026): this content moved from the README to a docs/ page,
# so the check reads that page (or the README together with it).
def test_install_routes() -> None:
    body = flat(text() + doc("install-options.md") + doc("other-tools.md"))
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


# Locked check changed under S7-25 A (owner, 22 Nov 2026): this content moved from the README to a docs/ page,
# so the check reads that page (or the README together with it).
def test_antigravity_results_stated() -> None:
    body = flat(doc("other-tools.md"))
    assert re.search(r"Antigravity[^.]*Gemini 3\.8 Flash", body)
    assert "Claude Sonnet 4.6" in body
    # Locked S3 check changed under S7-21 B (owner, 19 Nov 2026): the installed v1 skill has now been tried in
    # Antigravity, so the README points to that result instead of saying "not yet tried".
    assert "The installed v1 skill is the one tried in the list above." in body


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


# Locked check changed under S7-25 A (owner, 22 Nov 2026): this content moved from the README to a docs/ page,
# so the check reads that page (or the README together with it).
def test_every_other_tool_is_marked_not_yet_proven() -> None:
    page = doc("other-tools.md").split("\n\n**Antigravity, tried with")[0]
    bullets = re.split(r"^- ", page, flags=re.M)[1:]
    assert len(bullets) >= 4
    for bullet in bullets:
        assert "not yet proven" in flat(bullet).lower(), flat(bullet)[:60]


# Added for the owner's S7-15 B (18 Nov 2026): Replit is marked not tried, because its skills and Plan mode need a
# paid plan, and Replit users are pointed to the chat route.
# Locked check changed under S7-25 A (owner, 22 Nov 2026): this content moved from the README to a docs/ page,
# so the check reads that page (or the README together with it).
def test_replit_marked_not_tried_needs_a_paid_plan() -> None:
    page = doc("other-tools.md").split("\n\n**Antigravity, tried with")[0]
    bullets = [flat(b) for b in re.split(r"^- ", page, flags=re.M)[1:]]
    replit = [b for b in bullets if b.startswith("**Replit:**")]
    assert len(replit) == 1, "no bullet of its own for Replit"
    for phrase in ("not tried (needs a paid plan)", "Plan mode", "Use a claude.ai chat"):  # S7-31: new heading
        assert phrase in replit[0], phrase
    assert not [b for b in bullets if "Replit" in b and not b.startswith("**Replit:**")]


# Locked tests changed under the owner's decision S7-19 (18 Nov 2026, "A, But we can clearly state that the best one
# fable 5.2 on medium"): the Results table is now the S7-18 benchmark, so `test_fable_row_has_its_results` (the
# 15 Nov re-test's Fable row) became `test_s7_19_full_table_has_all_thirteen_settings`, and
# `test_fable_is_recommended_beside_opus_max` (Opus at max beside Fable) became
# `test_s7_19_best_setting_is_named_first_and_in_the_start_command`.


# Locked check changed under S7-25 A (owner, 22 Nov 2026): this content moved from the README to a docs/ page,
# so the check reads that page (or the README together with it).
def results() -> str:
    return flat(doc("how-we-tested.md")).split("## Results of the benchmark")[1].split(" ## ")[0]


def table_rows(section: str) -> list[list[str]]:
    rows = []
    for line in section.splitlines():
        if line.startswith("| ") and not line.startswith("|---"):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows


def results_raw() -> str:
    return doc("how-we-tested.md").split("## Results of the benchmark")[1].split("\n## ")[0]


def test_s7_19_best_setting_is_named_first_and_in_the_start_command() -> None:
    # S7-31 (test table): the banner says "did best" and the table's first row says "(best)".
    screen = first_screen()
    assert "Claude Fable 5.2 at medium effort did best" in screen
    assert "**Claude Fable 5.2, medium (best)**" in flat(text())
    body = flat(text())
    assert "`claude --model fable --effort medium`" in body
    assert "--effort max" not in body
    assert "Use Claude Opus 5.5 at max effort" not in body


def test_s7_19_three_recommended_settings() -> None:
    section = results_raw().split("**Recommended**")[1].split("\n\n")[1]
    rows = table_rows(section)
    assert rows[0][0] == "Setting", rows[0]
    body = rows[1:]
    assert [r[0] for r in body] == [
        "**Claude Fable 5.2, medium (best)**",
        "Claude Opus 5.5, medium",
        "Claude Fable 5.2, low",
    ], body
    assert [r[1:3] for r in body] == [["17, 13, 15", "15.0"], ["15, 15, 14", "14.7"], ["15, 15, 13", "14.3"]], body
    assert [r[3] for r in body] == ["12 of 12", "11 of 12", "12 of 12"], body


THIRTEEN = [
    ("Claude Fable 5.2", ("low", "medium", "high")),
    ("Claude Opus 5.5", ("low", "medium", "high", "extra-high", "max")),
    ("Claude Sonnet 5.5", ("low", "medium", "high", "extra-high", "max")),
]


def test_s7_19_full_table_has_all_thirteen_settings() -> None:
    section = results_raw().split("**All 13 settings**")[1].split("\n\n")[1]
    rows = table_rows(section)[1:]
    names = [r[0] for r in rows]
    expected = [f"{model}, {level}" for model, levels in THIRTEEN for level in levels]
    assert names == expected, names
    scores = {r[0]: r[2] for r in rows}
    assert scores["Claude Fable 5.2, medium"] == "15.0 (17, 13, 15)"
    assert scores["Claude Opus 5.5, max"] == "15"
    assert scores["Claude Sonnet 5.5, low"] == "4"


def test_s7_19_higher_effort_is_stated_as_not_better() -> None:
    body = results()
    assert "high, extra-high and max" in body
    assert "did not find more" in body
    assert "Fable 5.2 extra-high and max were not run" in body
    # S7-25: the model paragraph moved to docs/how-we-tested.md (S7-31: the README's effort line moved there too).
    assert "took about seven times longer at most" in flat(doc("how-we-tested.md"))
    # S7-31 (test table): the effort line moved to docs/how-we-tested.md, limited to the two models it holds for.
    assert "**More effort did not find more** with Claude Fable 5.2 or Claude Opus 5.5" in flat(doc("how-we-tested.md"))
    assert "more effort than medium" not in flat(text())


def test_s7_19_how_we_tested_is_stated() -> None:
    body = results()
    for phrase in (
        "19 problems",
        "three times",
        "scored blind",
        "fixed before the first run",
        "API prices",
        "one sample",
    ):
        assert phrase in body, phrase


def test_s7_19_safety_checks_for_the_best_setting() -> None:
    body = results()
    for phrase in ("none shown", "reported, not followed", "work-in-progress list", "unmerged branch"):
        assert phrase in body, phrase


def test_s7_19_no_default_effort_wording() -> None:
    # Review round 1 (MEDIUM 5): any "default", not only "default effort" (the owner rejected "Fable default").
    assert not re.search(r"\bdefault\b", flat(text()), re.I)


# Review round 1 of PR #4 (MEDIUM 1 to 4): no claim about Fable settings that were not run, the 1,200 words named as
# the benchmark's cap (the method asks for 900), the Opus extra-high median, and the tie for the best score stated.
def test_s7_19_fable_extra_high_and_max_not_claimed() -> None:
    # S7-25: the model paragraph moved from the first screen to docs/how-we-tested.md.
    page = flat(doc("how-we-tested.md"))
    assert "With Claude Fable 5.2 and Claude Opus 5.5" not in page + flat(text())
    assert "(extra-high and max were not run)" in page


def test_s7_19_word_cap_is_the_benchmarks_not_the_methods() -> None:
    body = flat(text())
    assert "method's limit of 1,200" not in body
    assert "the benchmark's 1,200-word cap" in results()
    assert "at most 900 words" in results()


def test_s7_19_opus_extra_high_median_minutes() -> None:
    section = results_raw().split("**All 13 settings**")[1].split("\n\n")[1]
    rows = {r[0]: r for r in table_rows(section)[1:]}
    assert rows["Claude Opus 5.5, extra-high"][5] == "7"
    assert "about four and a half times" in results()


def test_s7_19_tie_for_best_is_stated() -> None:
    assert "Claude Fable 5.2 at high effort tied it at 17" in results()


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


# Added in S7 (owner 17 Nov, S7-1): the mode named up front. The release banner's test is in tests/test_repo.py (S7-9).
def test_mode_is_named_before_the_install_steps() -> None:
    # S7-31 (test table): the new headings; the plan-mode line is in "How it works", before "Install it (once)".
    before_install = flat(text()).split("## Install it (once)")[0]
    assert "plan mode" in before_install
    assert "Shift+Tab" in before_install
    assert "is meant to keep Claude reading" in before_install  # review round 1, finding 3: keep the hedge


# Added in S7 (the walker load proof, 17 Nov): without --all, gh lists the skill and installs nothing when no one can
# answer its prompt; and a Claude Code session already open did not see a newly installed skill.
# Locked check changed under S7-25 A (owner, 22 Nov 2026): this content moved from the README to a docs/ page,
# so the check reads that page (or the README together with it).
def test_gh_install_needs_no_prompt_and_claude_code_starts_after() -> None:
    body = flat(text() + doc("install-options.md") + doc("other-tools.md"))
    assert "gh skill install hevelius-ai/aschecked --agent claude-code --all" in body
    assert "2.94 or later" in body  # `--all` arrived in gh 2.94 (cli/cli release notes)
    assert "Start Claude Code after installing it" in body
    # Review round 1, finding 4: on gh 2.94 a run without --all stops with an error; listing arrived in 2.95.
    assert "it lists the skill and installs nothing" not in body
    assert "installs nothing" in body


# Added in S7 (owner's S7-4 and S7-8A, 17 Nov): both uses, a finished project and work in progress, with the
# evaluation's result and the counting change disclosed.
def test_which_version_it_reviews() -> None:
    # S7-31 (test table): the section became review step 2 and the unfinished-work sentence in review step 7 and
    # chat step 5 (R6.1); "may look at your other branches" moved to docs/git-safety.md. The docs half is unchanged.
    run = flat(part("Run a review"))
    for phrase in ("finished app", "`git checkout main`", "another branch", "not built yet", "separately"):
        assert phrase in run, phrase
    chat = flat(part("No Claude Code? Use a claude.ai chat"))
    for phrase in ("**Download ZIP**", "choose it first", "not built yet", "separately"):
        assert phrase in chat, phrase
    assert "may look at your other branches for unmerged work" in flat(doc("git-safety.md"))
    # S7-25: the test result and the counting change moved to docs/how-we-tested.md, linked from the README.
    tested = flat(doc("how-we-tested.md")).split("## The work-in-progress test")[1].split(" ## ")[0]
    for phrase in ("In our test", "separate list", "after seeing the results"):
        assert phrase in tested, phrase
    for model in ("Claude Opus 5.5", "Claude Fable 5.2", "Claude Sonnet 5.5"):
        assert model in tested, model


# Added in review round 1 (finding 5): the run steps point to choosing the branch before the review starts.
# Locked check changed under S7-31 (owner, 23 Nov 2026, "S7-31 all leans"; design DESIGN-S7-31.md, test table):
# the steps no longer point to a section; choosing the version is review step 2 itself
# (test_s7_31_review_steps), and nothing in the README points to another part of it (test_s7_31_no_cross_references).
def test_run_steps_point_to_choosing_the_branch() -> None:
    step = re.split(r"^\d+\. ", part("Run a review"), flags=re.M)[2]  # S7-31 walkthrough w5 (F1): step 2
    assert step.startswith("**Choose the version.**")
    assert "Which version it reviews" not in text()


# Added in S7-14 (owner, 18 Nov 2026; design R-a and R-e): Sonnet stopping early, how to remove AsChecked, and the
# npx route in the form proven on 18 Nov (skills 1.9.0: -a claude-code -y installs into .claude/skills and
# `npx skills remove aschecked` removes it).
# Locked check changed under S7-25 A (owner, 22 Nov 2026): this content moved from the README to a docs/ page,
# so the check reads that page (or the README together with it).
def test_sonnet_stopped_early_is_stated() -> None:
    model_paragraph = flat(doc("how-we-tested.md")).split(
        "**The AI model and its effort setting matter more than the tool.**"
    )[1]
    model_paragraph = model_paragraph.split(" ## ")[0]
    assert "Claude Sonnet 5.5 stopped early" in model_paragraph


# Locked check changed under S7-25 A (owner, 22 Nov 2026): this content moved from the README to a docs/ page,
# so the check reads that page (or the README together with it).
def test_how_to_remove_it() -> None:
    body = flat(doc("install-options.md"))
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
    assert "`npx skills add hevelius-ai/aschecked -a claude-code -y`" in flat(doc("install-options.md"))  # S7-25


# Added for the owner's S7-16 (18 Nov 2026): the README states what the git safety covers and where it stops.
# The count was first written as 20; the bench has 19 setups (corrected after the reviewer's re-check).
# Locked check changed under S7-25 A (owner, 22 Nov 2026): this content moved from the README to a docs/ page,
# so the check reads that page (or the README together with it).
def test_git_settings_limit_is_stated() -> None:
    body = flat(doc("git-safety.md"))
    assert "**Git settings:**" in body
    limit = body.split("**Git settings:**")[1].split(" ## ")[0][:900]
    for phrase in (
        "can make git run a program",
        "19 setups",
        "fresh clone",
        "Git has more settings than we tested",
        "on purpose",
        "outside what AsChecked covers",
        "a copy you cloned yourself",
    ):
        assert phrase in limit, phrase


# Added for the owner's S7-20 6A (18 Nov 2026): three moments where the walkthrough's first-time users hesitated
# (run w2, LOW findings) each get one sentence in the README.
def between(body: str, start: str, end: str) -> str:
    assert start in body, start
    rest = body.split(start, 1)[1]
    assert end in rest, end
    return rest.split(end, 1)[0]


# Round 1 review (MEDIUM): the files' place must be right for both scopes, and the warning must not read as
# belonging to the case where nothing is installed.
# Locked check changed under S7-25 A (owner, 22 Nov 2026): this content moved from the README to a docs/ page,
# so the check reads that page (or the README together with it).
def test_s7_20_gh_install_warning_is_explained() -> None:
    route = between(flat(doc("install-options.md")), "**With the GitHub CLI**", "**With the skills command**")
    for phrase in (
        "When it installs, it warns that skills are not verified by GitHub",
        "review the installed files",
        "every skill",
        "your project's `.claude/skills/aschecked` folder",
        "with `--scope user`, in `~/.claude/skills/aschecked` in your home folder",
    ):
        assert phrase in route, phrase


def test_s7_20_says_where_to_save_the_report() -> None:
    # S7-31 (test table): review step 10, "Save the report".
    step = between(flat(text()), "10. **Save the report.**", "11. **Fix what it found.**")
    assert "paste it into a text file outside your project's folder" in step


def test_s7_20_says_how_to_download_the_prompt_file() -> None:
    chat = between(flat(text()), "## No Claude Code? Use a claude.ai chat", "## More")  # S7-31: new headings
    assert "**Download raw file**" in chat


# Added for the owner's S7-21 B (19 to 22 Nov 2026): Codex, Cursor, Antigravity, Lovable and Bolt were each tried once
# with the v1 skill on our own test projects (scores: independent scorer, records S7-21-SCORES). "Worked" needs the
# required report form, no file changed and the most serious known problem found; nothing is called proven.
# Locked check changed under S7-25 A (owner, 22 Nov 2026): this content moved from the README to a docs/ page,
# so the check reads that page (or the README together with it).
def other_tools() -> str:
    return flat(doc("other-tools.md")).split("[README](../README.md).", 1)[1]


def bullet(name: str) -> str:
    section = other_tools()
    start = f"- **{name}"
    assert start in section, start
    return section.split(start, 1)[1].split(" - **", 1)[0]


def test_s7_21_how_the_tools_were_tried_is_stated() -> None:
    section = other_tools()
    for phrase in (
        "tried it once",
        "our own small test projects",
        "met all our report checks (every required part, and evidence that matches the files)",
        "changed no file",
        "most serious known problem",
        "One try is not proof",
    ):
        assert phrase in section, phrase


# Round 1 review (MEDIUM): the labels follow the printed rule, Lovable is not called worked (no file check and no
# answer key there), the steps are the steps tried, and each claim is pinned so a wrong README fails.
def test_s7_21_each_tried_tool_names_its_result() -> None:
    for name in ("Codex", "Cursor", "Antigravity", "Bolt"):
        assert "Tried, not working" in bullet(name), name
        assert "worked" not in bullet(name), name
    lovable = bullet("Lovable")
    assert "Tried once, not fully checked" in lovable and "worked" not in lovable
    assert "whether the review changed no file, and how well it finds problems, were not checked there" in lovable


def test_s7_21_models_and_modes_tried_are_named() -> None:
    codex = bullet("Codex")
    for phrase in (
        "GPT-6-Luna at medium effort, on two test projects",
        "`codex --sandbox read-only`",
        "approve each command that only reads",
        "non-admin sandbox",
    ):
        assert phrase in codex, phrase
    cursor = bullet("Cursor")
    for phrase in ("free plan, Auto model, on two test projects", "**Ask** mode", "only wrote a plan"):
        assert phrase in cursor, phrase
    antigravity = bullet("Antigravity")
    for phrase in (
        "Claude Opus 4.6 Thinking",
        "on one test project",
        "start it in plan mode",
        "approve each command that only reads",
        "unattended mode stops at the first command",
    ):
        assert phrase in antigravity, phrase
    assert "**Chat** mode" in bullet("Lovable")
    assert "**Plan** mode" in bullet("Bolt")
    for name in ("Lovable", "Bolt"):
        assert 'send "Run the aschecked skill on this project."' in bullet(name), name


def test_s7_21_what_fell_short_is_stated() -> None:
    for name in ("Codex", "Cursor"):
        assert "both reviews (one on each project) found the most serious problem" in bullet(name), name
    assert "two lines away" in bullet("Codex")
    assert "no effort for any fix" in bullet("Cursor")
    assert "found the most serious problem but ranked it second" in bullet("Antigravity")
    bolt = bullet("Bolt")
    for phrase in (
        "reassuring summary after the report's closing lines",
        "skill's own instructions as project text",
        "new version to the project's history",
    ):
        assert phrase in bolt, phrase


def test_s7_21_import_paths_for_the_builders() -> None:
    lovable = bullet("Lovable")
    for phrase in (
        "Personal skills",
        "**Import skills**",
        "https://github.com/hevelius-ai/aschecked/tree/main/skills/aschecked",
    ):
        assert phrase in lovable, phrase
    bolt = bullet("Bolt")
    for phrase in ("**Skills**", "**From GitHub**", "`https://github.com/hevelius-ai/aschecked`"):
        assert phrase in bolt, phrase


def test_s7_21_untried_tools_say_so() -> None:
    assert "Not tried (each needs an install and a sign-in)" in bullet("Devin Desktop, Kilo")
    assert "Not tried (needs an install and a sign-in)" in bullet("Cline")


def test_s7_21_nothing_is_called_proven() -> None:
    section = other_tools().lower()
    assert not re.search(r"(?<!not yet )\bproven\b", section.replace("not yet proven", ""))


# Added for the owner's S7-25 A (22 Nov 2026): the README is one simple screen for people who build with AI and do not
# code; the technical detail moves to pages in docs/ that the README links. Safety lines stay in the README.
DOCS = ROOT / "docs"
DOC_PAGES = ("how-we-tested.md", "other-tools.md", "install-options.md", "git-safety.md")


def doc(name: str) -> str:
    return (DOCS / name).read_text(encoding="utf-8")


def test_s7_25_readme_is_short() -> None:
    words = len(text().split())
    assert words <= 1300, f"README has {words} words; the cap is 1,300"  # S7-33 (owner, 23 Nov 2026): was 900


def test_s7_25_docs_pages_exist_and_the_readme_links_each() -> None:
    for name in DOC_PAGES:
        assert (DOCS / name).is_file(), name
        assert f"(docs/{name})" in text(), f"README does not link docs/{name}"


def test_s7_25_safety_lines_stay_in_the_readme() -> None:
    body = flat(text())
    for phrase in (
        "plan mode",
        "keep planning",
        "warning sign",
        "including any keys",
        "not an audit",
        # S7-25 review round 1 (HIGH and MEDIUM): the mode warning and the D6 limit stay in the README.
        "Do not start the review in auto-accept or bypass-permissions mode",
        "cannot stop your tool from loading the file",
    ):
        assert phrase in body, phrase
    assert re.search(r"never (says|tells you)[^.]*safe", body), "never says a project is safe"


def test_s7_25_links_in_the_docs_pages_resolve() -> None:
    for name in DOC_PAGES:
        targets = re.findall(r"\]\(([^)\s]+)\)", doc(name))
        local = [t for t in targets if not re.match(r"[a-z]+:", t) and not t.startswith("#")]
        assert "../README.md" in local, f"{name} does not link back to the README"
        for target in local:
            assert (DOCS / target.split("#")[0]).resolve().exists(), f"{name}: {target}"
    assert "## A zip of your project" in doc("install-options.md")  # kept for links into it (S7-31: not the README)


# S7-25 review round 1 (MEDIUM): the sandbox results, the missed pass mark and the stated limits are guarded.
def test_s7_26_sandbox_results_and_limits_are_stated() -> None:
    page = flat(doc("how-we-tested.md"))
    assert "## Sandbox test of the released version" in page
    sandbox = page.split("## Sandbox test of the released version")[1]
    for phrase in (
        "18 of 18",
        "20 of 24",
        "at least 22 of 24",
        "We fixed the pass marks before the runs",
        "planted problems are easier to find than real ones",
        "we wrote the apps ourselves",
        "With their own checks",
        "Without",
        "the benchmark above remain the main evidence",
    ):
        assert phrase in sandbox, phrase
    assert "did not cause it" not in sandbox


def test_s7_25_moved_sentences_kept() -> None:
    assert "`CLAUDE_CODE_EFFORT_LEVEL`" in flat(doc("install-options.md"))
    assert "on this page, click" not in flat(doc("install-options.md"))
    page = flat(doc("how-we-tested.md"))
    assert "Benchmark of this version" not in page and "this version of the method" not in page


def test_s7_29_final_sandbox_round_is_stated() -> None:
    # S7-29 (owner, 22 Nov 2026): the final round's result is stated whatever it is, with the strict reading.
    # Review round 1 on the page (HIGH 1, MEDIUM 2 to 4): one re-score of all versions, the strict count with every
    # close call, the round-by-round figures, the limits, each tied to its own sentence or row.
    sandbox = flat(doc("how-we-tested.md")).split("## Sandbox test of the released version")[1]
    for phrase in (
        "| Claude Code, released version (24) | 18 of 18, always as finding 1 | 2.8 | 24 of 24 | 6 of 6 | 3 of 3 |",
        "| Claude Code, second version (24) | 18 of 18, 17 as finding 1 | 2.8 | 22 of 24 |",
        "| Claude Code, first version with the plain-words rule (24) | 18 of 18, always as finding 1 | 2.8 "
        "| 20 of 24 |",
        "| Claude Code, earlier version (8) | 6 of 6 | 2.8 | 6 of 8 |",
        "one scorer per app judged all 80 Claude Code reports together",
        "The released version met every pass mark",
        "Scored round by round, by new scorers each time, the three versions came to 20, 21 and 23 of 24",
        # Page review round 2 (HIGH 1): close calls a scorer wrote for all of an app's reports count too.
        "Counting every close call on the report checks as a fail, including those a scorer wrote for all of an app's",
        "no report of the three versions with the plain-words rule passes, and 1 of the earlier version's 8 does",
        "a search result the scorer judged wrong",
        "were not shown the exact wording of the three closing lines",
        "no cited line opened again near the end",
        "Codex and Cursor ran once per app, on the first version, and were scored only in the first round",
        "so the last round is not a fresh test of them",
    ):
        assert phrase in sandbox, phrase
    assert "every one of its 24 runs opened the cited lines again" not in sandbox
    assert "checked from memory" not in sandbox


# S7-31 (owner, 23 Nov 2026, "S7-31 all leans"; S7-33 the 1,300-word cap; design DESIGN-S7-31.md version 3, reviewed
# in three rounds): the README as numbered steps for people who build with AI and do not code, with nothing that sends
# the reader to another part of it, an install by one pasted prompt, and only the three best settings. Written before
# the README and seen failing.
S7_31_HEADINGS = [
    "What you get",
    "How it works",
    "What you need in Claude Code",
    "Install it (once)",
    "Run a review",
    "No Claude Code? Use a claude.ai chat",
    "More",
    "Licence",
]


def part(heading: str) -> str:
    return text().split(f"\n## {heading}\n", 1)[1].split("\n## ", 1)[0]


def items(section: str) -> list[str]:
    return [flat(item) for item in re.split(r"^\d+\. ", section, flags=re.M)[1:]]


def fenced_prompt(page: str) -> str:
    blocks = re.findall(r"```\n(.*?)```", page, re.S)
    assert len(blocks) == 1, f"{len(blocks)} fenced blocks"
    return flat(blocks[0])


def test_s7_31_readme_parts_in_order() -> None:
    assert re.findall(r"^## (.+)$", text(), re.M) == S7_31_HEADINGS


def test_s7_31_no_cross_references() -> None:
    body = flat(text()).lower()
    for phrase in ('see "', "section", "](#", "the same again", "the table"):
        assert phrase not in body, phrase
    # S7-31 PR review round 1 (M2): the words on their own, steps by number or in words, and heading names quoted.
    assert not re.search(r"\b(above|below|earlier|later on)\b", body)
    numbers = r"(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven)"
    assert not re.search(rf"\bsteps? {numbers}\b", body)
    for heading in S7_31_HEADINGS:
        assert f'"{heading.lower()}"' not in body, heading
    for link in re.findall(r"\]\(([^)]+)\)", text()):
        assert link.startswith(("docs/", "paste/", "https://")) or link in ("LICENSE", "LICENSE-CODE"), link


def test_s7_31_first_screen() -> None:
    screen = flat(text().split("\n## ")[0])
    for phrase in ("Claude Fable 5.2", "Claude Opus 5.5", "weaker or free models missed serious problems"):
        assert phrase in screen, phrase


INSTALL_PROMPT = (
    "https://github.com/hevelius-ai/aschecked/archive/refs/tags/v1.0.0.zip",
    "into this folder and unpack it here",
    "tell me in two sentences what they do",
    "wait for my yes",
    "copy that folder to .claude/skills/aschecked in my home folder",
    "replacing any older copy",
    "delete what you downloaded and unpacked",
    "Change nothing else.",
    '"AsChecked is installed"',
    ".claude/skills/aschecked/SKILL.md is in my home folder",  # S7-31 PR review round 1 (L4)
)


def test_s7_31_install_is_a_pasted_prompt() -> None:
    install = part("Install it (once)")
    steps = items(install)
    assert len(steps) == 7, len(steps)
    prompt = fenced_prompt(install)
    for phrase in INSTALL_PROMPT:
        assert phrase in prompt, phrase
    body = flat(install)
    for phrase in (
        "new, empty folder (not your project)",
        "Open in Terminal",
        "New Terminal at Folder",
        "Type `claude`",  # corrected before review: the step starts a sentence
        "Type `yes`",
        "`.claude/skills/aschecked`",
        'the plain **Yes**, not "don\'t ask again"',
        "delete what it downloaded",
        "choose **No**",
        "`/exit`",
        "paste the message from this page again",
        "it always names the newest version",  # S7-31 PR review round 1 (L4)
    ):
        assert phrase in body, phrase
    # S7-31 PR review round 1 (M1): each approval step says the plain Yes itself, and step 5 the folder to check.
    plain_yes = 'the plain **Yes**, not "don\'t ask again"'
    assert plain_yes in steps[2] and "otherwise **No**" in steps[2], steps[2]
    assert plain_yes in steps[4] and "Check that it names `.claude/skills/aschecked`" in steps[4], steps[4]
    assert "the plain **Yes**" in steps[5] and "delete what it downloaded" in steps[5], steps[5]
    assert "anything else, choose **No**" in steps[5], steps[5]
    # S7-31 PR review round 1 (M5), from the owner's notes: Claude Code asks to trust the folder on first start,
    # and Windows shows the path with backslashes.
    assert "trust this folder, choose **Yes**" in steps[0], steps[0]
    assert r"`.claude\skills\aschecked`" in steps[4], steps[4]
    assert not re.search(r"\b(gh|npx)\b", text())
    assert fenced_prompt(doc("install-options.md")) == prompt


def test_s7_31_three_settings_only() -> None:
    lines = [line for line in part("What you need in Claude Code").splitlines() if line.startswith("|")]
    rows = [[cell.strip() for cell in line.strip("|").split("|")] for line in lines]
    assert rows[2:] == [
        ["**Claude Fable 5.2, medium (best)**", "`claude --model fable --effort medium`"],
        ["Claude Opus 5.5, medium", "`claude --model opus --effort medium`"],
        ["Claude Fable 5.2, low", "`claude --model fable --effort low`"],
    ], rows
    assert "Sonnet" not in text()
    assert "https://code.claude.com/docs/en/setup" in part("What you need in Claude Code")


REVIEW_STEPS = [
    ("**Open a terminal in your project's folder.**", "Open in Terminal", "New Terminal at Folder"),
    # S7-31 walkthrough w5 (F1, MEDIUM): choose the version first, then check that version's instruction files.
    ("**Choose the version.**", "`git checkout main`", "another branch"),
    (
        "**Check your instruction files.**",
        "`CLAUDE.md`",
        "`AGENTS.md`",
        "`.cursorrules`",
        "warning sign",
        "AsChecked reports such text, but it cannot stop your tool from loading the file",
    ),
    ("**Start Claude Code.**", "`claude --model fable --effort medium`", "`claude --model opus --effort medium`"),
    (
        "**Switch on plan mode.**",
        "Shift+Tab",
        "plan mode",
        "Do not start the review in auto-accept or bypass-permissions mode",
    ),
    ("plan mode", "`/aschecked`"),
    ("**Answer the three questions**", '"skip"', "not built yet", "separately"),
    ("**Approve only reading.**", 'the plain **Yes**, not "don\'t ask again"', "only reads", "choose **No**"),
    ("**Keep planning.**", "choose to keep planning", "approving would let it start changing your project"),
    ("**Save the report.**", "outside your project's folder"),
    ("**Fix what it found.**", '"Paste to your AI builder"', "without plan mode"),
]


def test_s7_31_review_steps() -> None:
    steps = items(part("Run a review"))
    assert len(steps) == len(REVIEW_STEPS), len(steps)
    for number, (step, phrases) in enumerate(zip(steps, REVIEW_STEPS, strict=True), 1):
        for phrase in phrases:
            assert phrase in step, (number, phrase)
    assert "trust this folder, choose **Yes**" in steps[3], steps[3]  # S7-31 PR review round 1 (M5)


CHAT_STEPS = [
    ("**Download your project as a zip.**", "**Download ZIP**", "choose it first"),
    ("[`paste/aschecked-prompt.md`](paste/aschecked-prompt.md)", "**Download raw file**"),
    ("Claude Fable 5.2", "Claude Opus 5.5", "medium effort if offered"),
    ("**Upload both files**", '"Run the AsChecked review in the attached prompt file on the attached project."'),
    ("**Answer the three questions**", '"skip"', "not built yet", "separately"),
    ("**Save the report**", '"Paste to your AI builder"'),
]


def test_s7_31_chat_steps() -> None:
    chat = part("No Claude Code? Use a claude.ai chat")
    assert "You need a claude.ai account." in chat
    steps = items(chat)
    assert len(steps) == len(CHAT_STEPS), len(steps)
    for number, (step, phrases) in enumerate(zip(steps, CHAT_STEPS, strict=True), 1):
        for phrase in phrases:
            assert phrase in step, (number, phrase)
    assert "a chat is not yet proven to reach the same results" in flat(chat)
