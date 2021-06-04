from util import timestamps_video_and_video_for_file
from argparse import ArgumentParser
from plotting import plot_sync_accuracy
from testdata import testdata

parser = ArgumentParser(description='Command Line Interface for AV-Syncinator')

parser.add_argument('filename', help='Path to the video file to analyze')
args = parser.parse_args()

if args.filename == '__test__':
    plot_sync_accuracy(testdata['timestamps_video'], testdata['timestamps_audio'])
else:
    tv, ta = timestamps_video_and_video_for_file(args.filename)
    plot_sync_accuracy(tv, ta)
