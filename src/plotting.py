import os
from statistics import mean
import matplotlib.pyplot as plt
from localisation import translate as _
import logger

Log = logger.Logger.get_instance()

def plot_sync_accuracy(
        timestamps_video: list[int], timestamps_audio: list[int],
        output_folder = None,
) -> None:
    Log.info('plotting: ' + str(timestamps_video) + ',' + str(timestamps_audio))
    timestamps_audio = timestamps_audio[0:len(timestamps_video)]
    timestamps_video = timestamps_video[0:len(timestamps_audio)]
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