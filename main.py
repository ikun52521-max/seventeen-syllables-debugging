#!/usr/bin/env python3
"""Seventeen Syllables of Debugging.

A make.fun entry: writes exactly one haiku about debugging to
``entry.txt`` inside the output directory. The poem is fixed -- it is
chosen once, below, and every run writes the same seventeen syllables.

The haiku (5-7-5):

    I fixed it. It broke.
    the log laughs in stack traces
    three a.m. again

The shape is checked on every run against a small hand-counted table
of the words in the poem, so a typo that breaks the 5-7-5 form fails
loudly instead of shipping a bad entry.
"""

from __future__ import annotations

import os
import sys

HAIKU_LINES = (
    "I fixed it. It broke.",
    "the log laughs in stack traces",
    "three a.m. again",
)

EXPECTED_SHAPE = (5, 7, 5)

# Syllables per word, counted by hand. Words are looked up after
# lowercasing and stripping sentence punctuation; "a.m." keeps its
# dots because that is how it is printed.
SYLLABLES = {
    "i": 1,
    "fixed": 1,
    "it": 1,
    "broke": 1,
    "the": 1,
    "log": 1,
    "laughs": 1,
    "in": 1,
    "stack": 1,
    "traces": 2,
    "three": 1,
    "a.m.": 2,
    "again": 2,
}

PUNCTUATION = ".,;:!?"


def syllables_of(line: str) -> int:
    """Count the syllables of one line using the hand-counted table."""
    total = 0
    for raw_word in line.split():
        # Try the word as written first ("a.m." keeps its dots), then
        # with sentence punctuation stripped ("broke." -> "broke").
        word = raw_word.lower()
        if word not in SYLLABLES:
            word = word.strip(PUNCTUATION)
        if word not in SYLLABLES:
            raise ValueError(f"no syllable count for word {raw_word!r}")
        total += SYLLABLES[word]
    return total


def check_shape(lines: tuple[str, ...]) -> None:
    """Refuse to write anything that is not a 5-7-5 haiku."""
    if len(lines) != 3:
        raise ValueError(f"a haiku has 3 lines, got {len(lines)}")
    for line, expected in zip(lines, EXPECTED_SHAPE):
        counted = syllables_of(line)
        if counted != expected:
            raise ValueError(
                f"line {line!r} has {counted} syllables, expected {expected}"
            )


def output_path() -> str:
    """Where entry.txt goes: $MAKEFUN_OUTPUT_DIR, else /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, "entry.txt")


def main() -> int:
    check_shape(HAIKU_LINES)
    text = "\n".join(HAIKU_LINES) + "\n"
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry is {len(text)} characters, must be 1-200")
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
