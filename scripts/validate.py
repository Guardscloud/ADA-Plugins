"""Checks index.json and plugin files. --fix-sha rewrites sha256 values. Used by CI on every pull request."""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ID = re.compile(r"^[a-z0-9][a-z0-9-]{1,40}$")
FILE = re.compile(r"^plugins/[a-z0-9][a-z0-9-]{1,40}/[A-Za-z0-9_][A-Za-z0-9_.-]{0,60}\.py$")
CATS = {"security", "productivity", "finance", "writing", "developer", "integration", "other"}
BANNED = [r"\bexec\s*\(", r"\beval\s*\(", r"base64\.b64decode", r"marshal\.loads", r"__import__\s*\(", r"\bpickle\.loads"]


def main() -> int:
    fix = "--fix-sha" in sys.argv
    idx = json.loads((ROOT / "index.json").read_text(encoding="utf-8"))
    errors, seen = [], set()
    for e in idx.get("plugins", []):
        pid = e.get("id", "?")
        where = f"[{pid}]"
        if not ID.match(pid):
            errors.append(f"{where} invalid id")
        if pid in seen:
            errors.append(f"{where} duplicate id")
        seen.add(pid)
        for k in ("name", "description", "version", "author", "file", "category"):
            if not e.get(k):
                errors.append(f"{where} missing {k}")
        for k in ("name", "description"):
            if isinstance(e.get(k), dict) and not e[k].get("en"):
                errors.append(f"{where} {k} needs an 'en' text")
        if e.get("category") not in CATS:
            errors.append(f"{where} unknown category {e.get('category')!r}")
        f = e.get("file", "")
        if not FILE.match(f) or not f.startswith(f"plugins/{pid}/"):
            errors.append(f"{where} file must be plugins/{pid}/<name>.py")
            continue
        p = ROOT / f
        if not p.exists():
            errors.append(f"{where} {f} not found")
            continue
        data = p.read_bytes()
        if len(data) > 256 * 1024:
            errors.append(f"{where} file larger than 256 KB")
        try:
            src = data.decode("utf-8")
            compile(src, f, "exec")
        except (UnicodeDecodeError, SyntaxError) as ex:
            errors.append(f"{where} does not compile: {ex}")
            continue
        for b in BANNED:
            if re.search(b, src):
                errors.append(f"{where} uses a banned construct ({b}); explain it in the PR or remove it")
        sha = hashlib.sha256(data).hexdigest()
        if e.get("sha256") != sha:
            if fix:
                e["sha256"] = sha
            else:
                errors.append(f"{where} sha256 mismatch (run scripts/validate.py --fix-sha)")
    if fix:
        (ROOT / "index.json").write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for err in errors:
        print("ERROR", err)
    print(f"{len(idx.get('plugins', []))} plugins, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
