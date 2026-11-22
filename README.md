# AsChecked

> **Version 1.** Tested in Claude Code, where Claude Fable 5.2 at medium effort did best
> ([how we tested](docs/how-we-tested.md)). AsChecked lists problems it found in what it checked;
> it cannot confirm that anything is secure.

**You built an app with AI, and it works. AsChecked tells you what you didn't know to ask for.**

AsChecked reads your project and tells you, in plain words, the few things a professional would fix first: data
anyone can see, keys left in the open, promises your app makes that the code doesn't keep.

**What you get back:** a short report with at most five problems, most harmful first. Each one says why it matters,
where it is, how to fix it, and a ready-made message to paste to your AI builder. Then up to five smaller ones, one line each.

**What it is not:** it is not an audit, a certificate or a security scan, and it never tells you your app is safe.

**Tested with** Claude Fable 5.2, Claude Opus 5.5 and Claude Sonnet 5.5 in Claude Code; the best was **Claude Fable
5.2 at medium effort**. Weaker or free models missed serious problems in our tests.

## Which AI model to use

The AI model matters more than the tool. Our test: four projects, 19 known problems, three runs each:

| Model and effort | Known problems found (of 19), average | Most serious problem found |
|---|---|---|
| **Claude Fable 5.2, medium (best)** | 15.0 | 12 of 12 |
| Claude Opus 5.5, medium | 14.7 | 11 of 12 |
| Claude Fable 5.2, low | 14.3 | 12 of 12 |

For Claude Fable 5.2 and Claude Opus 5.5, more effort than medium did not find more.
[How we tested](docs/how-we-tested.md).

## Run it in Claude Code

**It is meant only to read.** In Claude Code it runs in **plan mode**, which is meant to keep Claude reading
instead of changing your files; switch it on in step 3 (press Shift+Tab until it shows plan mode). Do not start the
review in auto-accept or bypass-permissions mode.

1. **Install it.** Open a terminal in your project's folder and run
   `gh skill install hevelius-ai/aschecked --agent claude-code --all` (needs the GitHub CLI). No terminal? On this
   page click **Code**, then **Download ZIP**, and copy its `skills/aschecked` folder into your project as
   `.claude/skills/aschecked`. Then start Claude Code. [Other ways to install it, and how to remove
   it](docs/install-options.md).
2. **Check your instruction files.** Your AI tool reads files such as `CLAUDE.md`, `AGENTS.md` or `.cursorrules` by
   itself. If you did not write them, read them first: text telling an AI how to review your project, or to say it is
   fine, is a warning sign. AsChecked reports such text, but it cannot stop your tool from loading the file.
3. **Start the review.** Open the version you want reviewed (see "Which version it reviews"). Start Claude Code
   with `claude --model fable --effort medium`, switch to plan mode and type `/aschecked`. It asks three short
   questions; answer them, or say "skip". Before each step it says in plain words what it will check.
4. **Read the report.** If Claude Code asks whether to approve a plan, choose to **keep planning**: the report is the
   answer, and approving would let it start changing your project. Save the report yourself: copy it into a text file
   outside your project's folder, so it does not show up as a change in your project.

The AI reads your project's files, including any keys written into them. The report never shows a key's value: it
names a key by its kind, file, line and length. [What read-only covers, and where it stops](docs/git-safety.md).

## Which version it reviews

It reviews the branch you have open, and may look at your other branches for unmerged work.

- **A finished project:** open your main branch (`git checkout main`). For a chat, download the zip
  from your main branch.
- **Work in progress:** open that branch (`git checkout <branch-name>`; for a chat, choose the branch on GitHub, then
  **Code**, then **Download ZIP**). When AsChecked asks what changed recently, say what you are building and what is
  not built yet: it lists problems in that part separately instead of ranking them
  ([our test of this](docs/how-we-tested.md)).

## Run it in a chat (claude.ai)

1. Download your project as a zip from the branch you want reviewed (see "Which version it reviews"): on GitHub,
   **Code**, then **Download ZIP** ([from Lovable, Bolt or Replit](docs/install-options.md#a-zip-of-your-project)).
2. Start a new chat with Claude Fable 5.2 (or Claude Opus 5.5), medium effort if offered. Upload the zip and
   [`paste/aschecked-prompt.md`](paste/aschecked-prompt.md) from this repository (open the link on GitHub and click
   **Download raw file**).
3. Type: "Run the AsChecked review in the attached prompt file on the attached project."

Our tests ran in Claude Code; a chat is not yet proven to reach the same results.

## Other tools

Also packaged for Codex, Cursor, Antigravity, Devin Desktop, Kilo, Cline, Lovable, Bolt and Replit, but not yet
proven in any: of the five we tried, most fell short. [How each did](docs/other-tools.md).

## Licence

(c) 2026 Hevelius AI Group LLC. The method text (`skills/`, `paste/`, `docs/` and this README) is licensed under CC BY
4.0 ([LICENSE](LICENSE)); the join script, tests and configuration under MIT ([LICENSE-CODE](LICENSE-CODE)).

Suggested credit: "AsChecked" by Hevelius AI Group LLC, https://github.com/hevelius-ai/aschecked, licensed under CC BY 4.0.
