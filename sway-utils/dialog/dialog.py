#!/bin/python3

import argparse
import os
import sys
import time


def dialog(message, x, y, timeout=2) -> None:
    length = len(message)
    lines = "═" * length
    spaces = " " * length
    x = int(x) / 2 - length / 2 - 4
    margin = " " * int(x)

    for i in range(int(y / 2)):
        print("")

    print(
        f"""
{margin}╔═══{lines}═══╗
{margin}║   {spaces}   ║
{margin}║   {message}   ║
{margin}║   {spaces}   ║
{margin}╚═══{lines}═══╝"""
    )
    time.sleep(timeout)


def main(argv):
    """Display a dialog window."""
    parser = argparse.ArgumentParser(description="""Display a dialog window.""")
    parser.add_argument("message", help="message to display", type=str)
    parser.add_argument("x", help="x dimension", type=int)
    parser.add_argument("y", help="y dimension", type=int)
    parser.add_argument("timeout", help="timeout for dialog", type=float)
    args = parser.parse_args(argv)

    dialog(args.message, args.x, args.y, args.timeout)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("Interrupted by user.")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)  # pylint: disable=protected-access
