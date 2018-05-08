#!/usr/bin/env python3
import gi
import argparse

# import GStreamer and GLib-Helper classes
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

# init GObject & Co. before importing local classes
GObject.threads_init()

parser = argparse.ArgumentParser()
parser.add_argument("--intro", help="intro to prepend")
parser.add_argument("--content", help="content to wrap", required=True)
parser.add_argument("--outro", help="intro to append")
parser.parse_args()


mainloop = GObject.MainLoop()
mainloop.run()
