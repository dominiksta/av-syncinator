import cv2
import os
import shutil
from . import logger
from time import time as curr_time
import subprocess
import numpy as np
from pydub import AudioSegment
from .. import TEMPDIR, FFMPEG
from typing import List, Tuple

Log = logger.Logger.get_instance()


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


def white_timestamps_for_vidcap(
        vidcap: cv2.VideoCapture, tolerance_color: int,
        tolerance_color_ratio: int,
) -> List[int]:
    """
    Return a list of integer timestamps in ms corresponding to the start times
    of mostly white frames in `vidcap` relative to the start of the video. May
    take a long time depending on the size of the video.
    """
    success, img = vidcap.read()

    Log.info('Starting Video Processing')
    Log.info('tolerance_color: ' + str(tolerance_color))
    Log.info('tolerance_color_ratio: ' + str(tolerance_color_ratio))

    last_white = False
    timestamps = []

    vid_end = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) / \
        vidcap.get(cv2.CAP_PROP_FPS) * 1000

    last_progress_time = curr_time()

    while success:
        white = color_percent_in_img(img, [255, 255, 255], tolerance_color)
        time = vidcap.get(cv2.CAP_PROP_POS_MSEC)
        if white > tolerance_color_ratio:
            if not last_white:
                timestamps.append(time)
            last_white = True
        else: last_white = False
        if (curr_time() - last_progress_time) > 1:
            Log.info("Progress: " + str(int((time / vid_end) * 100)) + "%")
            last_progress_time = curr_time()
        success, img = vidcap.read()

    Log.info("Finished Video Processing")
    return timestamps[1:]


def video_to_wav(videofile: str) -> None:
    """
    Convert a video file given by `videofile` to a .wav in the same folder as
    the video file using `ffmpeg`. `videofile` should be a path using regular os
    separators.
    """
    Log.info("Converting audio to .wav")

    prevdir = os.getcwd()
    os.chdir(os.path.dirname(videofile))

    fname = os.path.splitext(os.path.basename(videofile))
    cmd = [FFMPEG, '-y', '-i', fname[0] + fname[1], fname[0] + '.wav']

    Log.info(cmd)
    try:
        # When using pyinstaller on windows, stdout and stderr seem to not open
        # correctly. The following command was the only way I could find to have
        # something that would run silently in all situations (except when using
        # pyinstaller it pops up a little console window on windows - but in all
        # other situations its silent).
        ret = subprocess.check_call(
            cmd, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

        if os.name != 'nt': ret = os.WEXITSTATUS(ret)
        if ret != 0:
            raise Exception(
                "`" + cmd + " ` failed with nonzero exit code: " + str(ret)
            )
    except: raise # We exit the function when an error is raised but we still
                  # want to chdir to prevdir
    finally:
        os.chdir(prevdir)

    shutil.move(os.path.dirname(videofile) + os.sep + fname[0] + '.wav',
                TEMPDIR + fname[0] + '.wav')


def volume_timestamps_for_wav(
        wavfile: str, interval_ms: int, min_volume_db: int
) -> List[int]:
    Log.info("Findind timestamps in audio")

    track = AudioSegment.from_wav(wavfile)
    last_loud = False
    timestamps = []

    for pos_ms in range(0, len(track), interval_ms):
        vol = track[pos_ms:pos_ms + interval_ms].dBFS
        if vol > min_volume_db:
            # Do not capture timestamps when the last recorded timestamps is
            # less than 1100ms away. This makes sense because the interval
            # between start and end of white noise in the testvideo is 1000ms.
            if not last_loud and (len(timestamps) == 0 or \
                                  pos_ms - timestamps[-1] > 1100):
                timestamps.append(pos_ms)
            last_loud = True
        else: last_loud = False

    return timestamps[1:]


def _match_nearest_list_items(l1: List[int], l2: List[int]) -> List[int]:
    """
    Return a list `l3` with `length == len(l1)` where for every `i in range(0,
    len(l1))`, `l3[i]` is the element in `l2` closest to `l1[i]`.
    """
    def nearest_int_in_list(value: int, l: List[int]) -> int:
        res = l[0]
        for i in l:
            if abs(i - value) < abs(res - value): res = i
        return res

    l3 = []
    for i in range(0, len(l1)):
        l3.append(nearest_int_in_list(l1[i], l2))

    return l3


def timestamps_video_and_audio_for_file(
        videofile: str,
        video_threshold_color_diff: int = 30,
        video_threshold_color_ratio: int = 0.7,
        audio_interval_ms: int = 1,
        audio_threshold_volume_db: int = -50,
        try_ignore_stutters_by_matching = True,
) -> Tuple[int, int]:
    """
    Return computed timestamps of white noise in audio and mostly white images
    in video for `videofile`.
    """
    video_to_wav(videofile)
    timestamps_audio = volume_timestamps_for_wav(
        TEMPDIR + os.path.splitext(os.path.basename(videofile))[0] + '.wav',
        audio_interval_ms,
        audio_threshold_volume_db
    )
    timestamps_video = white_timestamps_for_vidcap(
        cv2.VideoCapture(videofile),
        video_threshold_color_diff,
        video_threshold_color_ratio
    )
    Log.info("Got all timestamps")

    if try_ignore_stutters_by_matching:
        timestamps_audio = _match_nearest_list_items(
            timestamps_video, timestamps_audio
        )

    return timestamps_video, timestamps_audio