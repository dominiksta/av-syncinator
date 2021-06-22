import os
from statistics import mean
import matplotlib.pyplot as plt
import csv
from .localisation import translate as _
from . import logger
from typing import List, Tuple

Log = logger.Logger.get_instance()

def _preprocess(
        timestamps_audio: List[int], timestamps_video: List[int]
) -> Tuple[List[int], List[int]]:
    # cut off additional elements
    timestamps_audio = timestamps_audio[0:len(timestamps_video)]
    timestamps_video = timestamps_video[0:len(timestamps_audio)]
    # round to no decimal points (sub ms time is irrelevant)
    timestamps_audio = [int(t) for t in timestamps_audio]
    timestamps_video = [int(t) for t in timestamps_video]
    return timestamps_audio, timestamps_video
    

def plot_sync_accuracy(
        timestamps_video: List[int], timestamps_audio: List[int],
        output_folder = None,
) -> None:
    Log.info('plotting: ' + str(timestamps_video) + ',' + str(timestamps_audio))
    timestamps_audio, timestamps_video = \
        _preprocess(timestamps_audio, timestamps_video)
    def list_diff(l1, l2): return [abs(l1[i] - l2[i]) for i in range(0, len(l1))]
    diffs = list_diff(timestamps_video, timestamps_audio)
    x = list(range(0, len(timestamps_video)))
    plt.title(_("AV Sync accuracy"))
    plt.ylabel(_("Time Difference [ms]"))
    plt.xlabel(_("Nr. of detected white noise + white video"))
    plt.plot(x, diffs, "+", label=_("Measured Data"))
    plt.hlines(mean(diffs), x[0], x[-1], color="orange", label=_("Average"))
    plt.legend()
    if output_folder == None: plt.show()
    else: plt.savefig(output_folder + os.sep + 'accuracy.png')


def save_as_csv(
        timestamps_video: List[int], timestamps_audio: List[int], filename: str
) -> None:
    Log.info('saving: ' + str(timestamps_video) + ',' + str(timestamps_audio))
    timestamps_audio, timestamps_video = \
        _preprocess(timestamps_audio, timestamps_video)
    Log.info('saving to file: ' + filename)

    with open(filename, 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['timestamps_audio', 'timestamps_video'])
        for i in range(0, len(timestamps_audio)):
            writer.writerow([timestamps_audio[i], timestamps_video[i]]) 