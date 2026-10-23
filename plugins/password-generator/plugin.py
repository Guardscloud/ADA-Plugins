"""Password Generator: strong random passwords and passphrases (Python `secrets`, cryptographically secure).

Adds the tool `generate_password`. Nothing is stored or logged by the plugin.
"""
import secrets
import string

from ada import kernel

_WORDS = ("amber anchor apple arrow aspen atlas autumn badge bamboo basil beacon birch blossom breeze bronze "
          "cactus canyon carbon cedar cherry cobalt comet copper coral cosmos cotton crystal dawn delta desert "
          "ember falcon fern fjord flame forest frost galaxy garnet glacier granite harbor hazel horizon indigo "
          "island ivory jade jasmine jungle kayak lagoon lantern lemon lilac lotus lunar maple marble meadow "
          "mercury meteor mint mist monsoon nectar nova oasis ocean olive onyx orbit orchid pebble pepper pine "
          "planet plaza prism quartz quill radar raven reef river ruby saffron sage sapphire shadow silver "
          "sketch solar spruce storm summit sunset thunder tiger topaz tundra velvet violet walnut willow zephyr").split()


def make(length: int = 16, symbols: bool = True, words: int = 0) -> str:
    if words:
        return "-".join(secrets.choice(_WORDS) for _ in range(words)) + "-" + str(secrets.randbelow(90) + 10)
    pools = [string.ascii_lowercase, string.ascii_uppercase, string.digits] + (["!@#$%&*?-_=+"] if symbols else [])
    alphabet = "".join(pools)
    while True:
        pw = "".join(secrets.choice(alphabet) for _ in range(length))
        if all(any(c in p for c in pw) for p in pools):
            return pw


@kernel.tool(
    "generate_password",
    "Generate strong random passwords (or memorable passphrases) with a cryptographically secure generator.",
    {
        "length": {"type": "integer", "description": "Characters per password, 8-128 (default 16)"},
        "count": {"type": "integer", "description": "How many (default 1, max 20)"},
        "symbols": {"type": "boolean", "description": "Include symbols (default true)"},
        "passphrase_words": {"type": "integer", "description": "If > 0, make a passphrase of this many words instead"},
    },
)
def generate_password(length: int = 16, count: int = 1, symbols: bool = True, passphrase_words: int = 0) -> str:
    length = max(8, min(int(length or 16), 128))
    count = max(1, min(int(count or 1), 20))
    words = max(0, min(int(passphrase_words or 0), 12))
    return "\n".join(make(length, bool(symbols), words) for _ in range(count))
