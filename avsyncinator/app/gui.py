import os
import tkinter as tk
from tkinter import ttk
import threading, queue
from . import logger
from .. import dirsetup, dirteardown, APPDIR
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showinfo, showerror
from .localisation import translate as _
from .util import timestamps_video_and_audio_for_file
from .testdata import testdata
from . import processing
import sys

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
        self.arg_audio_threshold = tk.IntVar(); self.arg_audio_threshold.set(-50)
        self.arg_audio_interval = tk.IntVar(); self.arg_audio_interval.set(1)
        self.arg_video_color_diff = tk.IntVar(); self.arg_video_color_diff.set(30)
        self.arg_video_color_ratio = tk.StringVar(); self.arg_video_color_ratio.set('0.7')
        self.arg_try_match = tk.BooleanVar(); self.arg_try_match.set(True)
        self._log_output = tk.StringVar(); self._log_output.set('hi')

        self.analysis_queue = queue.Queue()

        master.title(_('AV-Syncinator'))
        if os.name == 'nt':
            master.iconbitmap(APPDIR + 'res' + os.sep + 'logo' + os.sep + 'logo.ico')
        master.resizable(False, False)
        master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.frame = tk.Frame(self.master, borderwidth=10)

        self.lblFilename = tk.Label(self.frame, text=_('File to analyze: '))
        self.lblFilename.grid(row=0, column=0, sticky='w')
        self.txtFilename = tk.Entry(self.frame, textvariable=self.arg_selected_file, width=50)
        self.txtFilename.grid(row=0, column=1, columnspan=5)
        self.btnBrowse = tk.Button(self.frame, text=_('Browse'), command=self._openfile)
        self.btnBrowse.grid(row=0, column=7, padx=10)


        self.lblAudioThreshold = tk.Label(self.frame, text=_('Audio Threshold: '))
        self.lblAudioThreshold.grid(row=1, column=0, sticky='w', pady=5)
        self.txtAudioThreshold = tk.Entry(
            self.frame, textvariable=self.arg_audio_threshold, width=5)
        self.txtAudioThreshold.grid(row=1, column=1)
        self.btnAudioThresholdInfo = tk.Button(
            self.frame, text='?', command=lambda: self._info('audio_threshold')
        )
        self.btnAudioThresholdInfo.grid(row=1, column=2, sticky='w')

        self.lblAudioInterval = tk.Label(self.frame, text=_('Audio Interval: '))
        self.lblAudioInterval.grid(row=1, column=3, sticky='w')
        self.txtAudioInterval = tk.Entry(
            self.frame, textvariable=self.arg_audio_interval, width=5)
        self.txtAudioInterval.grid(row=1, column=4)
        self.btnAudioIntervalInfo = tk.Button(
            self.frame, text='?', command=lambda: self._info('audio_interval')
        )
        self.btnAudioIntervalInfo.grid(row=1, column=5, sticky='w')

        self.lblVideoColorDiff = tk.Label(self.frame, text=_('Video Color Diff: '))
        self.lblVideoColorDiff.grid(row=2, column=0, sticky='w', pady=5)
        self.txtVideoColorDiff = tk.Entry(
            self.frame, textvariable=self.arg_video_color_diff, width=5)
        self.txtVideoColorDiff.grid(row=2, column=1)
        self.btnVideoColorDiffInfo = tk.Button(
            self.frame, text='?', command=lambda: self._info('video_color_diff')
        )
        self.btnVideoColorDiffInfo.grid(row=2, column=2, sticky='w')

        self.lblVideoColorRatio = tk.Label(self.frame, text=_('Video Color Ratio: '))
        self.lblVideoColorRatio.grid(row=2, column=3, sticky='w')
        self.txtVideoColorRatio = tk.Entry(
            self.frame, textvariable=self.arg_video_color_ratio, width=5)
        self.txtVideoColorRatio.grid(row=2, column=4)
        self.btnVideoColorRatioInfo = tk.Button(
            self.frame, text='?', command=lambda: self._info('video_color_ratio')
        )
        self.btnVideoColorRatioInfo.grid(row=2, column=5, sticky='w')

        self.comboOutputFormat = ttk.Combobox(self.frame, values = [
            _('Plot Image'), _('.csv File')
        ])
        self.comboOutputFormat.grid(row=3, column=0, columnspan=2, sticky='w', pady=5)
        self.comboOutputFormat.current(0)
        self.comboOutputFormatInfo = tk.Button(
            self.frame, text='?', command=lambda: self._info('output_format')
        )
        self.comboOutputFormatInfo.grid(row=3, column=2, sticky='w')

        self.chkTryMatch = tk.Checkbutton(self.frame, text=_('Try ignoring stutters'),
                                          var=self.arg_try_match)
        self.chkTryMatch.grid(row=3, column=3, columnspan=2, sticky='w')
        self.btnTryMatchInfo = tk.Button(
            self.frame, text='?', command=lambda: self._info('try_match')
        )
        self.btnTryMatchInfo.grid(row=3, column=5, sticky='w')

        self.btnSubmit = tk.Button(self.frame, text=_('Analyze'), command=self.analyze,
                                   bg='lightblue')
        self.btnSubmit.grid(row=4, column=0, sticky='w', pady=5)

        self.logOutput = LogOutput(self.frame)
        self.logOutput.grid(row=5, column=0, columnspan=8)
        self.logOutput.config(width=480, height=420)
        logger.Logger.get_instance().output_function = self.logOutput.log
        Log.info('Startup')

        self.frame.pack(pady=5)


    def analyze(self):
        threading.Thread(target=self._analyze).start()
        self.action_after_analysis()


    def _analyze(self):
        """ Fill `self.analysis_queue` with data."""
        try:
            if self.arg_selected_file.get() == '':
                showerror(_('Error'), _('No file selected!'))
                return
            if self.arg_selected_file.get() == '__test__':
                tv, ta = testdata['timestamps_video'], testdata['timestamps_audio']
            else:
                tv, ta = timestamps_video_and_audio_for_file(
                    videofile                   = self.arg_selected_file.get(),
                    video_threshold_color_diff  = self.arg_video_color_diff.get(),
                    video_threshold_color_ratio = float(self.arg_video_color_ratio.get()),
                    audio_interval_ms           = self.arg_audio_interval.get(),
                    audio_threshold_volume_db   = self.arg_audio_threshold.get(),
                    try_ignore_stutters_by_matching = self.arg_try_match.get(),
                )
            self.analysis_queue.put((tv, ta))
        except:
            Log.error('Failed Analysis')
            showerror('Error', 'Unexpected error:' + str(sys.exc_info()[0]))


    def action_after_analysis(self):
        """ Check if there is something in the queue, then take action. """
        try:
            res = self.analysis_queue.get(0)
            if self.comboOutputFormat.get() == _('.csv File'):
                filename = asksaveasfilename(defaultextension = '.csv')
                processing.save_as_csv(res[0], res[1], filename, {
                    'video_color_diff': self.arg_video_color_diff.get(),
                    'video_color_ratio': self.arg_video_color_ratio.get(),
                    'audio_interval': self.arg_audio_interval.get(),
                    'audio_threshold': self.arg_audio_threshold.get(),
                    'try_match': self.arg_try_match.get(),
                })
            else:
                processing.plot_sync_accuracy(res[0], res[1])
        except queue.Empty:
            self.master.after(100, self.action_after_analysis)
        except PermissionError:
            Log.error("Could not open file")
            showerror('Error', _(
                'Could not open file. Please check that is not opened in ' +
                'another application'
            ))

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
                                   ' trigger a data point [0-1]'),
            'output_format': _(
                'The result of the analysis can either be saved as a .csv file ' +
                'for further processing (.csv can for example be opened up in ' +
                'Excel) or as a plot.'
            ),
            'try_match': _(
                'Too many stutters in the audio of the selected video file may ' +
                'result in too many audio timestamps being recorded. This can ' +
                'drastically influence measurements for timestamps after the ' +
                'stutter. Therefore this toggle matches video timestamps with ' +
                'the \'closest\' audio timestamps in order to ignore these ' +
                'stutters. It should likely always be turned on - although it ' +
                'may lead to incorrect results in scenarios with /really/ high ' +
                'latency.'
            )
        }
        showinfo(_("Parameter Description"), info[key])


    def on_closing(self):
        dirteardown()
        root.destroy()


root = tk.Tk()
my_gui = App(root)
root.mainloop()