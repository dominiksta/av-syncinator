import os
from util import timestamps_video_and_video_for_file
from plotting import plot_sync_accuracy

base_path = '..' + os.sep + 'data' + os.sep + 'example' + os.sep

tv, ta = timestamps_video_and_video_for_file(base_path + 'rdp-wan.mkv')
plot_sync_accuracy(tv, ta)