# Other tools

Back to the [README](../README.md).

AsChecked is packaged for, not yet proven in, these tools. In November 2026 we tried it in five of them, on our own test projects; Codex and Cursor also ran in
our sandbox test, and Codex and Antigravity in our full test (see [how we tested](how-we-tested.md)). A tool worked when its report met all our report checks (every required part, and
evidence that matches the files), the review changed no file and it found the most serious known problem. One try
is not proof.

- **Codex** (command line; tried with GPT-6-Luna at medium effort, on two test projects): copy the `skills/aschecked`
  folder (from the downloaded zip; see [install options](install-options.md)) into your project as `.agents/skills/aschecked`, start
  `codex --sandbox read-only` in your project's folder, type `$aschecked` and approve each command that only reads.
  On Windows, Codex first asks how to set up its sandbox (we chose the non-admin sandbox); before that setup, our
  unattended run could not run any command. Tried, not working: both reviews (one on each project) found the most
  serious problem, but one cited a line two lines away from the text it described. In our full test (24 sample
  apps, 110 reviews with GPT-6-Luna at medium effort in its read-only sandbox), 72 of 110 reviews were complete
  and correct, against 112 of 120 for Claude Fable 5.2 at medium effort in Claude Code; it put the most serious
  problem first in 74 of 87 reviews of apps with one. Not yet proven.
- **Cursor** (command line, Auto model, on two test projects): copy the folder into
  `.agents/skills/aschecked`, start Cursor's agent in **Ask** mode (`agent --mode ask`) and type `/aschecked`. In plan
  mode it only wrote a plan and offered to build it. Tried, not working: both reviews (one on each project) found the
  most serious problem, but one gave no effort for any fix. Not yet proven.
- **Antigravity** (command line; tried with Claude Opus 4.6 Thinking, the strongest model it offered, on one test
  project): copy the folder into `.agents/skills/aschecked`, start it in plan mode, type `/aschecked` and approve each
  command that only reads; in that try, its unattended mode stops at the first command. Tried, not working: it found the most
  serious problem but ranked it second. In our full test (Antigravity CLI 1.5.16, Gemini 4 Hydrogen at medium
  effort, in its default mode with its sandbox), 10 reviews ran: 9 of 10 were
  complete and correct, too few to compare. Not yet proven.
- **Devin Desktop, Kilo:** copy the folder into `.agents/skills/aschecked`. Not tried. Not yet proven. Use the tool's plan or read-only mode where it has one.
- **Cline:** copy the folder into `.claude/skills/aschecked` in your project, and use Cline's plan mode. Not tried. Not yet proven.
- **Lovable:** in Account settings, open Personal skills, use the menu beside **Add skill** to choose **Import
  skills**, pick GitHub and paste `https://github.com/hevelius-ai/aschecked/tree/main/skills/aschecked`. Then, in a
  project, switch to **Chat** mode, type `/aschecked`, choose it from the list and send "Run the aschecked skill on
  this project." Tried once, not fully checked, on a new to-do app that Lovable made: the import and the review ran
  and the report had every required part; whether the review changed no file, and how well it finds problems, were
  not checked there (that app has no known problems to compare). Not yet proven.
- **Bolt:** in a project, open the project name menu, then **Skills**, **Add skill**, **From GitHub**, and enter
  `https://github.com/hevelius-ai/aschecked`. Then switch to **Plan** mode, type `/aschecked`, choose it from the list
  and send "Run the aschecked skill on this project." Tried, not working, on a new to-do app that Bolt made: it
  ranked a missing undo above a list anyone on the internet can wipe, and added a reassuring summary after the
  report's closing lines. Bolt keeps the skill inside your project, so the review reported the skill's own
  instructions as project text. Bolt then added a new version to the project's history; whether that changed a file
  was not checked. Not yet proven.
- **Replit:** not tried. Replit documents skills and its Plan mode for paid plans only. Not yet
  proven. On any plan, you can download your project from Replit and use "No Claude Code? Use a claude.ai chat" in the README.
- **Anything else:** paste [`paste/aschecked-prompt.md`](../paste/aschecked-prompt.md) and give it your code. Not yet
  proven.

**Antigravity, tried with an earlier version of the method as a plain prompt:** with Gemini 3.8 Flash it missed all
four known problems in a web app with accounts and called that app's access rules strong; it found two of
five known problems in a desktop app. Claude Sonnet 4.6 in the same tool found one of the four web-app problems.
The installed v1 skill is the one tried in the list above.
