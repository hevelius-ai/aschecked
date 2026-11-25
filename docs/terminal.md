# Install and run AsChecked in a terminal

Back to the [README](../README.md).

For people who use Claude Code in a terminal. To install Claude Code itself, see https://code.claude.com/docs/en/setup.
These steps follow Claude Code 2.1.330, where a new terminal session starts in Auto mode (Claude Code's documentation:
from version 2.1.283). The bottom of the screen shows the mode, for example "auto mode on" or "plan mode on".

## The three settings

| Model and effort | Start Claude Code with |
|---|---|
| **Claude Fable 5.2, medium (best)** | `claude --model fable --effort medium` |
| Claude Opus 5.5, medium | `claude --model opus --effort medium` |
| Claude Fable 5.2, low | `claude --model fable --effort low` |

## Steps

1. **Open a terminal in your project's folder.** On Windows, right-click inside the folder and choose Open in
   Terminal. On a Mac, right-click the folder in Finder and choose Services, then New Terminal at Folder. If you use git
   branches, type `git checkout` and the name of the version you want checked (for your finished app, usually `main`
   or `master`) and press Enter; if not, skip this.
2. **Start Claude Code.** Type `claude --model fable --effort medium` and press Enter. Without Claude Fable 5.2 in your
   plan, type `claude --model opus --effort medium` instead. If it asks whether you trust this folder, choose
   **Yes**.
3. **First time only: install AsChecked.** If the bottom of the screen shows anything but "auto mode on", press
   Shift+Tab until it does. Copy this message, paste it into Claude Code and press Enter:

   ```
   Install the AsChecked review skill for me. Download
   https://github.com/hevelius-ai/aschecked/archive/refs/tags/v1.0.0.zip into a new temporary folder outside this
   project and unpack it there. Read the files in its skills/aschecked folder and tell me in two sentences what they
   do. Then tell me what you will copy and where, and wait for my yes. After my yes, copy that folder to
   .claude/skills/aschecked in my home folder, replacing any older copy, and delete what you downloaded and unpacked.
   Change nothing else. Finally, check that .claude/skills/aschecked/SKILL.md is in my home folder and say
   "AsChecked is installed".
   ```

   In Auto mode, Claude Code's own automatic check decides which commands run, so it may not ask you. The check that
   waits for you is Claude's question before it copies: type `yes` only if it names your home
   `.claude/skills/aschecked` folder (on Windows `.claude\skills\aschecked`); otherwise type `no`. If Claude Code does
   ask to allow a command, choose the plain **Yes**, not "don't ask again", only when it names the AsChecked
   download, the temporary folder or `.claude/skills/aschecked`; otherwise **No**. Wait for "AsChecked is installed".
   To update AsChecked later, paste this message again: this page always names the newest version.
4. **Choose the mode.** Never start the review with "accept edits on" or "bypass
   permissions on" at the bottom of the screen.
5. **Start the review:** type `/aschecked` and press Enter. If it is not in the list, type `/reload-skills`, press
   Enter and try again. AsChecked only reads your files. If Claude Code asks you to allow something else, or to
   approve a plan, choose **No**.
6. **Answer the three questions**, or say "skip". If part of your app is not built yet, say which part: AsChecked then
   lists the problems in that part separately.
7. **Your report is ready.** If you want to keep it, select it and copy it (Ctrl+Shift+C or right-click and Copy;
   Cmd+C on a Mac) into a text file outside your project's folder. Then pass it to your AI builder to fix what it
   found: each problem comes with a message ready to paste.
