import subprocess
import sys
import os
import re
from pathlib import Path

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

def strip_ansi(s: str) -> str:
    return ANSI_RE.sub("", s)

def is_prompt_line(s: str) -> bool:
    """
    Detect the Rich prompt (after ANSI stripped), e.g.:
    'Which direction do you choose? (left/right/exit): '
    """
    return "Which direction do you choose" in s and "(left/right/exit):" in s

def test_exit_message():
    """Ensure the script outputs a goodbye message after user inputs 'exit'."""
    script_path = Path("src/adventure/story.py").resolve()
    
    env = os.environ.copy()
    # Tell Rich to always emit ANSI codes even if not a TTY
    env["FORCE_COLOR"] = "1"
    env["TERM"] = "xterm-256color"

    # Run script with sample input
    process = subprocess.run(
        [sys.executable, str(script_path)],
        input="left\nright\nexit\n",
        text=True,
        capture_output=True,
        env=env,
    )

    stdout = [line for line in process.stdout.splitlines() if line.strip()]
    
    # Sanity check: ensure script ran
    assert len(stdout) > 0, "No output captured from story.py"
    print(stdout)

    # Make ANSI-free copies for matching
    clean_lines = [strip_ansi(l) for l in stdout]
    clean_lines = [line for line in clean_lines if line.strip()]

    # Find the index of the LAST prompt
    last_prompt_idx = None
    for i, line in enumerate(clean_lines):
        if is_prompt_line(line):
            last_prompt_idx = i

    assert last_prompt_idx is not None, "No prompt found in output"

    # After the final prompt, there must be some printed message before program ends.
    # This message maybe on the SAME line or on the NEXT line.
    tail_after_colon = ""
    if ": " in clean_lines[last_prompt_idx]:
        tail_after_colon = clean_lines[last_prompt_idx].split(": ", 1)[1]

    has_same_line_output = bool(tail_after_colon.strip())
    has_next_line_output = last_prompt_idx + 1 < len(clean_lines)

    assert has_same_line_output or has_next_line_output, (
        "No message printed after the final prompt. "
        "Expected a goodbye (or any final output) before the program ends."
    )