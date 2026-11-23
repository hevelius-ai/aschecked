# AsChecked

> **Version 1.** Tested in Claude Code, where Claude Fable 5.2 at medium effort did best
> ([how we tested](docs/how-we-tested.md)). AsChecked lists problems it found in what it checked;
> it cannot confirm that anything is secure.

**You built an app with AI, and it works. AsChecked tells you what you didn't know to ask for.**

AsChecked reads your project and tells you, in plain words, the few things a
professional would fix first: data anyone can see, keys left in the open, promises your app makes that the code
doesn't keep. Use it with Claude Fable 5.2 or Claude Opus 5.5: weaker or free models missed serious problems in our
tests.

**What it is not:** it is not an audit, a certificate or a security scan, and it never tells you your app is safe.

## What you get

A short report: up to five problems, most harmful first, each with why it matters, where it is, how to fix it and a
message to paste to your AI builder; then up to five smaller ones, one line each.

## How it works

- **It is meant only to read.** It runs in Claude Code's plan mode, which is meant to keep Claude reading instead of
  changing your files. You switch plan mode on with Shift+Tab before you start a review.
- The AI reads your project's files, including any keys written into them. The
  report never shows a key's value: it names a key by its kind, file, line and length.

## What you need in Claude Code

- **Claude Code** (Anthropic's terminal app) and a Claude plan that includes it. To install it, see
  https://code.claude.com/docs/en/setup
- **Your project in a folder.**
- **One of these three settings:**

| Model and effort | Start Claude Code with |
|---|---|
| **Claude Fable 5.2, medium (best)** | `claude --model fable --effort medium` |
| Claude Opus 5.5, medium | `claude --model opus --effort medium` |
| Claude Fable 5.2, low | `claude --model fable --effort low` |

## Install it (once)

1. Make a new, empty folder (not your project) and open a terminal in it. On Windows, right-click inside the folder
   and choose Open in Terminal. On a Mac, right-click the folder in Finder and choose Services, then New Terminal at
   Folder. Type `claude` and press Enter. If it asks whether you trust this folder, choose **Yes**.
2. Copy this message, paste it into Claude Code and press Enter:

   ```
   Install the AsChecked review skill for me. Download
   https://github.com/hevelius-ai/aschecked/archive/refs/tags/v1.0.0.zip into this folder and unpack it here. Read
   the files in its skills/aschecked folder and tell me in two sentences what they do. Then tell me what you will copy
   and where, and wait for my yes. After my yes, copy that folder to .claude/skills/aschecked in my home folder,
   replacing any older copy, and delete what you downloaded and unpacked. Change nothing else. Finally, check that
   .claude/skills/aschecked/SKILL.md is in my home folder and say "AsChecked is installed".
   ```

3. Claude Code may ask before it downloads and unpacks. If it names the AsChecked download or this folder, choose
   the plain **Yes**, not "don't ask again"; otherwise **No**.
4. Claude Code says what the files do and what it will copy. Type `yes` and press Enter.
5. Claude Code normally asks before it writes to your `.claude` folder. Check that it names `.claude/skills/aschecked`
   (on Windows `.claude\skills\aschecked`), then choose the plain **Yes**, not "don't ask again".
6. If it then asks to look inside `.claude/skills/aschecked` or to delete what it downloaded here, choose the plain
   **Yes**. If it asks about anything else, choose **No**.
7. When it says "AsChecked is installed", type `/exit` and press Enter.

To update it later, paste the message from this page again: it always names the newest version.

## Run a review

1. **Open a terminal in your project's folder.** On Windows, right-click inside the folder and choose Open in
   Terminal. On a Mac, right-click the folder in Finder and choose Services, then New Terminal at Folder.
2. **Check your instruction files.** Look in your project's folder for files like `CLAUDE.md`, `AGENTS.md` or
   `.cursorrules` (a Mac hides names that start with a dot: press Cmd+Shift+period in Finder). Your AI tool reads them
   by itself. If you did not write one, read it: text telling an AI how to review your project, or to say it is fine,
   is a warning sign. AsChecked reports such text, but it cannot stop your tool from loading the file. If there are
   none, go on.
3. **Choose the version.** For your finished app, type `git checkout main` (or `git checkout master`, if that is its
   name) and press Enter. For work still on another branch, type `git checkout` and that branch's name, and press
   Enter. Not using git? Go on.
4. **Start Claude Code.** Type `claude --model fable --effort medium` and press Enter. Without Claude Fable 5.2 in your
   plan, type `claude --model opus --effort medium` instead. If it asks whether you trust this folder, choose
   **Yes**.
5. **Switch on plan mode.** Press Shift+Tab until the bottom of the screen shows plan mode. Do not start the review in
   auto-accept or bypass-permissions mode.
6. **Start the review in plan mode:** type `/aschecked` and press Enter.
7. **Answer the three questions**, or say "skip". If part of your app is not built yet, say which part:
   AsChecked then lists the problems in that part separately.
8. **Approve only reading.** Claude Code may ask before AsChecked runs a command. Choose the plain **Yes**, not
   "don't ask again", if it only reads (looks, lists or searches); otherwise choose **No**.
9. **Keep planning.** If Claude Code asks whether to approve a plan, choose to keep planning: the report is the
   answer, and approving would let it start changing your project.
10. **Save the report.** Select it with the mouse and copy it (Ctrl+Shift+C or right-click and Copy; Cmd+C on a
    Mac), then paste it into a text file outside your project's folder.
11. **Fix what it found.** Paste each "Paste to your AI builder" message into your AI builder: Lovable, Bolt, Cursor,
    or Claude Code started again in your project without plan mode.

## No Claude Code? Use a claude.ai chat

You need a claude.ai account.

1. **Download your project as a zip.** On GitHub: open your project, click **Code**, then **Download ZIP** (for a
   branch, choose it first). From Lovable, Bolt or Replit: use their download, or sync to GitHub first.
2. **Download the AsChecked prompt file.** Open [`paste/aschecked-prompt.md`](paste/aschecked-prompt.md) on GitHub
   and click **Download raw file**.
3. **Start a new chat** at claude.ai with Claude Fable 5.2 (or Claude Opus 5.5), medium effort if offered.
4. **Upload both files** and type: "Run the AsChecked review in the attached prompt file on the attached project."
5. **Answer the three questions**, or say "skip". If part of your app is not built yet, say which part:
   AsChecked then lists the problems in that part separately.
6. **Save the report** that appears in the chat into a text file, then paste each "Paste to your AI builder" message
   into your AI builder.

Our tests ran in Claude Code; a chat is not yet proven to reach the same results.

## More

- [How we tested it](docs/how-we-tested.md).
- [Other ways to install, update or remove it](docs/install-options.md).
- [What read-only covers, and where it stops](docs/git-safety.md).
- [Other AI tools](docs/other-tools.md) such as Codex, Cursor, Lovable or Bolt: packaged for, not yet proven; of the
  five we tried, most fell short.

## Licence

(c) 2026 Hevelius AI Group LLC. The method text (`skills/`, `paste/`, `docs/` and this README) is licensed under CC BY
4.0 ([LICENSE](LICENSE)); the join script, tests and configuration under MIT ([LICENSE-CODE](LICENSE-CODE)).

Suggested credit: "AsChecked" by Hevelius AI Group LLC, https://github.com/hevelius-ai/aschecked, licensed under CC BY 4.0.
