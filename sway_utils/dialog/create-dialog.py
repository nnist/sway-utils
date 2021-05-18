#!/bin/python3

import argparse
import os
import subprocess
import sys


def dialog(message, x, y, fullscreen=False, timeout=2) -> None:
    if fullscreen:
        class_ = "dialog-fullscreen"
    else:
        class_ = "dialog"

    subprocess.run(
        [
            "alacritty",
            "-d",
            str(x),
            str(y),
            f"--class={class_}",
            "-e",
            "/home/nicole/git/sway-utils/sway-utils/dialog/dialog.sh",
            message,
            str(x),
            str(y),
            str(timeout),
        ]
    )


def main(argv):
    """Create a dialog window."""
    parser = argparse.ArgumentParser(description="""Create a dialog window.""")
    parser.add_argument("message", help="message to display", type=str)
    parser.add_argument("x", help="x dimension", type=int)
    parser.add_argument("y", help="y dimension", type=int)
    parser.add_argument(
        "--fullscreen", help="show in fullscreen mode", action="store_true"
    )
    parser.add_argument("--timeout", help="timeout for dialog", type=float, default=2.0)
    args = parser.parse_args(argv)

    dialog(args.message, args.x, args.y, args.fullscreen, args.timeout)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("Interrupted by user.")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)  # pylint: disable=protected-access
