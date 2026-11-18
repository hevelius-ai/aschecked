# AsChecked

> **Version 1.** The method passed its benchmark (see Results). AsChecked lists the problems it found in what it
> checked; it cannot confirm that anything is secure.

AsChecked is a read-only review for people who built something with AI. You run it in the AI tool you already use.
It reads your project and gives you a short report in plain words: at most five things a professional would fix or
add that you did not know to ask for, most harmful first. Each one comes with its evidence, a fix, and a prompt you
can paste straight to your AI builder. Up to five further problems follow, one line each with where they are.

**It is not** an audit, a certificate or a security scan. It never says your project is safe: it lists the
problems it found in what it checked.

**The AI model and its effort setting matter more than the tool.** We tested 13 model and effort settings on four
test projects with 19 known problems, and the best was **Claude Fable 5.2 at medium effort**: 15 of 19 on average
over three runs, and the most serious problem in every report. Claude Opus 5.5 at medium effort (14.7) and Claude
Fable 5.2 at low effort (14.3) came next. Higher effort did not help: with Claude Opus 5.5, high, extra-high and max
found no more and took about seven times longer at most; with Claude Fable 5.2, high found no more (extra-high and
max were not run). Claude Sonnet 5.5 stopped early: at medium effort it took fewer than half as many steps as Claude
Fable 5.2 before writing its report, and below max effort it missed the most serious problem in half the projects
(see Results). In our earlier tests, weaker, older or free models missed serious problems and told the
owner that flawed access rules were strong. Treat a report from a free consumer chat model with caution.

## What the AI sees

The AI reads your project's files, including any keys written into them, as the AI that built it already does.
The report never shows a key's value: it names a key by its kind, file, line and length.

## Run it in Claude Code

**The mode it needs:** AsChecked runs in Claude Code's **plan mode**, which is meant to keep Claude reading and
planning instead of editing your files. You switch it on in step 3 (press Shift+Tab until it shows plan mode). Do
not start the review in auto-accept or bypass-permissions mode.

**1. Install it** (one of these):

- **By hand:** on this page, click **Code**, then **Download ZIP**, and unzip it. Copy its `skills/aschecked`
  folder into your project's `.claude/skills` folder, so that it ends up as `.claude/skills/aschecked` (create the
  `.claude` and `skills` folders if they are missing). To use it in every project, copy it to
  `~/.claude/skills/aschecked` in your home folder instead. On a Mac, Finder hides folders whose names start with
  a dot: press Cmd+Shift+period to show them. Claude Code reads `.claude/skills`, not `.agents/skills`.
- **With the GitHub CLI** 2.94 or later (`gh skill` arrived in 2.90 and is in preview; `--all` needs 2.94): open a
  terminal in your project's folder (it must be a git repository) and run
  `gh skill install hevelius-ai/aschecked --agent claude-code --all`. To install it for every project instead, add
  `--scope user`. Without `--agent claude-code` it installs for Copilot; without `--all`, when nobody can answer its
  question (for example when your AI tool runs it for you), it installs nothing.
- **With the skills command** (needs Node.js): open a terminal in your project's folder and run
  `npx skills add hevelius-ai/aschecked -a claude-code -y`. It puts the skill in `.claude/skills/aschecked` and
  adds a `skills-lock.json` file to your project's folder.

Start Claude Code after installing it: in our tests, a Claude Code session that was already open did not see the
newly installed skill.

**To remove AsChecked:** delete the `aschecked` folder it was installed into (`.claude/skills/aschecked` in your
project, or `~/.claude/skills/aschecked` in your home folder); the GitHub CLI has no uninstall command. If you
installed it with the skills command, run `npx skills remove aschecked` in your project's folder instead, which also
takes it out of `skills-lock.json`.

**2. Check the instruction files first.** Before the review starts, your tool loads its own instruction files by
itself: Claude Code loads `CLAUDE.md` (and `AGENTS.md` when there is no `CLAUDE.md`); other tools load files such as
`AGENTS.md` or `.cursorrules`. If you did not write them, open them and read them first: text telling an AI how to
review your project, or to say it is fine, is a warning sign. AsChecked treats such text as data and reports it,
but it cannot stop your tool from loading the file.

**3. Start the review.** First open the branch you want reviewed (see "Which version it reviews" below). For the
best results we measured, start Claude Code with Claude Fable 5.2 at medium effort:
`claude --model fable --effort medium`. A review then takes about 2 to 4 minutes. With Claude Opus 5.5, use medium
effort too: `claude --model opus --effort medium`. If you have set the `CLAUDE_CODE_EFFORT_LEVEL` environment
variable, it overrides `--effort`. Switch Claude Code to plan mode (press Shift+Tab until it shows plan mode), then
type `/aschecked`. AsChecked asks you three short questions about
your project; answer them, or say "skip" and it will work from your README.

