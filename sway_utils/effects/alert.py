#!/bin/python3

import argparse
import sys
import time
from dataclasses import dataclass
from typing import List

from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live


@dataclass
class Frame:
    text: str
    delay: float


def render(message: str, style: str):
    console = Console()
    console.clear()

    length = len(message)
    margin = 3
    msg = " " * margin + message + " " * margin
    empty = " " * margin + " " * length + " " * margin
    lines = "─" * (length + 6)
    panel_lines = "─" * (length + 4)
    top_blocks = "▄" * (length + 4)
    mid_blocks = "█" * (length + 4)
    bot_blocks = "▀" * (length + 4)

    FRAMES: List[Frame] = [
        Frame(
            f"""[{style}]
{empty}
{empty}
{lines}""",
            0.1,
        ),
        Frame(
            f"""[{style}]
{empty}
{msg}
{lines}""",
            0.1,
        ),
        Frame(
            f"""[{style}]
┌{panel_lines}┐
{msg}
└{panel_lines}┘""",
            0.03,
        ),
        Frame(
            f"""[{style}]
┌{panel_lines}┐
{msg}
└{panel_lines}┘""",
            0.05,
        ),
        Frame(
            f"""[{style}]
▗{top_blocks}▖
▐{mid_blocks}▌
▝{bot_blocks}▘""",
            0.18,
        ),
        Frame(
            f"""[{style}]
┌{panel_lines}┐
[bold]{msg}[not bold]
└{panel_lines}┘""",
            0.6,
        ),
    ]

    with Live(Align("", align="center"), refresh_per_second=60, transient=True) as live:
        for frame in FRAMES:
            live.update(Layout(Align(frame.text, align="center", vertical="middle")))
            time.sleep(frame.delay)


def main(argv):
    """Display a dialog window."""
    parser = argparse.ArgumentParser(description="""Display a dialog window.""")
    parser.add_argument("message", help="message to display", type=str)
    parser.add_argument("style", help="style (color) to use", type=str)
    args = parser.parse_args(argv)

    render(args.message, args.style)


if __name__ == "__main__":
    main(sys.argv[1:])
