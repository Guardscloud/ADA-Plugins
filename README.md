# ADA Plugin Store

Plugins for [ADA](https://github.com/Guardscloud/ADA), the AI coworker that runs on your desktop.
ADA reads [`index.json`](index.json) from this repository and shows these plugins in its **Plugin store**
(Control menu → Plugin store, or type `/plugins` in the chat box). One click installs a plugin into
`%APPDATA%\ADA\kernel\plugins\`; restart ADA and it is active.

| Plugin | What it does |
|---|---|
| Shell Guard | Blocks destructive commands (disk formatting, diskpart, deleting drive roots…) before ADA runs them |
| TCMB Exchange Rates | Tool for today's official Central Bank of Turkey exchange rates |
| Text Stats | Exact word/character/sentence counts, reading time, frequent words |
| Password Generator | Strong passwords and passphrases from a secure generator |
| Tool Audit CSV | Logs every tool call ADA makes to a CSV you can open in Excel |
| Dated Filenames | ADA starts every file it creates with today's date |

## How safe is this?

A plugin is ordinary Python code that runs with **your** permissions, so:

- Every plugin here is reviewed before it is merged and listed (`"verified": true`).
- ADA downloads plugin files **only from this repository** and checks each file's SHA-256 against `index.json`
  before installing. A file that does not match is rejected.
- In the store you can read a plugin's full source code before installing it.
- Plugins cannot bypass ADA's own safety chain (input validation, limits, approvals, action log).
- If you edit an installed plugin, updates will not silently overwrite your changes.

## Submit a plugin

See [CONTRIBUTING.md](CONTRIBUTING.md). In short: add `plugins/<id>/plugin.py`, add an entry to `index.json`,
run `python scripts/validate.py --fix-sha`, open a pull request.

## Writing plugins

The plugin API (`@kernel.tool`, `@kernel.before_tool`, `@kernel.after_tool`, `@kernel.system`) is documented in
[ADA's KERNEL.md](https://github.com/Guardscloud/ADA/blob/main/docs/KERNEL.md).

Licensed under MIT.
