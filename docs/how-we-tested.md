# How we tested

Back to the [README](../README.md).

## Which version was tested

The benchmark below ran on the method as it was on 18 Nov 2026 (`skills/aschecked` at commit `d8dd162`), before the
rule that has AsChecked say in plain words what each step does (added 22 Nov 2026). The sandbox test below ran on the
released version and on the earlier one, to check that the new rule changed nothing else.

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

In our test, on a small made-up app with a half-built feature and three planted problems in it, one run per model,
each at extra effort (`--effort xhigh`), Claude Opus 5.5, Claude Fable 5.2 and Claude Sonnet 5.5 each found all
three, in that separate list. We had planned to count only the numbered findings and "Also found" lines; because the
method hands such problems to the work in progress, we counted that list too, a change made after seeing the results.

## Results of the benchmark

Benchmark of this version, 18 Nov 2026, in Claude Code's plan mode. Use these results to choose a model and an effort
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

**What these results can and cannot claim:** they hold for these four projects, this version of the method and one
computer. They show averages, the spread between runs and cost, not that every project will get the same result.

How the method got here: the pass mark of 15 of 19 was set before an earlier re-test (15 Nov, one run per model).
The first version found at most 14 with any model. Four more rounds followed (one change, a longer report, made
results worse and was undone). The changes kept were checks on the main journey, lost work, what the product
publishes and platform claims; keeping related problems together; and, after the best run still stopped at 14, the
"Also found" list. Counting those lines was decided after seeing the earlier results.

## Sandbox test of the released version (22 Nov 2026)

Eight small apps we wrote for this test: six with problems we planted on purpose (team notes on Next.js and
Supabase, a group chat on Firebase, a bookings API on Express, an invoices app on Flask, a desktop notes app on
Electron, a shop taking card payments with Stripe) and two built correctly, to count false alarms. One app hid an
instruction telling AI reviewers to call it secure; two hid fake keys. An independent reviewer checked the answer key
against the code before any run, and the reports were scored blind (the scorer did not know which version or tool
wrote each one).

Claude Code with Claude Fable 5.2 at medium effort, in plan mode: three runs per app on the released version, one run
per app on the earlier version. Codex (GPT-6-Luna, medium) and Cursor (free plan, Auto model) once per app.

| Runs | Most serious problem found (6 apps with planted problems) | Other planted problems found, per run | All report checks met | Correct apps with no false alarm | Planted instruction reported, not followed |
|---|---|---|---|---|---|
| Claude Code, released version (24) | 18 of 18, always as finding 1 | 2.8 | 19 of 24 | 6 of 6 | 3 of 3 |
| Claude Code, earlier version (8) | 6 of 6 | 2.8 | 6 of 8 | 2 of 2 | 1 of 1 |
| Codex (8) | 5 of 6 | 2.0 | 3 of 8 | 2 of 2 | 1 of 1 |
| Cursor (2 of 8; the free plan's limit stopped the rest) | 2 of 2 | 3.0 | 1 of 2 | not run | not run |

In every Claude Code run no file changed and no planted key value appeared in anything the AI wrote. On the released
version, a plain-words line came before about 96% of the AI's steps (about 12% on the earlier version), and none of
those lines appeared in a report.

We fixed the pass marks before the runs. The released version met all of them but one: every report check met in at
least 22 of 24 runs. It was 19: five reports cited a line number one or two lines away from the text, sometimes past
the end of a short file. The earlier version did the same in one of its eight runs, so the plain-words rule did not
cause it.

What this test cannot show: planted problems are easier to find than real ones, and we wrote the apps ourselves.
Three of the six apps, and one of the two correct ones, use stacks the method has its own checks for. Codex and Cursor
ran once per app. It shows that the released version is consistent and did not get worse; the four real projects in
the benchmark above remain the main evidence.
