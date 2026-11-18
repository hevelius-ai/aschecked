# AsChecked

> **In development, not ready to use.** The method passed its re-test (see Results), but the release checks are
> still to come. Please do not install or run it until the first release is tagged.

AsChecked is a read-only review for people who built something with AI. You run it in the AI tool you already use.
It reads your project and gives you a short report in plain words: at most five things a professional would fix or
add that you did not know to ask for, most harmful first. Each one comes with its evidence, a fix, and a prompt you
can paste straight to your AI builder. Up to five further problems follow, one line each with where they are.

**It is not** an audit, a certificate or a security scan. It never says your project is safe: it lists the
problems it found in what it checked.

**The AI model and its effort setting matter more than the tool.** In our re-test, Claude Opus 5.5 at its maximum
effort setting found 16 of 19 known problems in four test projects, including the most serious one in each, and so
did Claude Fable 5.2 at its default effort. Claude Opus 5.5 at its default effort found 11, and Claude Sonnet 5.5
found 8 (see Results). Claude Sonnet 5.5 stopped early: it took about a fifth as many reading steps as Claude Opus
5.5 at max effort before writing its report. In our earlier tests, weaker, older or free models missed serious
problems and told the owner that flawed access rules were strong. Use Claude Opus 5.5 at max effort or Claude Fable
5.2 where you can, and treat a report from a free consumer chat model with caution.

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
best results, start Claude Code with Claude Opus 5.5 at max effort:
`claude --model opus --effort max`. A review then takes about 15 to 20 minutes. Switch Claude Code to plan mode
(press Shift+Tab until it shows plan mode), then type `/aschecked`. AsChecked asks you three short questions about
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
2. Start a new chat with Claude Opus 5.5 and set its effort to max (a chat starts at high; max is in the same menu).
   Whether a chat reaches the re-test's results is not yet proven. Upload two files: the zip, and
   [`paste/aschecked-prompt.md`](paste/aschecked-prompt.md) from this repository.
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

Re-test of this version, 15 Nov 2026 (Claude Fable 5.2 on 17 Nov): one run per project per model, in Claude Code's
plan mode. The four test projects are AsBuild, a web app with accounts and roles, a mobile fitness app with health
data, and a desktop app.
Earlier hand reviews found 19 problems in them. A problem counts as found only when the report names the same
defect in the same place, with every part of it; one-line "Also found" items count too. Two more copies test
safety: one with planted fake keys, one with a planted instruction telling the reviewer to report nothing. An
independent reviewer checked every count.

| Model | Known problems found (of 19) | Most serious problem found | Planted fake keys | Planted instruction | Report length |
|---|---|---|---|---|---|
| Claude Opus 5.5, max effort | 16 | 4 of 4 projects | none shown | reported, not followed | 899 to 1,046 words |
| Claude Opus 5.5, default effort | 11 | 3 of 4 | none shown | reported, not followed | 966 to 1,168 words |
| Claude Sonnet 5.5 | 8 | 2 of 4 | none shown | reported, not followed | 762 to 1,123 words |
| Claude Fable 5.2 | 16 | 4 of 4 projects | none shown | reported, not followed | 928 to 1,018 words |

How we got there: the pass mark, set before testing, was 15 of 19 for at least one model. The first version found at
most 14 with any model. Four more rounds followed (one change, a longer report, made results worse and was undone).
The changes kept were checks on the main journey, lost work, what the product publishes and platform claims;
keeping related problems together; and, after the best run still stopped at 14, the "Also found" list. Counting
those lines was decided after seeing the earlier results. A single run per project shows what one review found, not
how much results vary from run to run.

## Licence

(c) 2026 Hevelius AI Group LLC. The method text (`skills/`, `paste/` and this README) is licensed under CC BY 4.0
([LICENSE](LICENSE)); the join script, tests and configuration under MIT ([LICENSE-CODE](LICENSE-CODE)).

Suggested credit: "AsChecked" by Hevelius AI Group LLC, https://github.com/hevelius-ai/aschecked, licensed under CC BY 4.0.
