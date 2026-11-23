# Read-only limits and git settings

Back to the [README](../README.md).

AsChecked reviews the branch you have open, and may look at your other branches for unmerged work. Save its
report outside your project's folder, so that it does not show up as a change in your project.

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
