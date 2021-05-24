import datetime
import os
import subprocess
import sys
import time
from typing import Union

import gi
from rofi import Rofi
from sway_utils.effects.crt import CRTEffect

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("GtkLayerShell", "0.1")

from gi.repository import Gdk, GLib, Gtk, GtkLayerShell  # noqa:E402


def sanitize_string(string):
    string = string.replace("&", "&amp;")
    string = string.replace("<", "&lt;")
    string = string.replace(">", "&gt;")
    string = string.replace("'", "&#39;")
    string = string.replace('"', "&#34;")
    return string


def _input(msg, options):
    r = Rofi(rofi_args=["-theme", "base16-default-dark"])
    if options:
        key = -1
        while key != 0:
            index, key = r.select(msg, options)

        return options[index]
    else:
        return r.text_entry(msg)


class App:
    screen_width = 2560
    start_time: Union[float, int] = 0
    duration = 10
    task = None

    def __init__(self, task: str, duration: int, *args, **kwargs):
        self.task = task
        self.duration = duration
        self.crt_effect = CRTEffect(2560, 1080)

        self.bar = Gtk.Window()
        GtkLayerShell.init_for_window(self.bar)
        GtkLayerShell.set_exclusive_zone(self.bar, -1)
        GtkLayerShell.set_margin(self.bar, GtkLayerShell.Edge.BOTTOM, 0)
        GtkLayerShell.set_anchor(self.bar, GtkLayerShell.Edge.BOTTOM, True)
        GtkLayerShell.set_layer(self.bar, GtkLayerShell.Layer.OVERLAY)

        self.bar.set_accept_focus(False)
        self.bar.override_background_color(
            Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 0.0, 0.0, 1.0)
        )
        self.bar.set_size_request(0, 0)
        self.bar.show_all()
        self.bar.connect("destroy", Gtk.main_quit)

        label_overlay = Gtk.Window()
        label = Gtk.Label()
        label.set_markup(
            f'<span foreground="#D8D8D8" font_desc="Fira Code Regular 11">{task}</span>'  # noqa:E501
        )
        label_overlay.add(label)

        GtkLayerShell.init_for_window(label_overlay)
        GtkLayerShell.set_exclusive_zone(label_overlay, -1)
        GtkLayerShell.set_margin(label_overlay, GtkLayerShell.Edge.BOTTOM, 3)
        GtkLayerShell.set_anchor(label_overlay, GtkLayerShell.Edge.BOTTOM, True)

        GtkLayerShell.set_layer(label_overlay, GtkLayerShell.Layer.OVERLAY)
        label_overlay.override_background_color(
            Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 0.0)
        )
        label_overlay.set_accept_focus(False)
        label_overlay.show_all()
        label_overlay.connect("destroy", Gtk.main_quit)
        self.label_overlay = label_overlay

    def run(self):
        GLib.timeout_add(100, self._tick)
        self.start_time = time.time()
        Gtk.main()
        self.update_log()
        self.bar.hide()
        self.label_overlay.hide()
        self.crt_effect.run()
        self.lock()
        sys.exit(0)

    def gtk_quit(self):
        Gtk.main_quit()

    def update_log(self):
        directory = os.path.expanduser("~") + "/.intention"
        if not os.path.exists(directory):
            os.mkdir(directory)

        filename = f"{directory}/log.txt"
        if not os.path.exists(filename):
            os.mknod(filename)

        today = datetime.datetime.today().strftime("%a %d %b %Y")
        start_time = datetime.datetime.fromtimestamp(self.start_time).strftime("%H:%M")
        end_time = datetime.datetime.now().strftime("%H:%M")
        log_entry = [f"{start_time}-{end_time} - {self.task}"]

        with open(filename, mode="r+", encoding="utf-8") as f:
            lines = f.readlines()
            if lines and lines[0].strip() == today:
                # Heading for today already exists
                f.seek(len(today) + 1)
                lines = lines[1:]
            else:
                # Add new heading for today
                log_entry.insert(0, today)
                f.seek(0)
                log_entry.append("")

            f.writelines("\n".join(log_entry))
            f.writelines(["\n"] + lines)

    @property
    def progress(self):
        progress = (time.time() - self.start_time) / self.duration * 100
        if progress < 0:
            progress = 0
        elif progress > 100:
            progress = 100

        return progress

    def _tick(self):
        if self.progress < 100:
            self._update_bar()
            return True
        else:
            self.gtk_quit()
            return False

    def _update_bar(self):
        width = int(self.screen_width - self.screen_width * (self.progress / 100))
        self.bar.set_size_request(width, 2)

    def lock(self):
        subprocess.run(["swaylock", "-f", "-c", "000000"])
