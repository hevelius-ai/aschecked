# AsChecked

**You built an app with AI, and it works. AsChecked tells you what you didn't know to ask for.**

AsChecked reads your project and tells you, in plain words, the few things a
professional would fix first: data anyone can see, keys left in the open, promises your app makes that the code
doesn't keep. Use it with Claude Fable 5.2 or Claude Opus 5.5: weaker or free models missed serious problems in our
tests.

**What it is not:** It is not an audit, a certificate or a security scan: it only lists the problems it found in what it checked.

## What you get

A short report: up to five problems, most harmful first, each with why it matters, where it is, how to fix it and a
message to paste to your AI builder; then up to five smaller ones, one line each.

## How it works

- **It is meant only to read.** Its own rules tell Claude to read and never change your files. It works in Claude
  Code's Auto mode and in its plan mode. We tested both on 24 sample apps with Claude Fable 5.2 and Claude Opus 5.5:
  in our test, Auto was as good as plan mode for both. Details:
  [our test results](docs/how-we-tested.md#plan-mode-and-auto-mode).
- The AI reads your project's files, including any keys written into them. The
  report never shows a key's value: it gives a key's kind, file, line and, if certain, length.

## What you need

- **Claude Code** in the Claude desktop app, and a Claude plan that includes it. Get the app at
  https://claude.com/download and sign in.
- **Your project in a folder on your computer, one you built yourself.** Built in Lovable, Bolt or Replit and not on
  your computer? Use a claude.ai chat instead. Your project only on GitHub? Use a cloud session instead. For a project
  from someone else, read
  [this first](docs/git-safety.md#a-project-from-someone-else).
- **One of these three settings:** **Claude Fable 5.2 at medium effort (best)**, Claude Opus 5.5 at medium effort, or
  Claude Fable 5.2 at low effort.

## In the Claude Code desktop app

1. **Start a session on your project.** Open the **Code** tab (not Chat or Cowork) and start a new session; in the bar
   under the message box, choose **This computer**. If you use git branches, first switch your project's folder to the
   version you want checked (for your finished app, usually main or master), the way you usually do; if not, skip
   this. Then click the folder name and choose your project's folder. Untick **Worktree** if it is ticked. If it asks whether you trust this folder, choose **Yes**.
2. **Choose the model.** Click the model name and choose **Fable 5.2** (or **Opus 5.5** if the list has no Fable 5.2).
   In the same menu, open **Effort** and choose **Medium**. Turn fast mode off if it is on.
3. **First time only: install AsChecked.** Click the mode under the message box and choose **Auto** if it shows
   anything else. Copy this message, paste it into the message box and send it:

   ```
   Install the AsChecked review skill for me. Download
   https://github.com/hevelius-ai/aschecked/archive/refs/tags/v1.0.0.zip into a new temporary folder outside this
   project and unpack it there. Read the files in its skills/aschecked folder and tell me in two sentences what they
   do. Then tell me what you will copy and where, and wait for my yes. After my yes, copy that folder to
   .claude/skills/aschecked in my home folder, replacing any older copy, and delete what you downloaded and unpacked.
   Change nothing else. Finally, check that .claude/skills/aschecked/SKILL.md is in my home folder and say
   "AsChecked is installed".
   ```

   When it asks to copy to your home `.claude/skills/aschecked` folder (on Windows `.claude\skills\aschecked`), click
   its yes button (for example **Yes, copy it**) or type `yes` and send; otherwise click its no button or type `no`. Wait for "AsChecked is
   installed". To update AsChecked later, paste this message again in Auto mode: this page always names the newest
   version.
4. **Choose the mode.** Keep **Auto** (choose it under the message box if it shows anything else). Do not use Accept
   edits or Bypass permissions.
5. **Start the review:** type `/aschecked`, choose **aschecked** from the list and send. If it is not in the list, type
   `/reload-skills`, send it and try again. AsChecked is meant only to read your files. If a box asks you to allow something else, or to approve a plan, choose **No**.
6. **Answer the three questions.** If they come as cards, pick an answer (or **Other** and type skip), then **Next**,
   and on the last one **Submit**; if as text, answer or type skip and send. If part of your app is not built yet, say
   which part: AsChecked then lists the problems in that part separately.
7. **Your report is ready.** If you want to keep it, copy it into a text file outside your project's folder. Then pass
   it to your AI builder to fix what it found: each problem comes with a message ready to paste.

## Project on GitHub? Use a cloud session

Your project is on GitHub but not on your computer? Claude Code can review it in a cloud session. Nothing is
installed: you attach the AsChecked prompt file.

1. **Download the AsChecked prompt file.** Open [`paste/aschecked-prompt.md`](paste/aschecked-prompt.md) on GitHub,
   click the **⋯** button at the top right of the file and choose **Download**.
2. **Start a cloud session.** In the Claude Code desktop app, open the **Code** tab and start a new session. In the
   bar under the message box, choose a cloud environment (it shows a cloud icon), then your GitHub repository and the
   branch you want checked (for your finished app, usually main or master).
3. **Choose the model.** Choose **Fable 5.2** (or **Opus 5.5**) and **Medium** effort, and keep the mode on **Auto**.
   Do not use Accept edits or Bypass permissions.
4. **Start the review.** Attach the prompt file with **+**, type "Run the AsChecked review in the attached file on
   this project." and send. If it asks you to allow something other than reading, choose **No**.
5. **Answer the three questions**, or say "skip". If part of your app is not built yet, say which part: AsChecked
   then lists the problems in that part separately.
6. **Your report is ready.** If you want to keep it, copy it into a text file. Then pass it to your AI builder: each
   problem comes with a "Paste to your AI builder" message.

In a cloud session AsChecked could not search your project's git history for keys; the report says so. We tried this
once, on one GitHub project, with Claude Opus 5.5: [our test results](docs/how-we-tested.md#cloud-session-26-nov-2026).

## In a terminal

Using Claude Code in a terminal? [Follow these steps](docs/terminal.md).

## No Claude Code? Use a claude.ai chat

You need a claude.ai account.

1. **Download your project as a zip.** On GitHub: open your project, click **Code**, then **Download ZIP** (for a
   branch, choose it first). From Lovable, Bolt or Replit: use their download, or sync to GitHub first.
2. **Download the AsChecked prompt file.** Open [`paste/aschecked-prompt.md`](paste/aschecked-prompt.md) on GitHub,
   click the **⋯** button at the top right of the file and choose **Download**.
3. **Start a new chat** at claude.ai with Claude Fable 5.2 (or Claude Opus 5.5), medium effort if offered.
4. **Upload both files** and type: "Run the AsChecked review in the attached prompt file on the attached project."
5. **Answer the three questions**, or say "skip". If part of your app is not built yet, say which part:
   AsChecked then lists the problems in that part separately.
6. **Save the report** that appears in the chat into a text file, then paste each "Paste to your AI builder" message
   into your AI builder.

Our tests ran in Claude Code and other coding tools; a chat is not yet proven to reach the same results.

## Not using Claude? Other AI tools

AsChecked can also run in other AI tools, but we have not fully tested them or every model they offer: we tried five of
them (not Cline or the chat apps) and ran two, Codex and Antigravity, in our full test; none is proven yet. In our tests with Claude, the strongest models did best and weaker ones missed serious
problems, so choose the strongest model your tool offers.

For a tool that says "copy the folder", first download
[the AsChecked zip](https://github.com/hevelius-ai/aschecked/archive/refs/tags/v1.0.0.zip), unpack it and copy its
`skills/aschecked` folder into your project as the folder named.

| Tool | How to install and run it |
|---|---|
| Cursor | Copy the folder to `.agents/skills/aschecked`. Start Cursor's agent in **Ask** mode (`agent --mode ask`) and type `/aschecked`. |
| Codex (GPT models) | Copy the folder to `.agents/skills/aschecked`. In your project's folder, start `codex --sandbox read-only` and type `$aschecked`. |
| Antigravity (Google) | Copy the folder to `.agents/skills/aschecked`. Start it in plan mode and type `/aschecked`. |
| Cline | Copy the folder to `.claude/skills/aschecked` in your project and use Cline's plan mode (not tried). |
| Lovable | In Account settings, open Personal skills; in the menu beside **Add skill** choose **Import skills**, then GitHub, and paste `https://github.com/hevelius-ai/aschecked/tree/main/skills/aschecked`. In a project, switch to **Chat** mode, type `/aschecked`, choose it and send "Run the aschecked skill on this project." |
| Bolt | Open the project name menu, then **Skills**, **Add skill**, **From GitHub**, and enter `https://github.com/hevelius-ai/aschecked`. Switch to **Plan** mode, type `/aschecked`, choose it and send "Run the aschecked skill on this project." |
| ChatGPT, Gemini or another chat | Upload `paste/aschecked-prompt.md` and your project's zip, and ask it to run the AsChecked review in the prompt file on the project. |

In every tool, use its plan, ask or read-only mode, and allow only commands that read. More on each tool:
[Other tools](docs/other-tools.md).

## More

- [How we tested it](docs/how-we-tested.md).
- [Other ways to install, update or remove it](docs/install-options.md).
- [What read-only covers, and where it stops](docs/git-safety.md).
- [Install and run in a terminal](docs/terminal.md).
- [Other AI tools in detail](docs/other-tools.md).

## Licence

AsChecked is not a security tool. It gives no score, rating or certificate, and its reports come with no warranty,
as the licence says.

(c) 2026 Hevelius AI Group LLC. The method text (`skills/`, `paste/`, `docs/` and this README) is licensed under CC BY
4.0 ([LICENSE](LICENSE)); the join script, tests and configuration under MIT ([LICENSE-CODE](LICENSE-CODE)).

Suggested credit: "AsChecked" by Hevelius AI Group LLC, https://github.com/hevelius-ai/aschecked, licensed under CC BY 4.0.
