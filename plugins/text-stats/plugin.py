"""Text Stats: word, character and sentence counts, reading time and most frequent words.

Adds the tool `text_stats`. Works for any language; counts are exact (no model guessing).
"""
import re
from collections import Counter

from ada import kernel

_STOP = set("""a an the and or of to in on for is are was were be it this that with as at by from
ve veya ile bir bu şu da de ki için gibi çok daha en ama ya mi mı mu mü olarak olan""".split())


def stats(text: str, top: int = 10) -> str:
    words = re.findall(r"[^\W\d_]+(?:['’-][^\W\d_]+)*", text)
    sentences = [s for s in re.split(r"(?<=[.!?…])\s+", text.strip()) if s.strip()]
    low = [w.replace("İ", "i").lower() for w in words]  # Türkçe İ → i (i̇ değil)
    freq = Counter(w for w in low if w not in _STOP and len(w) > 2)
    minutes = len(words) / 220
    no_space = len(re.sub(r"\s", "", text))
    paragraphs = len([p for p in re.split(r"\n\s*\n", text) if p.strip()])
    lines = [
        f"Words: {len(words)}",
        f"Characters: {len(text)} (without spaces: {no_space})",
        f"Sentences: {len(sentences)}",
        f"Paragraphs: {paragraphs}",
        f"Average words per sentence: {len(words) / len(sentences):.1f}" if sentences else "Average words per sentence: 0",
        f"Reading time: ~{max(1, round(minutes))} min" if words else "Reading time: 0 min",
    ]
    if freq:
        lines.append("Most frequent: " + ", ".join(f"{w} ({n})" for w, n in freq.most_common(top)))
    return "\n".join(lines)


@kernel.tool(
    "text_stats",
    "Exact statistics for a text: words, characters, sentences, paragraphs, reading time, most frequent words.",
    {"text": {"type": "string"}, "top": {"type": "integer", "description": "How many frequent words (default 10)"}},
    required=["text"],
)
def text_stats(text: str, top: int = 10) -> str:
    return stats(text, max(1, min(int(top or 10), 50)))
