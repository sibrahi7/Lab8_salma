import subprocess
import sys
import os
import re
from pathlib import Path

def test_bold_prompt():
    """Run the story.py script and ensure color codes appear in output."""
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
    
    stdout = process.stdout
    pattern = re.compile(r"\x1b\[1mWhich direction do you choose.*\x1b\[", re.DOTALL)
    if not pattern.search(stdout):
        pattern = re.compile(r"\x1b\[1;[0-9;]*mWhich direction do you choose.*\x1b\[", re.DOTALL)
        if not pattern.search(stdout):
            pattern = re.compile(r"\x1b\[1;[0-9;]*[0-9]*mWhich direction do you choose.*\x1b\[", re.DOTALL)
            assert pattern.search(stdout)
