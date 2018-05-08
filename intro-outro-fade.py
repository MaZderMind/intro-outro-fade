#!/usr/bin/env python3
import gi
import sys
import argparse

# import GStreamer and GLib-Helper classes
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

# init GObject & Co. before importing local classes
GObject.threads_init()
Gst.init([])
mainloop = GObject.MainLoop()

parser = argparse.ArgumentParser()
parser.add_argument("--intro", help="intro to prepend")

parser.add_argument("--intro-fade-time", help="duration in seconds for which intro and content should overlap", default=0.5, type=float)
parser.add_argument("--intro-audio-earlier", help="duration in seconds by which the audio overlap between intro and content should be earlier then the video-overlap", default=0.25, type=float)

parser.add_argument("--content", help="content to wrap", required=True)

parser.add_argument("--outro-fade-time", help="duration in seconds for which outro and content should overlap", default=0.5, type=float)
parser.add_argument("--outro-audio-later", help="duration in seconds by which the audio overlap between outro and content should be later then the video-overlap", default=0.25, type=float)

parser.add_argument("--outro", help="outro to append")

parser.add_argument("--tty-ok", help="outro to append", action='store_true')

args = parser.parse_args()
print(args, file=sys.stderr)

if sys.stdout.isatty() and not args.tty_ok:
	print("refusing to output binary data (raw-video/-audio in matroska) to stdout, which seems to be a tty. Pass --tty-ok to force.", file=sys.stderr)
	sys.exit(1)

pipelineDescription = """
	filesrc location="{intro}" ! decodebin name=intro
	intro. ! {vfilter} ! {vcaps} ! queue ! vmix.
	intro. ! {afilter} ! {acaps} ! queue ! amix.

	filesrc location="{content}" ! decodebin name=content
	content. ! {vfilter} ! {vcaps} ! queue ! vmix.
	content. ! {afilter} ! {acaps} ! queue ! amix.

	compositor name=vmix ! queue ! {vcaps} ! mux.
	audiomixer name=amix ! queue ! {acaps} ! mux.

	matroskamux matroskamux name=mux ! fdsink
""".format(
	vcaps="video/x-raw,format=I420,width=1920,height=1080,framerate=25/1,interlace-mode=progressive,chroma-site=mpeg2",
	acaps="audio/x-raw,format=S16LE,layout=interleaved,rate=48000,channels=2",
	vfilter="videoconvert ! videoscale ! videorate",
	afilter="audioconvert ! audiorate",

	intro=args.intro,
	content=args.content
)

print(pipelineDescription, file=sys.stderr)

pipeline = Gst.parse_launch(pipelineDescription)


def on_eos(bus, message):
    print('EOS', file=sys.stderr)
    mainloop.quit()

def on_error(bus, message):
    print('Received Error-Signal')
    (error, debug) = message.parse_error()
    print('Error-Details: #%u: %s' % (error.code, debug), file=sys.stderr)
    mainloop.quit()

pipeline.bus.add_signal_watch()
pipeline.bus.connect("message::eos", on_eos)
pipeline.bus.connect("message::error", on_error)

pipeline.set_state(Gst.State.PLAYING)
mainloop.run()
