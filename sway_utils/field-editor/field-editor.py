#!/bin/python3

import argparse
import asyncio
import logging as log
import os
import subprocess
import sys
import time

from i3ipc import Event
from i3ipc.aio import Connection


async def launch_app(conn, app_name):
    def on_new_window(self, e):
        self.locked = False

    conn.locked = True
    conn.on(Event.WINDOW_NEW, on_new_window)
    timing = time.time()
    await conn.command(f"exec {app_name}")

    while conn.locked:
        await asyncio.sleep(0.1)

    _timing = time.time() - timing
    log.info(f"({_timing:.4f}s) Launched {app_name}")


def edit_clipboard(filename) -> None:
    subprocess.run(
        [
            "alacritty",
            "--class=field-editor",
            "-e",
            "/home/nicole/git/sway-utils/sway-utils/field-editor/field-editor.sh",
            filename,
        ]
    )


def get_clipboard() -> str:
    output = ""
    process = subprocess.run(
        ["wl-paste", "-n"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    if process.stdout:
        output = process.stdout.decode("utf-8")
        return output

    return output


def load_file_to_clipboard(filename) -> None:
    cat = subprocess.run(["cat", filename], stdout=subprocess.PIPE)
    process = subprocess.Popen(["wl-copy", "-n", "-o"], stdin=subprocess.PIPE)
    process.communicate(input=cat.stdout.strip())


async def edit_field() -> None:
    conn = await Connection().connect()

    # Cancel operation if we're currently focusing a terminal
    tree = await conn.get_tree()
    focused = tree.find_focused()
    if focused.name == "Alacritty":
        return

    # Create a temporary file to hold the clipboard contents, so we can edit it
    process = subprocess.run(["mktemp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    tmpfile = process.stdout.decode("utf-8").splitlines()[0]

    # Copy the field contents
    await conn.command("exec ydotool key Ctrl+a")
    await asyncio.sleep(0.05)
    await conn.command("exec ydotool key Ctrl+c")
    await asyncio.sleep(0.20)
    clipboard = get_clipboard()
    if clipboard:
        with open(tmpfile, "w") as f:
            f.writelines(clipboard)

    # Let the user edit the clipboard contents
    edit_clipboard(tmpfile)

    # Paste the file contents back into the clipboard and re-paste it into the field
    load_file_to_clipboard(tmpfile)
    await asyncio.sleep(0.2)
    await conn.command("exec ydotool key Ctrl+v")


def main(argv):
    """Edit the contents of the currently focused field in vim."""
    parser = argparse.ArgumentParser(
        description="""Edit the contents of the currently focused field in vim."""
    )
    parser.parse_args(argv)

    asyncio.get_event_loop().run_until_complete(edit_field())


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("Interrupted by user.")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)  # pylint: disable=protected-access
