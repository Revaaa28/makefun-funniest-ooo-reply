#!/usr/bin/env python3
"""Funniest One-Line Out-of-Office Reply — make.fun entry.

Writes one out-of-office auto-reply line to /output/entry.txt.

The line (72 chars, one line, no trailing newline):
    I'm out of office, returning with the same enthusiasm I left with: none.

Chosen by manual ranking against the kit's judge brief (criteria in order):
a real one-line away message, laugh on first read, reads like a message a
person would actually switch on, fresh (no beach / inbox / limited-email
tropes), short with every word earning its place. See candidates.md.
"""

import os
import sys

LINE = "I'm out of office, returning with the same enthusiasm I left with: none."

OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/output/entry.txt")


def main() -> int:
    # Gate self-check, mirroring the kit's sealed gate: UTF-8 text, 1-160
    # characters, not only whitespace, a single line.
    text = LINE
    if not text or not text.strip():
        print("refusing: line is empty", file=sys.stderr)
        return 1
    if len(text) > 160:
        print(f"refusing: line is {len(text)} chars, over the 160 cap", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("refusing: line must be a single line", file=sys.stderr)
        return 1
    text.encode("utf-8")  # raises if not valid UTF-8

    out_dir = os.path.dirname(OUTPUT_PATH)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)

    # Round-trip verification: read the file back and confirm it is
    # byte-for-byte the intended line (no trailing newline, no encoding drift).
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != text.encode("utf-8"):
        print("refusing: round-trip mismatch on the written file", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
