"""Tool Audit CSV: writes every tool call ADA makes to a CSV file you can open in Excel.

File: %APPDATA%\\ADA\\kernel\\tool_audit.csv (time, tool, summary, error, seconds-free). Inputs are shortened
to 200 characters; text typed with the keyboard tool and email bodies are not recorded.
"""
import csv
import json
from datetime import datetime

from ada import config, kernel

PATH = config.HOME_DIR / "kernel" / "tool_audit.csv"
_SKIP_KEYS = {"text", "body", "content", "markdown", "code"}


def _summary(args) -> str:
    if not isinstance(args, dict):
        return str(args)[:200]
    safe = {k: v for k, v in args.items() if k not in _SKIP_KEYS}
    return json.dumps(safe, ensure_ascii=False, default=str)[:200]


@kernel.after_tool
def audit(name, args, result):
    new = not PATH.exists()
    PATH.parent.mkdir(parents=True, exist_ok=True)
    with PATH.open("a", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["time", "tool", "input", "error"])
        w.writerow([datetime.now().isoformat(timespec="seconds"), name, _summary(args),
                    "yes" if getattr(result, "is_error", False) else ""])
    return None
