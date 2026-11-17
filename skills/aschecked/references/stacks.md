# Stack checklists

Detail for the stack core rules in SKILL.md. Use a section only when its stack is present. Each item is something to check with evidence (file and line, or the search you ran), not something to assume. The hard limits in SKILL.md still apply: read only, values never shown.

## Supabase

- **Replay the rules, do not read them one by one.** List every migration in order. For each table, write down the policies and grants that are in force after the last migration, per action: select, insert, update, delete. A later migration that drops, replaces or re-creates a policy wins over an earlier one.
- **Insert and update need a column check.** A policy that checks only `auth.uid() = user_id` still lets a user set every other column they are granted: role, workspace or team id, owner, plan, price. Compare the column grants with what the policy checks. "Can a new account add itself to someone else's workspace, or give itself a higher role?" is the question.
- **Row level security on every table** that holds user data; a table without it is open to anyone with the public key.
- **Functions:** `security definer` functions run with the owner's rights; check who can call them and that they check the caller. Check `search_path` is set.
- **Storage buckets:** public buckets, and policies on `storage.objects`.
- **Keys:** the anon or publishable key is public by design; a service-role or secret key in client code, in the app bundle or in a public repository is not.
- **Comments and screens that claim a protection** ("the grant prevents this", "only managers can") are checked against the replayed rules.
- **Trace:** who changed or deleted a row, and is there a history or audit table the app writes to.

## Firebase

- **Rules files** (`firestore.rules`, `database.rules.json`, `storage.rules`): find any `allow read, write: if true`, rules that check only `request.auth != null`, and test-mode rules (`if request.time < timestamp.date(...)`): they are open to everyone until that date, so a date still ahead means the data is open now (after the date they refuse everything, which breaks the app instead).
- **Writes:** can a user write `role`, `admin`, `isPaid` or another user's document? Check the rule restricts the fields written (`request.resource.data`), not only the path.
- **Server code:** Cloud Functions that use the Admin SDK bypass the rules; check they check the caller.
- **Keys:** the web config `apiKey` is public by design; a service-account JSON in the project is not.

## Electron

- **Renderer:** `sandbox: true`, `contextIsolation: true`, `nodeIntegration: false` on every window, including ones opened later; no remote content loaded with Node access.
- **Messages to the main process:** each `ipcMain` handler checks the sender (frame URL or origin) and the arguments; the preload exposes narrow functions, not `ipcRenderer` itself.
- **Fuses:** `RunAsNode`, `EnableNodeOptionsEnvironmentVariable`, `EnableNodeCliInspectArguments` off, ASAR integrity on. This matters most when the app holds device permissions (Full Disk Access, camera, accessibility): without fuses another local program can start the app's binary as plain Node and borrow those permissions.
- **Updates:** downloaded updates checked by signature or checksum before install; no quarantine flag removed by hand; the update feed served over HTTPS from a source the owner controls.
- **Signing and notarisation** on macOS and Windows, and whether the README tells users to bypass the system's warning.
- **Local data:** what is written to disk (tokens, cookies, chat history), in plain text or the system keychain.

## CI and automation

- **Job rights:** a top-level `permissions:` block, read-only by default; write rights only on the job that needs them.
- **Untrusted code:** `pull_request_target` and `workflow_run` jobs that check out the pull request's code; steps that put issue, comment or branch text straight into a shell (`${{ github.event... }}` inside `run:`); self-hosted runners on public repositories.
- **Pinning:** third-party actions pinned by full commit, not a tag; tools downloaded in CI checked by hash; users told to fetch the project by a tag that can move.
- **Secrets:** which secrets a job can reach, and whether a job that runs untrusted code is one of them; `persist-credentials` left on after checkout.
- **Automations outside GitHub** (n8n, Zapier, Make exports, cron scripts): stored credentials, webhooks with no secret, and steps that act without a person confirming.
