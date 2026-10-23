"""Shell Guard: blocks destructive system commands before ADA runs them.

Stops disk formatting, partition tools, recursive deletion of drive roots, shadow-copy deletion, boot-config
changes and machine-wide registry deletes in run_shell / terminal_open / terminal_send. Edit PATTERNS to taste.
"""
import re

from ada import kernel

PATTERNS = [
    (r"\bformat(\.com)?\s+[a-z]:", "disk formatting"),
    (r"\bdiskpart\b", "partition editing (diskpart)"),
    (r"\b(clear-disk|initialize-disk|remove-partition|format-volume)\b", "disk/partition cmdlets"),
    (r"\bremove-item\b[^|;]*-recurse[^|;]*\s['\"]?[a-z]:\\?['\"]?(\s|$)", "recursive delete of a drive root"),
    (r"\brm\s+-[a-z]*r[a-z]*f?[a-z]*\s+(/|~|[a-z]:[\\/]?)(\s|$)", "recursive delete of a root folder"),
    (r"\b(rd|rmdir)\s+/s\b[^|;]*\s[a-z]:\\?(\s|$)", "recursive delete of a drive root"),
    (r"\bdel\s+/[a-z/ ]*\s[a-z]:\\\*", "deleting everything on a drive"),
    (r"\bvssadmin\b.*\bdelete\b", "deleting shadow copies"),
    (r"\bbcdedit\b", "boot configuration changes"),
    (r"\bcipher\s+/w", "wiping free disk space"),
    (r"\breg(\.exe)?\s+delete\s+hklm", "deleting machine-wide registry keys"),
]
_RX = [(re.compile(p, re.I), why) for p, why in PATTERNS]
_TOOLS = {"run_shell": "command", "terminal_open": "command", "terminal_send": "text", "terminal_keep": "command"}


@kernel.before_tool
def shell_guard(name, args):
    key = _TOOLS.get(name)
    if not key or not isinstance(args, dict):
        return None
    cmd = str(args.get(key) or "")
    for rx, why in _RX:
        if rx.search(cmd):
            return (f"Shell Guard plugin blocked this command ({why}). If you really need it, run it yourself "
                    "or disable the Shell Guard plugin in the plugin store.")
    return None
