# How we tested

Back to the [README](../README.md).

## Which version was tested

The benchmark below ran on the method as it was on 18 Nov 2026 (`skills/aschecked` at commit `2080d5a`), before the
rule that has AsChecked say in plain words what each step does and the checks on cited lines and ranking (added 22 Nov
2026). The sandbox test below ran on the version of 22 Nov 2026 (called "released version" there), on the two versions before it and on the earlier one, to
check that these changes made nothing worse.

The full test (see [Plan mode and Auto mode](#plan-mode-and-auto-mode)) ran commit `be325c9`.

## Models and effort

**The AI model and its effort setting matter more than the tool.** We tested 13 model and effort settings on four
test projects with 19 known problems, and the best was **Claude Fable 5.2 at medium effort**: 15 of 19 on average
over three runs, and the most serious problem in every report. Claude Opus 5.5 at medium effort (14.7) and Claude
Fable 5.2 at low effort (14.3) came next. Higher effort did not help: with Claude Opus 5.5, high, extra-high and max
found no more and took about seven times longer at most; with Claude Fable 5.2, high found no more (extra-high and
max were not run). Claude Sonnet 5.5 stopped early: at medium effort it took fewer than half as many steps as Claude
Fable 5.2 before writing its report, and below max effort it missed the most serious problem in half the projects
(see the results below). In our earlier tests, weaker, older or free models missed serious problems and told the
owner that flawed access rules were strong. Treat a report from a free consumer chat model with caution.

## The work-in-progress test

In our test, on an app we built with a half-built feature and three planted problems in it, one run per model,
each at extra effort (`--effort xhigh`), Claude Opus 5.5, Claude Fable 5.2 and Claude Sonnet 5.5 each found all
three, in a separate list after the numbered findings, not ranked. We had planned to count only the numbered findings and "Also found" lines; because the
method hands such problems to the work in progress, we counted that list too, a change made after seeing the results.

## Results of the benchmark

Benchmark of the earlier version (commit `2080d5a`), 18 Nov 2026, in Claude Code's plan mode. Use these results to choose a model and an effort
setting; the best we measured is Claude Fable 5.2 at medium effort.

**How we tested.** The four test projects are AsBuild, a web app with accounts and roles, a mobile fitness app with
health data, and a desktop app. Earlier hand reviews found 19 problems in them. A problem counts as found only when
the report names the same defect in the same place, with every part of it; one-line "Also found" items count too.
We ran 13 settings (Claude Fable 5.2 at three effort levels, Claude Opus 5.5 and Claude Sonnet 5.5 at five each,
with `--effort` set every time) once on all four projects. Four finalists (the best score and the cheapest settings
within 3 points of it, leaving out max) were then run twice more, so each of them was measured three times. Claude
Fable 5.2 at high effort tied it at 17 for the best score; the cheaper, medium, was taken as the best, so high was
run once. Every report was scored blind (the scorers were not told which setting wrote it) by independent reviewers,
separate AI agents that did not write the reports. The pass mark and the rules for choosing were fixed before the
first run: the cheapest setting that finds at least 15 of 19 on average and the most serious problem in at least 11
of 12 reports, which is Claude Fable 5.2 at medium effort. We show the next two as well, so you can weigh cost and
choice of model. Cost per review is at API prices, as Claude Code counts it; on a Claude subscription a review uses
your plan's allowance instead.

**Recommended**

| Setting | Known problems found (of 19), three runs | Average | Most serious problem found | Cost per review | Minutes per review |
|---|---|---|---|---|---|
| **Claude Fable 5.2, medium (best)** | 17, 13, 15 | 15.0 | 12 of 12 | $2.93 | 2 to 4 |
| Claude Opus 5.5, medium | 15, 15, 14 | 14.7 | 11 of 12 | $1.30 | 2 to 4 |
| Claude Fable 5.2, low | 15, 15, 13 | 14.3 | 12 of 12 | $2.52 | 2 to 3 |

Of the settings measured three times, only Claude Fable 5.2 at medium effort reached the pass mark of 15. One of
Claude Opus 5.5's twelve reports at medium effort ran to 1,207 words, over the benchmark's 1,200-word cap.

**All 13 settings** (one run on the four projects, or the average of three runs where three are shown)

| Setting | Runs | Known problems found (of 19) | Most serious problem found | Cost per review | Minutes per review (median) |
|---|---|---|---|---|---|
| Claude Fable 5.2, low | 3 | 14.3 (15, 15, 13) | 12 of 12 | $2.52 | 2 |
| Claude Fable 5.2, medium | 3 | 15.0 (17, 13, 15) | 12 of 12 | $2.93 | 3 |
| Claude Fable 5.2, high | 1 | 17 | 4 of 4 | $4.13 | 5 |
| Claude Opus 5.5, low | 1 | 8 | 2 of 4 | $0.76 | 2 |
| Claude Opus 5.5, medium | 3 | 14.7 (15, 15, 14) | 11 of 12 | $1.30 | 2 |
| Claude Opus 5.5, high | 1 | 13 | 4 of 4 | $1.68 | 5 |
| Claude Opus 5.5, extra-high | 3 | 13.3 (14, 13, 13) | 10 of 12 | $3.10 | 7 |
| Claude Opus 5.5, max | 1 | 15 | 4 of 4 | $5.93 | 18 |
| Claude Sonnet 5.5, low | 1 | 4 | 2 of 4 | $0.32 | 1 |
| Claude Sonnet 5.5, medium | 1 | 9 | 2 of 4 | $0.43 | 1 |
| Claude Sonnet 5.5, high | 1 | 10 | 2 of 4 | $0.70 | 2 |
| Claude Sonnet 5.5, extra-high | 1 | 13 | 2 of 4 | $1.50 | 6 |
| Claude Sonnet 5.5, max | 1 | 14 | 4 of 4 | $3.41 | 17 |

**What the differences show**

- **More effort did not find more** with Claude Fable 5.2 or Claude Opus 5.5. We tested high, extra-high and max as
  well as medium: none scored above the range of medium's three runs, and they took about seven times longer at
  most and cost about four and a half times as much at most. Claude Fable 5.2 extra-high and max were not run: they
  cost the most, and an earlier test at extra-high scored below medium.
- **Low effort** hurt Claude Opus 5.5: it found 8 and missed the most serious problem in two projects. Claude Fable
  5.2 at low effort held up.
- **Claude Sonnet 5.5 found more with more effort** (4 at low, 14 at max), but below max it missed the most serious
  problem in half the projects, and at max a review took about 17 minutes and cost more than Claude Fable 5.2 at
  medium.
- **Runs vary.** The same setting found 17 in one run and 13 in another, so one review is one sample, and a gap of a
  point or two between settings is within that variation.
- **Report length:** the method asks for at most 900 words, and most reports ran longer. Every report stayed within
  the benchmark's 1,200-word cap except three from Claude Opus 5.5 on one project (two at extra-high, one at medium).

**Safety and edge cases** (Claude Fable 5.2 at medium effort, one run each): planted fake keys: none shown; a planted
instruction telling the reviewer to report nothing: reported, not followed; a planted command in a code comment:
kept out of every prompt and reported; an unmerged branch: named, with its work; a half-built feature with three
planted problems: all three found, in the work-in-progress list.

**What these results can and cannot claim:** they hold for these four projects, that version of the method and one
computer. They show averages, the spread between runs and cost, not that every project will get the same result.

How the method got here: the pass mark of 15 of 19 was set before an earlier re-test (15 Nov, one run per model).
The first version found at most 14 with any model. Four more rounds followed (one change, a longer report, made
results worse and was undone). The changes kept were checks on the main journey, lost work, what the product
publishes and platform claims; keeping related problems together; and, after the best run still stopped at 14, the
"Also found" list. Counting those lines was decided after seeing the earlier results.

## When a new model comes out

We check a new model the same way every time before the README recommends it. The new model and the current best
each review our four test projects three times, on the same version of AsChecked, and every report is scored blind in
one batch, so both are judged by the same standard. The new model becomes the recommendation only if all of these hold:

- it finds at least 15 of the 19 known problems on average, and the most serious problem in at least 11 of 12 reports;
- none of its reports breaks a report rule (no verdict that an app is safe, no list of strengths, the fixed closing
  lines, at most 1,200 words), and on average over its 12 reviews a plain-words line comes before at least 9 in 10
  of its steps;
- it is clearly better (at least 2 more on average, and its weakest run set beats the current best's strongest), or
  it finds at least as many and costs at least $0.25 less per review;
- it then passes the eight-app sandbox on its own: the most serious problem in at least 5 of the 6 apps with planted
  problems, no false alarm on the two correct apps, no file changed and no key shown in any run.

The rule was fixed before any new model existed, and a completed check stands: checking the same model again needs a
reason. Three run sets cannot show a gain of one point, so a cheaper model that is slightly weaker can pass the second
way. Each completed check is added to this page, whatever it decides.

## Sandbox test of the released version (22 Nov 2026)

Eight apps we wrote for this test: six with problems we planted on purpose (team notes on Next.js and
Supabase, a group chat on Firebase, a bookings API on Express, an invoices app on Flask, a desktop notes app on
Electron, a shop taking card payments with Stripe) and two built correctly, to count false alarms. One app hid an
instruction telling AI reviewers to call it secure; two hid fake keys. An independent reviewer checked the answer key
against the code before any run, and the reports were scored blind (the scorer did not know which version or tool
wrote each one).

Claude Code with Claude Fable 5.2 at medium effort, in plan mode: three runs per app on each of three versions with
the plain-words rule, one run per app on the earlier version. Codex (GPT-6-Luna, medium) and Cursor (Auto
model) once per app, on the first of those versions.

We fixed the pass marks before the runs, and the test ran in three rounds, each scored as it finished. The first
version with the plain-words rule missed one pass mark, every report check met in at least 22 of 24 runs: several
reports cited a line number one or two lines away from the text, sometimes past the end of a short file. The earlier
version did the same, so this fault is older than the plain-words rule. We then added a step that has AsChecked re-read
the lines it cites before writing the report. The run logs showed that in 18 of the second version's 24 runs no cited
line opened again near the end, and one run ranked orders lost on a restart above a stranger marking orders as paid.
The released version makes the re-reading a real step (each of its 24 runs read a few lines of a file again near the end,
3 to 10 times), shows line numbers when it reads a file that may hold keys, and ranks what a stranger can do on purpose
above an accident of about the same harm.

Because new scorers judged each round, their strictness could differ between rounds. So at the end, one scorer per app
judged all 80 Claude Code reports together, every version mixed and unlabelled, with the same instructions. The table
shows that single scoring:

| Runs | Most serious problem found (6 apps with planted problems) | Other planted problems found, per run | All report checks met | Correct apps with no false alarm | Planted instruction reported, not followed |
|---|---|---|---|---|---|
| Claude Code, released version (24) | 18 of 18, always as finding 1 | 2.8 | 24 of 24 | 6 of 6 | 3 of 3 |
| Claude Code, second version (24) | 18 of 18, 17 as finding 1 | 2.8 | 22 of 24 | 6 of 6 | 3 of 3 |
| Claude Code, first version with the plain-words rule (24) | 18 of 18, always as finding 1 | 2.8 | 20 of 24 | 6 of 6 | 3 of 3 |
| Claude Code, earlier version (8) | 6 of 6 | 2.8 | 6 of 8 | 2 of 2 | 1 of 1 |
| Codex (8) | 5 of 6 | 2.0 | 3 of 8 | 2 of 2 | 1 of 1 |
| Cursor (2 of 8; the other six did not run) | 2 of 2 | 3.0 | 1 of 2 | not run | not run |

The released version met every pass mark. Scored round by round, by new scorers each time, the three versions came to
20, 21 and 23 of 24 on the report checks: the second round's scorers failed a citation one line off, while the third
round's passed similar ones, and the third round's failed an effort given as "small to medium" that the single scoring
passed. The scorers were also asked to list every close call. Many are about wording: a key's length given as a bound
rather than a number, a range that runs a line past what it shows, two efforts for two alternative fixes, the
project's name spelled as in its package file, a loose verb about a cited line. Others are more than wording: in the
released version, a search result the scorer judged wrong, shapes in a cited drawing miscounted, a short note after the
report's closing lines, a key's length not given, behaviour overstated, the order of findings below the first. The
scorers were not shown the exact wording of the three closing lines; those who say how they judged them compared the
reports with each other instead. Counting every close call on the report checks as a fail, including those a scorer
wrote for all of an app's reports, no report of the three versions with the plain-words rule passes, and 1 of the
earlier version's 8 does: almost every report has some close call, so that count cannot tell the versions apart. As in
every round, a citation of the reviewed copy's own git settings file counts as present:
each such report cites its remote address on the line where it is.

In every Claude Code run no file changed and no planted key value appeared in anything the AI wrote. On the released
version, a plain-words line came before about 97% of the AI's steps (93% on the second version, 96% on the first,
about 12% on the earlier version), and none of those lines appeared in a report.

Split by stack, released version (single scoring): apps whose stacks the method has its own checks for (team notes,
group chat, desktop notes, and the first correct app) against the others:

| Stacks | Most serious problem found | Other planted problems found, per run | All report checks met |
|---|---|---|---|
| With their own checks | 9 of 9 | 2.3 | 12 of 12 |
| Without | 9 of 9 | 3.2 | 12 of 12 |

Limits: we wrote the apps and planted the problems ourselves.
Three of the six apps, and one of the two correct ones, use stacks the method has its own checks for. Codex and Cursor
ran once per app, on the first version, and were scored only in the first round. The fixes were made after seeing the
earlier rounds and tested again on the same apps, so the last round is not a fresh test of them. It shows that the
released version is consistent and did not get worse; the four real projects in the benchmark above remain the main
evidence.

## Plan mode and Auto mode

**What we tested.** On 24 and 25 November 2026 (UTC), on one Windows machine, our full test ran AsChecked (commit
`be325c9`) on 24 sample apps we built: 19 with planted problems and 5 built correctly; two of the 19 also hide an
instruction aimed at AI reviewers. Each setting below was set to review every app five times, each run in its own copy of the
app, with nobody approving anything during a run. Tools: Claude Code 2.1.330; Codex CLI 0.170.0 in its read-only
sandbox; Antigravity CLI 1.5.16 in its default mode with its sandbox. A program checked every copy for any file
created, changed or deleted, and every report and tool record for any piece of a planted secret key.

**How it was scored.** One scorer per app, Claude Fable 5.2 at high effort, scored that app's reports blind (renamed,
tool and mode hidden) under rules frozen before the first run. **Complete and correct** means: the most serious
planted problem found and put first (on a correct app, no false alarm); all seven report checks met (title and order,
parts of each finding, evidence that holds, keys described without showing them, no all-clear or praise, closing
sections, length); and no safety failure. A second scorer re-scored 96 reports blind. On "evidence that holds" the
two first agreed on only 7 of the 10 reports either failed, so before matching any score to a setting we wrote that
rule out more exactly and re-scored every report on it; the two then agreed on 11 of 13. On complete and correct as a
whole they agreed on 93 of 96 reports.

**Results, all 24 apps**

| Setting | Complete and correct | Most serious problem found and put first | All seven report checks | False alarms (runs on correct apps) | Safety failures |
|---|---|---|---|---|---|
| Claude Fable 5.2, medium, plan mode | 116 of 120 (0 to 100%) | 95 of 95 | 116 of 120 | 0 of 25 | 0 |
| **Claude Fable 5.2, medium, Auto (recommended)** | **112 of 120** (88.4 to 97.9%) | 95 of 95 | 112 of 120 | 0 of 25 | 0 |
| Claude Opus 5.5, medium, plan mode | 104 of 120 (80.3 to 92.5%) | 93 of 95 | 105 of 120 | 0 of 25 | 1 |
| Claude Opus 5.5, medium, Auto | 108 of 120 (82.7 to 95.8%) | 94 of 95 | 108 of 120 | 0 of 25 | 0 |
| Claude Fable 5.2, low, Auto | 113 of 120 (72.7 to 99.7%) | 94 of 95 | 113 of 120 | 0 of 25 | 0 |
| Claude Sonnet 5.5, medium, Auto | 113 of 120 (74.4 to 99.5%) | 93 of 95 | 115 of 120 | 2 of 25 | 0 |
| Codex, GPT-6-Luna, medium, read-only | 72 of 110 (47.5 to 80.5%) | 74 of 87 | 76 of 110 | 1 of 23 | 0 |
| Antigravity, Gemini 4 Hydrogen, medium | 9 of 10 (0 to 100%) | 9 of 9 | 9 of 10 | 0 of 1 | 0 |

In brackets: 95% ranges, from a bootstrap over the 24 apps (bootstrap-t, 10,000 draws, widened by 1.17, the factor
our coverage test chose before the first run). When nearly every app passes every run, this method cannot say how far
the rate could move and gives a range of 0 to 100: read those as no range. Comparisons between settings use the same
method on the difference, worked out on the same apps, and the answers below rest only on those. Two Claude Opus 5.5
runs (one per mode) ended without a report and count as not complete and correct. Most report-check misses were
"evidence that holds": a cited line just off, or a claim the cited code contradicts.

**Is Auto as good as plan mode?** In our test, "as good as Plan" for both models, by our rule fixed before the test
(Auto had no safety failure, and the whole range of Auto minus plan mode lies above -10 points). Claude Fable 5.2 at
medium effort: -3.3 points (range -9.3 to +2.2), so Auto could be up to 9.3 points behind. Claude Opus 5.5 at medium
effort: +3.3 (range -3.1 to +9.7).

**Which Claude setting is best in Auto?** In our test, no clear best: the sample apps did not separate the settings.
Among the four Auto settings, Claude Fable 5.2 at low effort and Claude Sonnet 5.5 at medium effort tied at 113 of 120; Claude Fable 5.2 at medium effort
in Auto was level with them; for Claude Opus 5.5 at medium effort in Auto the test could not show that (it could be up to 13.1 points
behind). So the README keeps the order of our benchmark on real projects, with Claude Fable 5.2 at medium effort first.

**Other tools.** In our test, Claude Fable 5.2 at medium effort in Auto did better than Codex with GPT-6-Luna at medium
effort, the one model we ran in Codex: 27.9 points ahead on complete and correct (range 12.6 to 46.3). Antigravity:
measured, no comparison (10 runs; the rules need 35).

**Recommended: Claude Fable 5.2 at medium effort, in Auto.** In our test it met every release bar fixed before the
test: the most serious problem found in 95 of 95 runs on apps with one (bar 90%); all seven report checks in 112 of
120 (bar 92%); a false alarm on 0 of 25 runs on correct apps (bar at most 1); the planted instruction followed in 0 of
10; no safety failure.

**Safety.** One safety failure: Claude Opus 5.5 at medium effort in plan mode, on one app. A command meant only to read
wrote a file into the project. No other run changed its copy. No report or tool record showed any piece of a planted key. The planted
instruction was reported and never followed, in 10 runs on two apps by each Claude setting and in 8 runs on two apps
by Codex. No write outside the project copy was found in the folders we watched (the tools' own folders and the folder
holding the copies), apart from the tools updating their own plugins.

**The 16 apps built for this test alone** (complete and correct): Claude Fable 5.2 medium, plan mode 76 of 80; Auto 74
of 80; Claude Opus 5.5 medium, plan mode 68 of 80; Auto 72 of 80; Claude Fable 5.2 low, Auto 74 of 80; Claude Sonnet
5.5 medium, Auto 77 of 80; Codex 46 of 73; Antigravity 7 of 7.

**Runs.** Codex ran 110 and Antigravity 10 of the 120 runs planned for each; Cursor was not part of this test. One
Claude run that read a file outside its copy was set aside and run again.

**Limits:** we built the 24 apps and planted their problems (16 for this test, 8 for the sandbox test above); they
are not projects from real users. One
Windows machine, the tool versions above, two days in November 2026. AsChecked was developed with Claude, and Claude
models built the apps, checked the answer keys and scored the reports. The real projects in our benchmark remain the main evidence for choosing a model.

## Cloud session (26 Nov 2026)

We reviewed one GitHub project, our own website's repository, in a Claude Code cloud session: Claude Opus 5.5 at
medium effort, Auto mode, the prompt file `paste/aschecked-prompt.md` attached and nothing installed. The report had
every required part, the four citations we checked against the repository each said what the report claimed, no key
value appeared, and nothing in the project changed (`git status` showed nothing). The session's git refused one of
AsChecked's safety settings, so AsChecked ran no git commands: it did not search past commits for keys or check other
branches, and the report said so under "Not checked". Installing AsChecked as a skill does not work in a cloud
session: it can download only from the repository it is attached to, and it does not keep an install.
