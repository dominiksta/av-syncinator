import cv2
import os
from time import time as curr_time
from subprocess import DEVNULL, STDOUT, check_call
import numpy as np
from pydub import AudioSegment

from shutil import which
FFMPEG = which("ffmpeg")
if FFMPEG == None: raise Exception("ffmpeg not found in PATH")

TEMP_DIR = '..' + os.sep + 'data' + os.sep + 'temp' + os.sep

TOLERANCE_COLOR_DETECTION = 30
TOLERANCE_COLOR_PERCENT = 0.7
VOLUME_MIN_LEVEL_DB = -100
SOUND_INTERVAL_MS = 10

def color_percent_in_img(img: np.array, rgb, diff) -> int:
    """
    Return the percentage of the color given by `rgb` in `img` where `img` is
    formatted like return values of `cv2.imread`. Allow for a 'tolerance' of
    `diff`.
    """
    def min0(i): return 0 if i < 0 else i
    def max255(i): return 255 if i > 255 else i

    # in order 'BGR' (as opposed to RGB) as opencv represents images as numpy
    # arrays in reverse order
    boundaries = ([min0(rgb[2]-diff), min0(rgb[1]-diff), min0(rgb[0]-diff)],
                  [max255(rgb[2]+diff), max255(rgb[1]+diff), max255(rgb[0]+diff)])

    lower = np.array(boundaries[0], dtype=np.uint8)
    upper = np.array(boundaries[1], dtype=np.uint8)
    mask = cv2.inRange(img, lower, upper)

    ratio = cv2.countNonZero(mask)/(img.size/3)
    return ratio
    # output = cv2.bitwise_and(img, img, mask=mask)
    # cv2.imshow("images", np.hstack([img, output]))
    # cv2.waitKey(0)


def white_percent_in_img(img: np.array) -> int:
    return color_percent_in_img(img, [255, 255, 255], TOLERANCE_COLOR_DETECTION)


def white_timestamps_for_vidcap(vidcap) -> list[int]:
    """
    Return a list of integer timestamps in ms corresponding to the start times
    of mostly white frames in `vidcap` relative to the start of the video. May
    take a long time depending on the size of the video.
    """
    success, img = vidcap.read()

    print("Starting Video Processing")

    last_white = False
    timestamps = []

    vid_end = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) / \
        vidcap.get(cv2.CAP_PROP_FPS) * 1000

    last_progress_time = curr_time()

    while success:
        white = white_percent_in_img(img)
        time = vidcap.get(cv2.CAP_PROP_POS_MSEC)
        if white > TOLERANCE_COLOR_PERCENT:
            if not last_white:
                timestamps.append(time)
            last_white = True
        else: last_white = False
        if (curr_time() - last_progress_time) > 1:
            print("Progress: " + str(int((time / vid_end) * 100)) + "%")
            last_progress_time = curr_time()
        success, img = vidcap.read()

    print("Finished Video Processing")
    return timestamps[1:]
    

def video_to_wav(videofile: str, ffmpeg = FFMPEG) -> None:
    """
    Convert a video file given by `videofile` to a .wav in the same folder as
    the video file using `ffmpeg`. `videofile` should be a path using regular os
    separators.
    """
    prevdir = os.getcwd()
    os.chdir(os.path.dirname(videofile))

    fname = os.path.splitext(os.path.basename(videofile))
    cmd = ffmpeg + ' -y -i "' + fname[0] + fname[1] + '" "' + fname[0] + '.wav"'

    ret = check_call(cmd, stdout=DEVNULL, stderr=STDOUT)

    if os.name != 'nt': ret = os.WEXITSTATUS(ret)
    if ret != 0:
        raise Exception(
            "`" + cmd + " ` failed with nonzero exit code: " + str(ret)
        )

    os.chdir(prevdir)
    os.replace(os.path.dirname(videofile) + os.sep + fname[0] + '.wav',
               TEMP_DIR + fname[0] + '.wav')


def volume_timestamps_for_wav(wavfile: str) -> list[int]:
    track = AudioSegment.from_wav(wavfile)
    last_loud = False
    timestamps = []

    for pos_ms in range(0, len(track), SOUND_INTERVAL_MS):
        vol = track[pos_ms:pos_ms + SOUND_INTERVAL_MS].dBFS
        # if vol != float('-inf'):
        #     print(vol)
        if vol > VOLUME_MIN_LEVEL_DB:
            if not last_loud:
                timestamps.append(pos_ms)
            last_loud = True
        else: last_loud = False
        # print(timestamps)

    return timestamps[1:]
    

base_path = '..' + os.sep + 'data' + os.sep + 'example' + os.sep

vidcap = cv2.VideoCapture(base_path + 'local.mkv')
white_timestamps_for_vidcap(vidcap)

video_to_wav(base_path + 'local.mkv')
print(volume_timestamps_for_wav(TEMP_DIR + 'local.wav'))