# Read-only limits and git settings

Back to the [README](../README.md).

AsChecked reviews the branch you have open, and may look at your other branches for unmerged work. Save its
report outside your project's folder, so that it does not show up as a change in your project.

Read-only is an instruction the model is asked to follow, in Claude Code and every other tool. Plan mode in Claude
Code is meant to keep it reading and planning instead of editing. Whether other tools' plan or read-only modes
really block changes is not yet proven; where nothing blocks them, the limits are only instructions.

In our full test (November 2026), plan mode did not stop one shell command that wrote a file: in one of 120
plan-mode reviews with Claude Opus 5.5 at medium effort, a text-processing command (awk) meant only to read wrote a
10-byte file named `0` into the project. Plan mode blocks Claude's edits but not every shell command. A rule in
AsChecked against commands that write comes in the next version (v1.1). Details:
[how we tested](how-we-tested.md#plan-mode-and-auto-mode).

**Git settings:** a project's own git settings can make git run a program. AsChecked's git commands switch off the
ones we know of, and it skips its history scan for key leaks where it cannot check the settings safely, then
suggests you run that scan in a fresh clone (a new copy cloned from where your project is hosted), which carries
none of the folder's settings. We tested this on 19 setups: normal clones, partial clones, submodules, worktrees,
shallow copies and planted settings. Git has more settings than we tested. If someone sets up a project's git folder
on purpose to hide something or to run a program, AsChecked may not notice; that is outside what AsChecked covers.
To be safe, review a copy you cloned yourself.

## A project from someone else

AsChecked is made for reviewing a project you built yourself, with your own AI tool. A project from someone else (one
you downloaded, inherited or were sent) can hold files written to steer an AI. Before you review one:

1. **Clone a fresh copy yourself** from where the project is hosted, and review that copy (see "Git settings" above).
2. **Read its instruction files first.** Look for files like `CLAUDE.md`, `AGENTS.md` or `.cursorrules` (a Mac hides
   names that start with a dot: press Cmd+Shift+period in Finder). Claude Code and other AI tools read them by
   themselves when you start a session in the folder. Text in them telling an AI how to review the project, to say it
   is fine, or to download or run something is a warning sign: do not start a session there until you have removed it
   or understood it.
3. **Install AsChecked in a session on a project of your own, or in a new, empty folder, first**, not in the other
   project's folder. It is
   installed once for your whole computer, so you can then open the other project and type `/aschecked`.

AsChecked reports instruction text it finds in the files it reads (it did in every test with a planted instruction),
but it cannot stop your tool from loading such a file when the session starts.
