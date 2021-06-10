"""
This is by no means thorough, but it should at least tell me when something very
basic goes wrong.
"""

import unittest
import cv2
import os, sys
import subprocess
import warnings

# HACK: This probably shows my lack of deeper knowledge about python more then
# anything in this project. For now it works though.
sys.path.insert(0, '../app')
import util, logger, common

Log = logger.Logger.get_instance()
Log.output_function = lambda msg: None
DATADIR = '..' + os.sep + '..' + os.sep + 'data' + os.sep


class TestCode(unittest.TestCase):
    def setUp(self): common.dirsetup()
    def tearDown(self): common.dirteardown()

    def test_color_percent_100(self):
        img = cv2.imread(DATADIR + 'testvid_src' + os.sep + 'black.png')
        res = util.color_percent_in_img(img, [0, 0, 0], 0)
        self.assertEqual(res, 1)


    def test_color_percent_0(self):
        img = cv2.imread(DATADIR + 'testvid_src' + os.sep + 'white.png')
        res = util.color_percent_in_img(img, [0, 0, 0], 0)
        self.assertEqual(res, 0)


    def test_color_percent_0_diff(self):
        img = cv2.imread(DATADIR + 'testvid_src' + os.sep + 'white.png')
        res = util.color_percent_in_img(img, [0, 0, 0], 50)
        self.assertEqual(res, 0)


    def test_video_to_wav_success(self):
        util.video_to_wav(DATADIR + 'testvid.mp4')


    def test_video_to_wav_missing_file(self):
        with self.assertRaises(subprocess.CalledProcessError):
            util.video_to_wav(DATADIR + 'estvid.mp4')


    def test_timestamps_on_example(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            stamps = util.timestamps_video_and_video_for_file(
                DATADIR + 'testvid.mp4'
            )
        self.assertEqual(
            stamps,
            (
                [
                    2000.0, 4000.0, 6000.0, 8000.0, 10000.0, 12000.0, 14000.0,
                    16000.0, 18000.0, 20000.0, 22000.0, 24000.0, 26000.0,
                    28000.0, 30000.0
                ],
                [
                    1990, 3990, 5990, 8010, 9990, 11990, 13990, 15990, 17990,
                    19990, 21990, 23990, 25990, 27990, 29990
                ]
            )
        )


if __name__ == '__main__': unittest.main()