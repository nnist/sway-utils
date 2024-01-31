#!/bin/python3

import math
import subprocess
import sys

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("GtkLayerShell", "0.1")

from gi.repository import Gdk, GLib, Gtk, GtkLayerShell  # noqa:E401


class CRTEffect:
    progress = 0
    speed = 0.6
    tick_rate = 1

    def _create_window(self, anchor, color):
        window = Gtk.Window()
        GtkLayerShell.init_for_window(window)
        GtkLayerShell.set_exclusive_zone(window, -1)
        GtkLayerShell.set_margin(window, GtkLayerShell.Edge.TOP, 0)
        GtkLayerShell.set_margin(window, GtkLayerShell.Edge.BOTTOM, 0)
        GtkLayerShell.set_anchor(window, anchor, True)
        GtkLayerShell.set_layer(window, GtkLayerShell.Layer.OVERLAY)
        window.set_size_request(0, 0)
        window.override_background_color(Gtk.StateFlags.NORMAL, color)
        window.set_accept_focus(False)
        window.show_all()
        window.connect("destroy", Gtk.main_quit)
        return window

    def _init_windows(self):
        self.top_shutter = self._create_window(
            GtkLayerShell.Edge.TOP, Gdk.RGBA(0.0, 0.0, 0.0, 1.0)
        )
        self.bottom_shutter = self._create_window(
            GtkLayerShell.Edge.BOTTOM, Gdk.RGBA(0.0, 0.0, 0.0, 1.0)
        )
        self.left_shutter = self._create_window(
            GtkLayerShell.Edge.LEFT, Gdk.RGBA(0.0, 0.0, 0.0, 1.0)
        )
        self.right_shutter = self._create_window(
            GtkLayerShell.Edge.RIGHT, Gdk.RGBA(0.0, 0.0, 0.0, 1.0)
        )
        self.flash_shutter = self._create_window(
            GtkLayerShell.Edge.BOTTOM, Gdk.RGBA(1.0, 1.0, 1.0, 1.0)
        )

    def __init__(self, width: int, height: int, *args, **kwargs):
        self.width = width
        self.height = height

    def run(self):
        self._init_windows()
        self.progress = 100
        GLib.timeout_add(self.tick_rate, self._tick)
        Gtk.main()

    def _tick(self):
        self.progress -= self.speed
        self.render()
        if self.progress <= 0:
            Gtk.main_quit()
            return False

        return True

    def render(self):
        if self.progress > 100:
            self.progress = 100
        elif self.progress < 1:
            self.progress = 0

        if self.progress > 0:
            width = int(
                (self.width / 2) - (self.width / 2) / math.pow(100 / self.progress, 1.0)
            )
            height = int(
                (self.height / 2)
                - (self.height / 2) / math.pow(100 / self.progress, 32)
            )
            flash_opacity = 1 - 1 / math.pow(100 / self.progress, 8)
            self.flash_shutter.set_opacity(flash_opacity)
        else:
            width = int(self.width / 2)
            height = int(self.height / 2)
            self.flash_shutter.hide()

        self.left_shutter.set_size_request(width, self.height)
        self.right_shutter.set_size_request(width, self.height)
        self.top_shutter.set_size_request(self.width, height)
        self.bottom_shutter.set_size_request(self.width, height)
        self.flash_shutter.set_size_request(self.width, self.height)

    def stop(self):
        self.left_shutter.destroy()
        self.right_shutter.destroy()
        self.top_shutter.destroy()
        self.bottom_shutter.destroy()
        self.flash_shutter.destroy()


if __name__ == "__main__":
    effect = CRTEffect(2560, 1600)
    effect.run()
    if "--lock" in sys.argv:
        subprocess.run(["swaylock", "-f", "-c", "000000"])
