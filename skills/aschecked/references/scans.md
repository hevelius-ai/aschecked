# Scans

Which scanners to suggest under "Scans to run yourself", by stack and platform, and the traps in reading their output. Run a scanner during the review only if it is already installed, from outside the project, as SKILL.md says; never install one.

## Suggest by stack and platform

Pick two to four that fit the project, each with one line on what it adds.

| Stack or platform | Scan | What it adds |
|---|---|---|
| Any GitHub repository | GitHub secret scanning and push protection (repository settings, Security) | Finds keys in the whole history and blocks new ones on push |
| Any GitHub repository | Dependabot alerts | Known-vulnerable packages, with a pull request to update |
| Any project with a lock file | `osv-scanner` | Known-vulnerable packages from the OSV database, across npm, PyPI, Go, Rust and others |
| Any project | `gitleaks` with `--redact` | Keys in the files and the history, with values hidden |
| Supabase | Supabase Security Advisor and Performance Advisor (dashboard) | Tables without row level security, risky functions, exposed views |
| Firebase | Rules Playground (Firebase console, Rules tab) | Tries a read or write as a given user against the live rules |
| Lovable | Lovable's Security view: the Quick scan runs on publish; run the Deep scan too | Checks the code and the live database settings; the Deep scan also reviews the app's own permissions logic |
| Electron | `npx @electron/fuses read --app <built app>`; the platform's signature check (`codesign -dv`, Windows file properties) | Shows which fuses are on and whether the build is signed |
| Bolt, Replit, other builders | The platform's own security or deployment check, where it has one | Platform-specific settings the code does not show |
| npm projects | `npm audit --package-lock-only --ignore-scripts` | Known-vulnerable packages; sends the package list to npm |
| GitHub Actions | `zizmor` | Risky workflow patterns: untrusted input in shells, unpinned actions, broad rights |
| Web app in production | Mozilla HTTP Observatory | Security headers and HTTPS settings of the live site |

## Traps

- **Build-only noise:** most `npm audit` findings are in development tools that never reach users. Say which are which instead of passing on a count.
- **Public-by-design keys:** a Supabase anon or publishable key, a Firebase web `apiKey`, a Stripe publishable key are meant to be in the client. Name them as public by design; the question is what the rules let that key do.
- **A clean scan is not a clean bill:** scanners do not read access rules, business logic or claims on screen. Never write that a scan found nothing as a sign the project is fine.
- **Scanners read their settings from the scanned folder:** a project's own `.gitleaks.toml` or `.gitleaksignore` can hide findings. Say when one is present.
- **Values:** never paste a scanner's raw output that shows a value. gitleaks only with `--redact`.
- **Sending data out:** `npm audit` and an online `osv-scanner` send the package list (not the code) to an outside service; say so in the report.
