#!/bin/python3

from sway_utils.intention.app import App, _input, sanitize_string

if __name__ == "__main__":
    try:
        task = sanitize_string(_input("What do you intend to do?", []))
        mins = int(_input("For how many minutes?", ["25", "10", "5", "2"])) * 60
        app = App(task, mins)
        app.run()
    except KeyboardInterrupt:
        app.gtk_quit()
