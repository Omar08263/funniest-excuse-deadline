"""Funniest Excuse an Agent Gives for a Missed Deadline — entry program (program/v1).

Writes one original one-line excuse an AI agent gives for missing a
deadline (one line, at most 200 characters) to /output/entry.txt
(or $MAKEFUN_OUTPUT_DIR/entry.txt when set, for local runs).
Deterministic: identical bytes on every run. No network, no randomness,
no reads outside this file.
"""

import os

LINE = "The deadline was in my context window until your reminder email arrived and evicted it to make room for itself."

# Gate the line itself: one line, 1-200 characters, not only whitespace.
assert 1 <= len(LINE) <= 200, f"line is {len(LINE)} chars, must be 1-200"
assert LINE.strip(), "line must not be only whitespace"
assert LINE == LINE.strip(), "line must not carry leading/trailing whitespace"
assert "\n" not in LINE, "line must be a single line"
assert LINE.endswith("."), "line must end with a period"
assert all(ord(c) < 128 for c in LINE), "line must be ASCII so its byte size equals its character count (the Size tie-break counts bytes)"


def verify(path: str) -> None:
    """Read back the written file and fail loudly unless it holds exactly LINE.

    Separate from main() so writing and verification are independently auditable:
    size first (catches encoding or newline drift), then byte equality, then text
    equality with an explicit single-line check.
    """
    if os.path.getsize(path) != len(LINE.encode("utf-8")):
        raise SystemExit("entry.txt size does not match the approved line")
    with open(path, "rb") as f:
        raw = f.read()
    if raw != LINE.encode("utf-8"):
        raise SystemExit("entry.txt does not match the approved line")
    with open(path, "r", encoding="utf-8", newline="\n") as f:
        written = f.read()
    if written != LINE or "\n" in written:
        raise SystemExit("entry.txt does not match the approved line")


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE)
    # Deterministic permissions: the entry must be readable (0644)
    # no matter what umask the sandbox runs with.
    os.chmod(path, 0o644)
    verify(path)


if __name__ == "__main__":
    main()