**4. Read the report.** If Claude Code asks at the end whether to approve a plan, choose to keep planning: the
report is the answer, and approving would let it start editing your project. Save the report yourself.

Read-only is an instruction the model is asked to follow, in Claude Code and every other tool. Plan mode in Claude
Code is meant to keep it reading and planning instead of editing. Whether other tools' plan or read-only modes
really block changes is not yet proven; where nothing blocks them, the limits are only instructions.

**Git settings:** a project's own git settings can make git run a program. AsChecked's git commands switch off the
ones we know of, and it skips its history scan for key leaks where it cannot check the settings safely, then
suggests you run that scan in a fresh clone (a new copy cloned from where your project is hosted), which carries
none of the folder's settings. We tested this on 19 setups: normal clones, partial clones, submodules, worktrees,
shallow copies and planted settings. Git has more settings than we tested. If someone sets up a project's git folder
on purpose to hide something or to run a program, AsChecked may not notice; that is outside what AsChecked covers.
To be safe, review a copy you cloned yourself.

## Run it in a chat (claude.ai)

1. Download your project as a zip, from the branch you want reviewed (see "Which version it reviews" below): on
   GitHub, **Code**, then **Download ZIP**; in Bolt or Replit, use their
   download or export. Lovable's own zip download is on paid plans only; on a free plan, sync your project to
   GitHub and use GitHub's **Download ZIP**.
2. Start a new chat with Claude Fable 5.2 (or Claude Opus 5.5); if the chat offers an effort setting, choose medium.
   Our benchmark ran in Claude Code; whether a chat reaches the same results is not yet proven. Upload two files: the
   zip, and [`paste/aschecked-prompt.md`](paste/aschecked-prompt.md) from this repository.
3. Type: "Run the AsChecked review in the attached prompt file on the attached project."

## Which version it reviews

AsChecked reviews the files in your project folder as they are, on the branch you have open. It may also look at
your other branches for work that was never merged, and the report says what it reviewed. Choose the branch before
you start the review.

- **A finished project:** open your main branch (in a terminal: `git checkout main`). For a chat, download the zip
  from your main branch.
- **Work in progress:** open that branch instead (`git checkout <branch-name>`; for a chat, choose the branch on
  GitHub, then **Code**, then **Download ZIP**). When AsChecked asks what changed recently, say what you are building
  and what is not built yet. The method hands problems in a part you are still building to that work instead of
  ranking them. In our test they came in a separate list after the numbered findings, not ranked, and the parts the
  owner said were not built yet were not listed as numbered findings.

In our test, on a small made-up app with a half-built feature and three planted problems in it, one run per model,
each at extra effort (`--effort xhigh`), Claude Opus 5.5, Claude Fable 5.2 and Claude Sonnet 5.5 each found all
three, in that separate list. We had planned to count only the numbered findings and "Also found" lines; because the
method hands such problems to the work in progress, we counted that list too, a change made after seeing the results.

## Other tools

AsChecked is packaged for, not yet proven in, these tools.

- **Codex, Cursor, Antigravity, Devin Desktop, Kilo:** copy the `skills/aschecked` folder (from the downloaded zip,
  as above) into your project as `.agents/skills/aschecked`. Packaged for, not yet proven. Use the tool's plan or
  read-only mode where it has one.
- **Cline:** copy the folder into `.claude/skills/aschecked`, as for Claude Code. Packaged for, not yet proven.
- **Lovable, Bolt:** these builders document importing a skill from a public GitHub repository; for Lovable use
  `https://github.com/hevelius-ai/aschecked/tree/main/skills/aschecked`. Not yet proven: AsChecked has not been
  imported into them yet, and whether they also take the `references` folder is unknown (the method works from
  `SKILL.md` alone).
- **Replit:** not tried (needs a paid plan): Replit documents skills and its Plan mode for paid plans only. Not yet
  proven. On any plan, you can download your project from Replit and use "Run it in a chat (claude.ai)" above.
- **Anything else:** paste [`paste/aschecked-prompt.md`](paste/aschecked-prompt.md) and give it your code. Not yet
  proven.

**Antigravity, tried with an earlier version of the method as a plain prompt:** with Gemini 3.8 Flash it missed all
four known problems in a small web app with accounts and called that app's access rules strong; it found two of
five known problems in a desktop app. Claude Sonnet 4.6 in the same tool found one of the four web-app problems.
The installed v1 skill in Antigravity is not yet tried.

## Results

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

## Licence

(c) 2026 Hevelius AI Group LLC. The method text (`skills/`, `paste/` and this README) is licensed under CC BY 4.0
([LICENSE](LICENSE)); the join script, tests and configuration under MIT ([LICENSE-CODE](LICENSE-CODE)).

Suggested credit: "AsChecked" by Hevelius AI Group LLC, https://github.com/hevelius-ai/aschecked, licensed under CC BY 4.0.
