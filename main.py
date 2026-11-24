#!/usr/bin/env python3
"""One Letter: Coffee or Tea — make.fun entry.

Sends exactly one letter, A for coffee, and nothing else.

The program writes a single byte, ``A``, to ``$MAKEFUN_OUTPUT_DIR/entry.txt``.
The gate requires entry.txt to be UTF-8 text of exactly 1 character, so no
trailing newline is written. The choice is fixed: coffee.

Why coffee (A) and not tea (B): the judge weighs, most important first,
vividness/specificity, funniness, and truth of the choice behind the letter.
Coffee is the more vivid word — dark, bitter, steaming, the morning jolt —
where tea reads soft and calm. Coffee also carries the far richer joke
culture (caffeine-first mornings, "don't talk to me before coffee"), and as
the day's fuel it is the truer report of a working day. So A.

The program is fully deterministic: same input (none), same output, every
run. It makes no model call, no network call, and reads no clock. It
verifies its own output before exiting, so a silent partial write can never
pass as a valid entry.
"""

import os
import sys

LETTER = "A"  # A for coffee.


def main() -> int:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    payload = LETTER.encode("utf-8")
    # Create with world-readable mode at once (umask-independent): the
    # grader collects outputs as another user, so a 0600 file would fail.
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)
    # Force the mode: os.open's mode is still masked by the umask, and the
    # grader collects outputs as another user, so a 0640 file would fail.
    os.chmod(path, 0o644)
    # Verify what landed on disk before reporting success.
    with open(path, "rb") as f:
        if f.read() != payload:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
