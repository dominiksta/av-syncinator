import os, sys
from . import logger
from .. import dirteardown
from .util import timestamps_video_and_audio_for_file
from .localisation import set_locale
from argparse import ArgumentParser
from . import processing
from .testdata import testdata

def on_closing(): dirteardown()

logger.Logger.get_instance()

parser = ArgumentParser(description='Command Line Interface for AV-Syncinator')

parser.add_argument('filename', help='Path to the video file to analyze (mkv or mp4)')
parser.add_argument('-l', '--lang', type=str, help='Set localisation')
parser.add_argument('-o', '--output-directory', type=str, default=os.getcwd(),
                    help='Save figures to this directory instead of showing them')
parser.add_argument('-f', '--output-format', type=str, help='Either .csv or .png',
                    default='.csv')
parser.add_argument('--audio-interval', type=int, default=1,
                    help='Step size for scanning the audio [ms]')
parser.add_argument('--audio-threshold', type=int, default=-50,
                    help='The loudness of the sound to consider [dB]')
parser.add_argument('--video-color-diff', type=int, default=30,
                    help='How much the color in the video may differ from white [0-255]')
parser.add_argument('--video-color-ratio', type=int, default=0.7,
                    help='How much of the screen has to be white [0-1]')
parser.add_argument('--no-try-match', action="store_true",
                    help='Don\'t try ignoring stutters')

try:
    args = parser.parse_args()
except:
    on_closing()
    sys.exit(1)

if args.lang != None: set_locale(args.lang)

if not os.path.exists(args.output_directory):
    raise Exception("Invalid Directory: " + args.output_directory)

if args.filename == '__test__':
    tv, ta = testdata['timestamps_video'], testdata['timestamps_audio']
else:
    tv, ta = timestamps_video_and_audio_for_file(
        videofile=args.filename,
        video_threshold_color_diff = args.video_color_diff,
        video_threshold_color_ratio = args.video_color_ratio,
        audio_interval_ms = args.audio_interval,
        audio_threshold_volume_db = args.audio_threshold,
        try_ignore_stutters_by_matching = not args.no_try_match,
    )

if args.output_format == '.png':
    processing.plot_sync_accuracy(tv, ta, args.output_directory)
else:
    if args.output_directory == None: args.output_directory = os.getcwd()
    processing.save_as_csv(tv, ta, args.output_directory + os.sep + 'out.csv', {
        'video_color_diff': args.video_color_diff,
        'video_color_ratio': args.video_color_ratio,
        'audio_interval': args.audio_interval,
        'audio_threshold': args.audio_threshold,
        'try_match': not args.no_try_match,
    })

on_closing()