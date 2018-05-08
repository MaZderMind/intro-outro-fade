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

parser.add_argument("--intro-fade-time", help="duration in seconds for which intro and content should overlap", default=0.5)
parser.add_argument("--intro-audio-earlier", help="duration in seconds by which the audio overlap between intro and content should be earlier then the video-overlap", default=0.25)

parser.add_argument("--content", help="content to wrap", required=True)

parser.add_argument("--outro-fade-time", help="duration in seconds for which outro and content should overlap", default=0.5)
parser.add_argument("--outro-audio-later", help="duration in seconds by which the audio overlap between outro and content should be later then the video-overlap", default=0.25)

parser.add_argument("--outro", help="outro to append")

args = parser.parse_args()

print(args)


#mainloop = GObject.MainLoop()
#mainloop.run()
