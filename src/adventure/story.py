# src/adventure/story.py
from __future__ import annotations

import os
import sys
import random
from typing import List

from adventure.utils import read_events_from_file

# Rich formatting
from rich.console import Console
from rich.theme import Theme
from rich.prompt import Prompt


def _colors_disabled_for_tests() -> bool:
    """
    Disable ANSI colors when running under pytest or when stdout isn't a TTY.
    This keeps unit tests stable (no escape codes in captured output).
    """
    running_pytest = os.getenv("PYTEST_CURRENT_TEST") is not None
    not_a_tty = not sys.stdout.isatty()
    return running_pytest or not_a_tty


THEME = Theme(
    {
        "title": "bold",
        "narration": "italic",
        "choice": "bold",
        "hint": "dim",
        "danger": "bold red",
        "success": "bold green",
    }
)

console = Console(theme=THEME, no_color=_colors_disabled_for_tests(), highlight=False)


def step(choice: str, events: List[str]) -> str:
    """
    Decide the next story sentence based on a user's choice and a random event.
    Returns a plain text sentence (no color codes).
    """
    random_event = random.choice(events)

    if choice == "left":
        return left_path(random_event)
    elif choice == "right":
        return right_path(random_event)
    else:
        return "You stand still, unsure what to do. The forest swallows you."


def left_path(event: str) -> str:
    """Sentence for the left path."""
    return "You walk left. " + event


def right_path(event: str) -> str:
    """Sentence for the right path."""
    return "You walk right. " + event


def main() -> None:
    """Run the interactive story loop with styled output."""
    events = read_events_from_file("events.txt")

    console.rule("[title]Adventure[/title]")
    console.print("You wake up in a dark forest. You can go left or right.", style="narration")
    console.print("Choose a direction:", style="hint")
    console.print("  - left", style="choice")
    console.print("  - right", style="choice")
    console.print("  - exit", style="choice")

    while True:
        # Keep the original prompt text exactly to preserve behavior/tests.
        choice = Prompt.ask("Which direction do you choose? (left/right/exit): ").strip().lower()
        if choice == "exit":
            break

        result = step(choice, events)
        style = "success" if result.startswith("You walk") else "danger"
        console.print(result, style=style)

    console.rule("[hint]The End[/hint]")


if __name__ == "__main__":
    main()