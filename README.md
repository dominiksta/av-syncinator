<img src="avsyncinator/res/logo/logo-256x256.png" height="128" align="right"/>

# AV-Syncinator

![License GPL 3](https://img.shields.io/github/license/dominiksta/av-syncinator)
![Build Status](https://img.shields.io/github/workflow/status/dominiksta/av-syncinator/CI/master)

AV-Syncinator is a small utility to measure
[Audio-Video-Synchronization](https://en.wikipedia.org/wiki/Audio-to-video_synchronization).
It works by analyzing a recording of the playback of a specifically prepared
video file. It was created to be used in the context of remote desktop systems
(such as RDP, VNC, etc.), although other applications are conceivable.

# Usage

1. Download `data/testvid.mp4`.
2. Play `testvid.mp4` on the system you wish to analyze. Then record the
   playback. As an example, the file in `data/example/rdp-wan.mkv` contains an
   [OBS](https://obsproject.com/) recording of `testvid.mp4` being played back
   over an RDP connection over a Wide Area Network.
3. Start AV-Syncinator
4. Click "Browse" and locate your recording
5. Click "Analyze"

After some time, you will see a plot of the results:

<img src="data/screenshot.png"/>

[More documentation will follow.]
