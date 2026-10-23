# Contributing a plugin

1. **Fork** this repository.
2. Create `plugins/<id>/plugin.py`. The id is lowercase letters, digits and dashes (`my-plugin`).
   Start the file with a docstring that says what the plugin does.
3. Add an entry to `index.json`:

```json
{
  "id": "my-plugin",
  "name": {"en": "My Plugin", "tr": "Eklentim"},
  "description": {"en": "One sentence about what it does.", "tr": "Ne yaptığını anlatan tek cümle."},
  "version": "1.0.0",
  "author": "your-github-name",
  "category": "productivity",
  "tags": ["files"],
  "tools": ["my_tool"],
  "hooks": [],
  "api": 1,
  "min_ada": "0.6.0",
  "verified": false,
  "file": "plugins/my-plugin/plugin.py",
  "sha256": "",
  "homepage": "https://github.com/Guardscloud/ADA-Plugins/tree/main/plugins/my-plugin"
}
```

4. Run `python scripts/validate.py --fix-sha` (fills in `sha256` and checks everything).
5. Open a pull request. A maintainer reviews the code and sets `"verified": true` when merging.

**Categories:** `security`, `productivity`, `finance`, `writing`, `developer`, `integration`, `other`.

## Review rules

- No obfuscated code, no downloading and running other code, no telemetry.
- Network access only to the service the plugin is about, and it must be stated in the description.
- No reading browser profiles, password stores, SSH keys or other secrets.
- `before_tool` hooks may block or tighten calls; they must not silently widen what ADA is allowed to do.
- Every change to a plugin bumps its `version`.
