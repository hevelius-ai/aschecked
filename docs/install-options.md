# Installing and removing AsChecked in Claude Code

Back to the [README](../README.md).

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
  question (for example when your AI tool runs it for you), it installs nothing. When it installs, it warns that
  skills are not verified by GitHub and asks you to review the installed files: GitHub shows this for every skill.
  The files are in your project's `.claude/skills/aschecked` folder (with `--scope user`, in
  `~/.claude/skills/aschecked` in your home folder) if you want to read them before you start.
- **With the skills command** (needs Node.js): open a terminal in your project's folder and run
  `npx skills add hevelius-ai/aschecked -a claude-code -y`. It puts the skill in `.claude/skills/aschecked` and
  adds a `skills-lock.json` file to your project's folder.

Start Claude Code after installing it: in our tests, a Claude Code session that was already open did not see the
newly installed skill.

**To remove AsChecked:** delete the `aschecked` folder it was installed into (`.claude/skills/aschecked` in your
project, or `~/.claude/skills/aschecked` in your home folder); the GitHub CLI has no uninstall command. If you
installed it with the skills command, run `npx skills remove aschecked` in your project's folder instead, which also
takes it out of `skills-lock.json`.

## A zip of your project

For the chat route you need your project as a zip, from the branch you want reviewed. On GitHub: **Code**, then
**Download ZIP**. In Bolt or Replit, use their download or export. Lovable's own zip download is on paid plans only;
on a free plan, sync your project to GitHub and use GitHub's **Download ZIP**.
