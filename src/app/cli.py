import os, sys
import logger
import common
from util import timestamps_video_and_video_for_file
from localisation import set_locale
from argparse import ArgumentParser
from plotting import plot_sync_accuracy
from testdata import testdata

common.dirsetup()
def on_closing(): common.dirteardown()

Log = logger.Logger.get_instance().log
lvl = logger.LogLvl

parser = ArgumentParser(description='Command Line Interface for AV-Syncinator')

parser.add_argument('filename', help='Path to the video file to analyze (mkv or mp4)')
parser.add_argument('-l', '--lang', type=str, help='Set localisation')
parser.add_argument('-o', '--output-directory', type=str,
                    help='Save figures to this directory instead of showing them')
parser.add_argument('--audio-interval', type=int, default=10,
                    help='Step size for scanning the audio [ms]')
parser.add_argument('--audio-threshold', type=int, default=-100,
                    help='The loudness of the sound to consider [dB]')
parser.add_argument('--video-color-diff', type=int, default=30,
                    help='How much the color in the video may differ from white [0-255]')
parser.add_argument('--video-color-ratio', type=int, default=0.7,
                    help='How much of the screen has to be white [0-1]')

try:
    args = parser.parse_args()
except:
    on_closing()
    sys.exit(1)

if args.lang != None: set_locale(args.lang)

if args.output_directory != None:
    if not os.path.exists(args.output_directory):
        raise Exception("Invalid Directory: " + args.output_directory)

if args.filename == '__test__':
    tv, ta = testdata['timestamps_video'], testdata['timestamps_audio']
else:
    tv, ta = timestamps_video_and_video_for_file(
        videofile=args.filename,
        video_threshold_color_diff=args.video_color_diff,
        video_threshold_color_ratio=args.video_color_ratio,
        audio_interval_ms=args.audio_interval,
        audio_threshold_volume_db=args.audio_threshold,
    )

plot_sync_accuracy(tv, ta, args.output_directory)
on_closing()