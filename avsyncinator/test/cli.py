import unittest
import os
import subprocess
from . import DATADIR

class TestCommandLineInterface(unittest.TestCase):

    def _run_cmd_silently(self, cmd: str) -> None:
        ret = subprocess.check_call(
            cmd, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        if os.name != 'nt': ret = os.WEXITSTATUS(ret)
        return ret


    def test_outputs_img(self):
        if os.name != 'nt':
            print('CLI only gets tested on windows currently')
            return
        exe = 'build' + os.sep + 'windows' + os.sep + 'dist' + \
            os.sep + 'av-syncinator-cli.exe'
        if not os.path.exists(exe):
            print('Please build an exe file first (build-cli.bat)')
        self.assertTrue(os.path.exists(exe))

        with self.assertRaises(subprocess.CalledProcessError):
            ret = self._run_cmd_silently(exe)
            self.assertEqual(ret, 1)

        with self.assertRaises(subprocess.CalledProcessError):
            ret = self._run_cmd_silently(exe + ' nonexistent.mpv')
            self.assertEqual(ret, 1)

        with self.assertRaises(subprocess.CalledProcessError):
            ret = self._run_cmd_silently(exe + ' nonexistent.mpv')
            self.assertEqual(ret, 1)

        cmd = exe + ' -o . ' + DATADIR + 'testvid.mp4'
        ret = self._run_cmd_silently(cmd)
        self.assertEqual(ret, 0)
        self.assertTrue(os.path.exists('accuracy.png'))
        os.remove('accuracy.png')

if __name__ == '__main__':
    unittest.main()