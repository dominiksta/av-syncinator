import os
import tkinter as tk
import threading, queue
import logger
import common
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo, showerror
from localisation import translate as _
from util import timestamps_video_and_video_for_file
from testdata import testdata
import plotting
import sys

common.dirsetup()
Log = logger.Logger.get_instance()

class LogOutput(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_propagate(False) # ensure a consistent GUI size
        self.grid_rowconfigure(0, weight=1) # implement stretchability
        self.grid_columnconfigure(0, weight=1)

        self.txt = tk.Text(self, font='TkFixedFont', state='disabled')
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        scrollb = tk.Scrollbar(self, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set


    def log(self, msg: str):
        self.txt.config(state = 'normal')
        self.txt.insert(tk.END, msg + '\n')
        self.txt.see(tk.END)
        self.txt.config(state = 'disabled')


class App:
    def __init__(self, master):
        self.master = master
        self.arg_selected_file = tk.StringVar()
        self.arg_selected_file.set('')
        self.arg_audio_threshold = tk.IntVar(); self.arg_audio_threshold.set(-100)
        self.arg_audio_interval = tk.IntVar(); self.arg_audio_interval.set(10)
        self.arg_video_color_diff= tk.IntVar(); self.arg_video_color_diff.set(30)
        self.arg_video_color_ratio= tk.StringVar(); self.arg_video_color_ratio.set('0.7')
        self._log_output = tk.StringVar(); self._log_output.set('hi')

        self.analysis_queue = queue.Queue()

        master.title(_('AV-Syncinator'))
        master.geometry('500x600')
        master.iconbitmap(common.APPDIR + 'res' + os.sep + 'logo' + os.sep + 'logo.ico')
        master.resizable(False, False)
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.lblFilename = tk.Label(master, text=_('File to analyze: '))
        self.lblFilename.place(x=10, y=10)
        self.txtFilename = tk.Entry(master, textvariable=self.arg_selected_file, width=50)
        self.txtFilename.place(x=120, y=12)
        self.btnBrowse = tk.Button(master, text=_('Browse'), command=self._openfile)
        self.btnBrowse.place(x=430, y=8)


        self.lblAudioThreshold = tk.Label(master, text=_('Audio Threshold: '))
        self.lblAudioThreshold.place(x=10, y=40)
        self.txtAudioThreshold = tk.Entry(
            master, textvariable=self.arg_audio_threshold, width=5)
        self.txtAudioThreshold.place(x=120, y=42)
        self.btnAudioThresholdInfo = tk.Button(
            master, text='?', command=lambda: self._info('audio_threshold')
        )
        self.btnAudioThresholdInfo.place(x=160, y=38)

        self.lblAudioInterval = tk.Label(master, text=_('Audio Interval: '))
        self.lblAudioInterval.place(x=10, y=70)
        self.txtAudioInterval = tk.Entry(
            master, textvariable=self.arg_audio_interval, width=5)
        self.txtAudioInterval.place(x=120, y=72)
        self.btnAudioIntervalInfo = tk.Button(
            master, text='?', command=lambda: self._info('audio_interval')
        )
        self.btnAudioIntervalInfo.place(x=160, y=68)

        self.lblVideoColorDiff = tk.Label(master, text=_('Video Color Diff: '))
        self.lblVideoColorDiff.place(x=200, y=40)
        self.txtVideoColorDiff = tk.Entry(
            master, textvariable=self.arg_video_color_diff, width=5)
        self.txtVideoColorDiff.place(x=310, y=42)
        self.btnVideoColorDiffInfo = tk.Button(
            master, text='?', command=lambda: self._info('video_color_diff')
        )
        self.btnVideoColorDiffInfo.place(x=350, y=38)

        self.lblVideoColorRatio = tk.Label(master, text=_('Video Color Ratio: '))
        self.lblVideoColorRatio.place(x=200, y=70)
        self.txtVideoColorRatio = tk.Entry(
            master, textvariable=self.arg_video_color_ratio, width=5)
        self.txtVideoColorRatio.place(x=310, y=72)
        self.btnVideoColorRatioInfo = tk.Button(
            master, text='?', command=lambda: self._info('video_color_ratio')
        )
        self.btnVideoColorRatioInfo.place(x=350, y=68)

        self.logOutput = LogOutput()
        self.logOutput.place(x=10, y=140)
        self.logOutput.config(width=480, height=440)
        logger.Logger.get_instance().output_function = self.logOutput.log
        Log.info('Startup')

        self.btnSubmit = tk.Button(master, text=_('Analyze'), command=self.analyze,
                                   bg='lightblue')
        self.btnSubmit.place(x=12, y=100)


    def analyze(self):
        threading.Thread(target=self._analyze).start()
        self.display_when_ready()


    def _analyze(self):
        """ Fill `self.analysis_queue` with data."""
        try:
            if self.arg_selected_file.get() == '':
                showerror(_('Error'), _('No file selected!'))
                return
            if self.arg_selected_file.get() == '__test__':
                tv, ta = testdata['timestamps_video'], testdata['timestamps_audio']
            else:
                tv, ta = timestamps_video_and_video_for_file(
                    videofile                   = self.arg_selected_file.get(),
                    video_threshold_color_diff  = self.arg_video_color_diff.get(),
                    video_threshold_color_ratio = float(self.arg_video_color_ratio.get()),
                    audio_interval_ms           = self.arg_audio_interval.get(),
                    audio_threshold_volume_db   = self.arg_audio_threshold.get(),
                )
            self.analysis_queue.put((tv, ta))
        except:
            Log.error('Failed Analysis')
            showerror('Error', 'Unexpected error:' + str(sys.exc_info()[0]))


    def display_when_ready(self):
        """ Check if there is something in the queue, then display. """
        try:
            res = self.analysis_queue.get(0)
            plotting.plot_sync_accuracy(res[0], res[1])
        except queue.Empty:
            self.master.after(100, self.display_when_ready)


    def _openfile(self):
        self.arg_selected_file.set(askopenfilename(filetypes=[
            (_('Video Files'), '.mp4 .mkv'),
            (_('All Files'), '*'),
        ]))


    def _info(self, key):
        info = {
            'audio_threshold': _('How long the audio has to be to trigger' +
                                 ' a data point (in dB from -inf to 0).'),
            'audio_interval': _('Step size for scanning the audio [ms]'),
            'video_color_diff': _('How much the color in the video may differ' +
                                  ' from white [0-255] to trigger a data point.'),
            'video_color_ratio': _('How much of the screen has to be white to' +
                                   ' trigger a data point [0-1]')
        }
        showinfo(_("Parameter Description"), info[key])


    def on_closing(self):
        common.dirteardown()
        root.destroy()


root = tk.Tk()
my_gui = App(root)
root.mainloop()