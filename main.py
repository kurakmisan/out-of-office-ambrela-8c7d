"""Funniest One-Line Out-of-Office Reply — make.fun bounty entry.

Writes one out-of-office email auto-reply, a single line of text, to
``/output/entry.txt`` (or ``$OOO_OUTPUT_DIR/entry.txt``) and to stdout.

The entry must be UTF-8 text of 1-160 characters, not only white space
(the sealed scorer's gate). ``entry_text()`` enforces it as five
separate checks, each naming the rule it enforces. Ten original
candidates are kept below and ``PICK`` selects the one that is
submitted. The picked line is 93 characters of plain ASCII.
"""

import os
import sys

# Ten original one-line out-of-office replies, drafted for this bounty.
# Each is a self-contained away message a real person could switch on;
# the joke is a turn on the usual away message, not the beach / inbox /
# limited-email lines, and the punchline lands at the end.
CANDIDATES = [
    # 0 — the pick: a turn on the standard auto-acknowledgement
    # ("your email has been received"). The filing category is the joke,
    # and "until Monday" lands it. Reads like a real message a person
    # would gladly switch on before going away.
    "Your email has been received and filed under 'things I'll pretend "
    "I didn't see until Monday'.",
    # 1 — triple beat: inbox open, laptop closed, brain on airplane mode.
    "I'm on leave. My inbox is open, my laptop is closed, and my brain "
    "is on airplane mode.",
    # 2 — the inbox gets a promotion while its owner is away.
    "Out of office \u2014 I've left my inbox in charge, and it has already "
    "promoted itself.",
    # 3 — the email itself is on holiday, and hides it better than I do.
    "I'm away until the 30th \u2014 my email is on holiday too, it's just "
    "better at hiding it.",
    # 4 — the inbox is in the care of a houseplant with questions.
    "I'm away. My inbox is being looked after by a plant, and the plant "
    "has questions.",
    # 5 — the auto-reply itself is doing the work.
    "I'm out until Monday. My out-of-office reply is doing more work than "
    "I am, and it knows it.",
    # 6 — a turn on "your message is important to me".
    "Your message is important to me, which is why I've left it unread "
    "until Monday.",
    # 7 — the inbox is on a strict diet.
    "I'm away; my inbox is on a strict diet \u2014 one email a day, and it "
    "has already eaten.",
    # 8 — the inbox is closed for renovations.
    "Out of office until Monday. My inbox is closed for renovations; "
    "please use the side entrance (me, later).",
    # 9 — the inbox starts talking to itself.
    "I'm on leave \u2014 my laptop is off, my phone is on silent, and my "
    "inbox is talking to itself.",
]

PICK = 0

MAX_CHARS = 160


def entry_text():
    """Return the picked one-line out-of-office reply.

    The gate is the sealed scorer's — UTF-8 text of 1-160 characters,
    not only white space — enforced as five separate checks, each naming
    the rule it enforces so a failure is diagnosable:

    1. ``PICK`` must name one of the candidates.
    2. The line must not be empty after whitespace normalisation.
    3. The line must be a single line: no control characters.
    4. The line must be plain ASCII.
    5. The line must be 1-160 characters long.
    """
    if not 0 <= PICK < len(CANDIDATES):
        raise ValueError(
            "PICK index %d out of range for %d candidates" % (PICK, len(CANDIDATES))
        )
    line = CANDIDATES[PICK]
    if not line.strip():
        raise ValueError("entry is empty after whitespace normalisation")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in line):
        raise ValueError(
            "entry must be a single line without control characters"
        )
    try:
        line.encode("ascii")
    except UnicodeEncodeError:
        raise ValueError("entry must be plain ASCII")
    if not 1 <= len(line) <= MAX_CHARS:
        raise ValueError(
            "entry must be 1-%d characters, got %d" % (MAX_CHARS, len(line))
        )
    return line


def main():
    line = entry_text()
    out_dir = os.environ.get("OOO_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    sys.stdout.write(line + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
