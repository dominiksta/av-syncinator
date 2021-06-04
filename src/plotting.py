from statistics import mean
import matplotlib.pyplot as plt


def plot_sync_accuracy(
        timestamps_video: list[int], timestamps_audio: list[int]
) -> None:
    timestamps_audio = timestamps_audio[0:len(timestamps_video)]
    timestamps_video = timestamps_video[0:len(timestamps_audio)]
    def list_diff(l1, l2): return [abs(l1[i] - l2[i]) for i in range(0, len(l1))]
    diffs = list_diff(timestamps_video, timestamps_audio)
    x = list(range(0, len(timestamps_video)))
    plt.title("AV Sync accuracy")
    plt.ylabel("Time Difference [ms]")
    plt.xlabel("Nr. of detected white noise + white video")
    plt.plot(x, diffs, "+", label="Measured Data")
    plt.hlines(mean(diffs), x[0], x[-1], color="orange", label="Average")
    plt.legend()
    plt.show()