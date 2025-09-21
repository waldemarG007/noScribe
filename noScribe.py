# noScribe - AI-powered Audio Transcription
# Copyright (C) 2025 Kai Dröge
# ported to MAC by Philipp Schneider (gernophil)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
# In the compiled version (no command line), stdout is None which might lead to errors
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

import tkinter as tk
import customtkinter as ctk
from tkHyperlinkManager import HyperlinkManager
import webbrowser
from functools import partial
from PIL import Image
import os
import platform
import yaml
import locale
import appdirs
from subprocess import run, call, Popen, PIPE, STDOUT
if platform.system() == 'Windows':
    # import torch.cuda # to check with torch.cuda.is_available()
    from subprocess import STARTUPINFO, STARTF_USESHOWWINDOW
if platform.system() in ("Windows", "Linux"):
    from ctranslate2 import get_cuda_device_count
    import torch
import re
if platform.system() == "Darwin": # = MAC
    from subprocess import check_output
    if platform.machine() == "x86_64":
        os.environ['KMP_DUPLICATE_LIB_OK']='True' # prevent OMP: Error #15: Initializing libomp.dylib, but found libiomp5.dylib already initialized.
    # import torch.backends.mps # loading torch modules leads to segmentation fault later
from faster_whisper.audio import decode_audio
from faster_whisper.vad import VadOptions, get_speech_timestamps
import AdvancedHTMLParser
import html
from threading import Thread
import time
from tempfile import TemporaryDirectory
import datetime
from pathlib import Path
if platform.system() in ("Darwin", "Linux"):
    import shlex
if platform.system() == 'Windows':
    import cpufeature
if platform.system() == 'Darwin':
    import Foundation
import logging
import json
import urllib
import multiprocessing
import gc
import traceback
from transcriber import run_transcription, get_whisper_models as get_transcriber_whisper_models

# Pyinstaller fix, used to open multiple instances on Mac
multiprocessing.freeze_support()

logging.basicConfig()
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

app_version = '0.6.2'
app_year = '2025'
app_dir = os.path.abspath(os.path.dirname(__file__))

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

default_html = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html >
<head >
<meta charset="UTF-8" />
<meta name="qrichtext" content="1" />
<style type="text/css" >
p, li { white-space: pre-wrap; }
</style>
<style type="text/css" > 
 p { font-size: 0.9em; } 
 .MsoNormal { font-family: "Arial"; font-weight: 400; font-style: normal; font-size: 0.9em; }
 @page WordSection1 {mso-line-numbers-restart: continuous; mso-line-numbers-count-by: 1; mso-line-numbers-start: 1; }
 div.WordSection1 {page:WordSection1;} 
</style>
</head>
<body style="font-family: 'Arial'; font-weight: 400; font-style: normal" >
</body>
</html>"""

languages = {
    "Auto": "auto",
    "Multilingual": "multilingual",
    "Afrikaans": "af",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azerbaijani": "az",
    "Belarusian": "be",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Chinese": "zh",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Estonian": "et",
    "Finnish": "fi",
    "French": "fr",
    "Galician": "gl",
    "German": "de",
    "Greek": "el",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Indonesian": "id",
    "Italian": "it",
    "Japanese": "ja",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Korean": "ko",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Macedonian": "mk",
    "Malay": "ms",
    "Marathi": "mr",
    "Maori": "mi",
    "Nepali": "ne",
    "Norwegian": "no",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Romanian": "ro",
    "Russian": "ru",
    "Serbian": "sr",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Spanish": "es",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tagalog": "tl",
    "Tamil": "ta",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Vietnamese": "vi",
    "Welsh": "cy",
}

# config
config_dir = appdirs.user_config_dir('noScribe')
if not os.path.exists(config_dir):
    os.makedirs(config_dir)

config_file = os.path.join(config_dir, 'config.yml')

try:
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
        if not config:
            raise # config file is empty (None)        
except: # seems we run it for the first time and there is no config file
    config = {}
    
def get_config(key: str, default):
    """ Get a config value, set it if it doesn't exist """
    if key not in config:
        config[key] = default
    return config[key]

    
def version_higher(version1, version2) -> int:
    """Will return 
    1 if version1 is higher
    2 if version2 is higher
    0  if both are equal """
    version1_elems = version1.split('.')
    version2_elems = version2.split('.')
    # make both versions the same length
    elem_num = max(len(version1_elems), len(version2_elems))
    while len(version1_elems) < elem_num:
        version1_elems.append('0')
    while len(version1_elems) < elem_num:
        version1_elems.append('0')
    for i in range(elem_num):
        if int(version1_elems[i]) > int(version2_elems[i]):
            return 1
        elif int(version2_elems[i]) > int(version1_elems[i]):
            return 2
    # must be completly equal
    return 0
    
# In versions < 0.4.5 (Windows/Linux only), 'pyannote_xpu' was always set to 'cpu'.
# Delete this so we can determine the optimal value  
if platform.system() in ('Windows', 'Linux'):
    try:
        if version_higher('0.4.5', config['app_version']) == 1:
            del config['pyannote_xpu'] 
    except:
        pass

config['app_version'] = app_version

def save_config():
    with open(config_file, 'w') as file:
        yaml.safe_dump(config, file)

save_config()

# locale: setting the language of the UI
# see https://pypi.org/project/python-i18n/
import i18n
from i18n import t
i18n.set('filename_format', '{locale}.{format}')
i18n.load_path.append(os.path.join(app_dir, 'trans'))

try:
    app_locale = config['locale']
except:
    app_locale = 'auto'

if app_locale == 'auto': # read system locale settings
    try:
        if platform.system() == 'Windows':
            app_locale = locale.getdefaultlocale()[0][0:2]
        elif platform.system() == "Darwin": # = MAC
            app_locale = Foundation.NSUserDefaults.standardUserDefaults().stringForKey_('AppleLocale')[0:2]
    except:
        app_locale = 'en'
i18n.set('fallback', 'en')
i18n.set('locale', app_locale)
config['locale'] = app_locale

# determine optimal number of threads for faster-whisper (depending on cpu cores)
if platform.system() == 'Windows':
    number_threads = get_config('threads', cpufeature.CPUFeature["num_physical_cores"])
elif platform.system() == "Linux":
    number_threads = get_config('threads', os.cpu_count() if os.cpu_count() is not None else 4)
elif platform.system() == "Darwin": # = MAC
    if platform.machine() == "arm64":
        cpu_count = int(check_output(["sysctl", "-n", "hw.perflevel0.logicalcpu_max"]))
    elif platform.machine() == "x86_64":
        cpu_count = int(check_output(["sysctl", "-n", "hw.logicalcpu_max"]))
    else:
        raise Exception("Unsupported mac")
    number_threads = get_config('threads', int(cpu_count * 0.75))
else:
    raise Exception('Platform not supported yet.')

# timestamp regex
timestamp_re = re.compile('\[\d\d:\d\d:\d\d.\d\d\d --> \d\d:\d\d:\d\d.\d\d\d\]')

# Helper functions

def millisec(timeStr: str) -> int:
    """ Convert 'hh:mm:ss' string into milliseconds """
    try:
        h, m, s = timeStr.split(':')
        return (int(h) * 3600 + int(m) * 60 + int(s)) * 1000 # https://stackoverflow.com/a/6402859
    except:
        raise Exception(t('err_invalid_time_string', time = timeStr))

def ms_to_str(milliseconds: float, include_ms=False):
    """ Convert milliseconds into formatted timestamp 'hh:mm:ss' """
    seconds, milliseconds = divmod(milliseconds,1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    formatted = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    if include_ms:
        formatted += f'.{milliseconds:03d}'
    return formatted 

def iter_except(function, exception):
        # Works like builtin 2-argument `iter()`, but stops on `exception`.
        try:
            while True:
                yield function()
        except exception:
            return
        
# Helper for text only output
        
def html_node_to_text(node: AdvancedHTMLParser.AdvancedTag) -> str:
    """
    Recursively get all text from a html node and its children. 
    """
    # For text nodes, return their value directly
    if AdvancedHTMLParser.isTextNode(node): # node.nodeType == node.TEXT_NODE:
        return html.unescape(node)
    # For element nodes, recursively process their children
    elif AdvancedHTMLParser.isTagNode(node):
        text_parts = []
        for child in node.childBlocks:
            text = html_node_to_text(child)
            if text:
                text_parts.append(text)
        # For block-level elements, prepend and append newlines
        if node.tagName.lower() in ['p', 'div', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br']:
            if node.tagName.lower() == 'br':
                return '\n'
            else:
                return '\n' + ''.join(text_parts).strip() + '\n'
        else:
            return ''.join(text_parts)
    else:
        return ''

def html_to_text(parser: AdvancedHTMLParser.AdvancedHTMLParser) -> str:
    return html_node_to_text(parser.body)

# Helper for WebVTT output

def vtt_escape(txt: str) -> str:
    txt = html.escape(txt)
    while txt.find('\n\n') > -1:
        txt = txt.replace('\n\n', '\n')
    return txt    

def ms_to_webvtt(milliseconds) -> str:
    """converts milliseconds to the time stamp of WebVTT (HH:MM:SS.mmm)
    """
    # 1 hour = 3600000 milliseconds
    # 1 minute = 60000 milliseconds
    # 1 second = 1000 milliseconds
    hours, milliseconds = divmod(milliseconds, 3600000)
    minutes, milliseconds = divmod(milliseconds, 60000)
    seconds, milliseconds = divmod(milliseconds, 1000)
    return "{:02d}:{:02d}:{:02d}.{:03d}".format(hours, minutes, seconds, milliseconds)

def html_to_webvtt(parser: AdvancedHTMLParser.AdvancedHTMLParser, media_path: str):
    vtt = 'WEBVTT '
    paragraphs = parser.getElementsByTagName('p')
    # The first paragraph contains the title
    vtt += vtt_escape(paragraphs[0].textContent) + '\n\n'
    # Next paragraph contains info about the transcript. Add as a note.
    vtt += vtt_escape('NOTE\n' + html_node_to_text(paragraphs[1])) + '\n\n'
    # Add media source:
    vtt += f'NOTE media: {media_path}\n\n'

    #Add all segments as VTT cues
    segments = parser.getElementsByTagName('a')
    i = 0
    for i in range(len(segments)):
        segment = segments[i]
        name = segment.attributes['name']
        if name is not None:
            name_elems = name.split('_', 4)
            if len(name_elems) > 1 and name_elems[0] == 'ts':
                start = ms_to_webvtt(int(name_elems[1]))
                end = ms_to_webvtt(int(name_elems[2]))
                spkr = name_elems[3]
                txt = vtt_escape(html_node_to_text(segment))
                vtt += f'{i+1}\n{start} --> {end}\n<v {spkr}>{txt.lstrip()}\n\n'
    return vtt
    
class TimeEntry(ctk.CTkEntry): # special Entry box to enter time in the format hh:mm:ss
                               # based on https://stackoverflow.com/questions/63622880/how-to-make-python-automatically-put-colon-in-the-format-of-time-hhmmss
    def __init__(self, master, **kwargs):
        ctk.CTkEntry.__init__(self, master, **kwargs)
        vcmd = self.register(self.validate)

        self.bind('<Key>', self.format)
        self.configure(validate="all", validatecommand=(vcmd, '%P'))

        self.valid = re.compile('^\d{0,2}(:\d{0,2}(:\d{0,2})?)?$', re.I)

    def validate(self, text):
        if text == '':
            return True
        elif ''.join(text.split(':')).isnumeric():
            return not self.valid.match(text) is None
        else:
            return False

    def format(self, event):
        if event.keysym not in ['BackSpace', 'Shift_L', 'Shift_R', 'Control_L', 'Control_R']:
            i = self.index('insert')
            if i in [2, 5]:
                if event.char != ':':
                    if self.get()[i:i+1] != ':':
                        self.insert(i, ':')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.user_models_dir = os.path.join(config_dir, 'whisper_models')
        os.makedirs(self.user_models_dir, exist_ok=True)
        whisper_models_readme = os.path.join(self.user_models_dir, 'readme.txt')
        if not os.path.exists(whisper_models_readme):
            with open(whisper_models_readme, 'w') as file:
                file.write('You can download custom Whisper-models for the transcription into this folder. \n' 
                           'See here for more information: https://github.com/kaixxx/noScribe/wiki/Add-custom-Whisper-models-for-transcription')            
        
        self.audio_file = ''
        self.transcript_file = ''
        self.log_file = None
        self.cancel = False # if set to True, transcription will be canceled

        # configure window
        self.title('noScribe - ' + t('app_header'))
        if platform.system() in ("Darwin", "Linux"):
            self.geometry(f"{1100}x{765}")
        else:
            self.geometry(f"{1100}x{690}")
        if platform.system() in ("Darwin", "Windows"):
            self.iconbitmap(os.path.join(app_dir, 'noScribeLogo.ico'))
        if platform.system() == "Linux":
            if hasattr(sys, "_MEIPASS"):
                self.iconphoto(True, tk.PhotoImage(file=os.path.join(sys._MEIPASS, "noScribeLogo.png")))
            else:
                self.iconphoto(True, tk.PhotoImage(file='noScribeLogo.png'))

        # header
        self.frame_header = ctk.CTkFrame(self, height=100)
        self.frame_header.pack(padx=0, pady=0, anchor='nw', fill='x')

        self.frame_header_logo = ctk.CTkFrame(self.frame_header, fg_color='transparent')
        self.frame_header_logo.pack(anchor='w', side='left')

        # logo
        self.logo_label = ctk.CTkLabel(self.frame_header_logo, text="noScribe", font=ctk.CTkFont(size=42, weight="bold"))
        self.logo_label.pack(padx=20, pady=[40, 0], anchor='w')

        # sub header
        self.header_label = ctk.CTkLabel(self.frame_header_logo, text=t('app_header'), font=ctk.CTkFont(size=16, weight="bold"))
        self.header_label.pack(padx=20, pady=[0, 20], anchor='w')

        # graphic
        self.header_graphic = ctk.CTkImage(dark_image=Image.open(os.path.join(app_dir, 'graphic_sw.png')), size=(926,119))
        self.header_graphic_label = ctk.CTkLabel(self.frame_header, image=self.header_graphic, text='')
        self.header_graphic_label.pack(anchor='ne', side='right', padx=[30,30])

        # main window
        self.frame_main = ctk.CTkFrame(self)
        self.frame_main.pack(padx=0, pady=0, anchor='nw', expand=True, fill='both')

        # create sidebar frame for options
        self.sidebar_frame = ctk.CTkFrame(self.frame_main, width=300, corner_radius=0, fg_color='transparent')
        self.sidebar_frame.pack(padx=0, pady=0, fill='y', expand=False, side='left')

        # create options scrollable frame
        self.scrollable_options = ctk.CTkScrollableFrame(self.sidebar_frame, width=300, corner_radius=0, fg_color='transparent')
        self.scrollable_options.pack(padx=0, pady=0, anchor='w', fill='both', expand=True)
        self.bind('<Configure>', self.on_resize) # Bind the configure event of options_frame to a check_scrollbar requirement function
        
        # input audio file
        self.label_audio_file = ctk.CTkLabel(self.scrollable_options, text=t('label_audio_file'))
        self.label_audio_file.pack(padx=20, pady=[20,0], anchor='w')

        self.frame_audio_file = ctk.CTkFrame(self.scrollable_options, width=260, height=33, corner_radius=8, border_width=2)
        self.frame_audio_file.pack(padx=20, pady=[0,10], anchor='w')

        self.button_audio_file_name = ctk.CTkButton(self.frame_audio_file, width=200, corner_radius=8, bg_color='transparent', 
                                                    fg_color='transparent', hover_color=self.frame_audio_file._bg_color, 
                                                    border_width=0, anchor='w',  
                                                    text=t('label_audio_file_name'), command=self.button_audio_file_event)
        self.button_audio_file_name.place(x=3, y=3)

        self.button_audio_file = ctk.CTkButton(self.frame_audio_file, width=45, height=29, text='📂', command=self.button_audio_file_event)
        self.button_audio_file.place(x=213, y=2)

        # input transcript file name
        self.label_transcript_file = ctk.CTkLabel(self.scrollable_options, text=t('label_transcript_file'))
        self.label_transcript_file.pack(padx=20, pady=[10,0], anchor='w')

        self.frame_transcript_file = ctk.CTkFrame(self.scrollable_options, width=260, height=33, corner_radius=8, border_width=2)
        self.frame_transcript_file.pack(padx=20, pady=[0,10], anchor='w')

        self.button_transcript_file_name = ctk.CTkButton(self.frame_transcript_file, width=200, corner_radius=8, bg_color='transparent', 
                                                    fg_color='transparent', hover_color=self.frame_transcript_file._bg_color, 
                                                    border_width=0, anchor='w',  
                                                    text=t('label_transcript_file_name'), command=self.button_transcript_file_event)
        self.button_transcript_file_name.place(x=3, y=3)

        self.button_transcript_file = ctk.CTkButton(self.frame_transcript_file, width=45, height=29, text='📂', command=self.button_transcript_file_event)
        self.button_transcript_file.place(x=213, y=2)

        # Options grid
        self.frame_options = ctk.CTkFrame(self.scrollable_options, width=250, fg_color='transparent')
        self.frame_options.pack_propagate(False)
        self.frame_options.pack(padx=20, pady=10, anchor='w', fill='x')

        # self.frame_options.grid_configure .resizable(width=False, height=True)
        self.frame_options.grid_columnconfigure(0, weight=1, minsize=0)
        self.frame_options.grid_columnconfigure(1, weight=0)

        # Start/stop
        self.label_start = ctk.CTkLabel(self.frame_options, text=t('label_start'))
        self.label_start.grid(column=0, row=0, sticky='w', pady=[0,5])

        self.entry_start = TimeEntry(self.frame_options, width=100)
        self.entry_start.grid(column='1', row='0', sticky='e', pady=[0,5])
        self.entry_start.insert(0, '00:00:00')

        self.label_stop = ctk.CTkLabel(self.frame_options, text=t('label_stop'))
        self.label_stop.grid(column=0, row=1, sticky='w', pady=[5,10])

        self.entry_stop = TimeEntry(self.frame_options, width=100)
        self.entry_stop.grid(column='1', row='1', sticky='e', pady=[5,10])

        # language
        self.label_language = ctk.CTkLabel(self.frame_options, text=t('label_language'))
        self.label_language.grid(column=0, row=2, sticky='w', pady=5)

        self.option_menu_language = ctk.CTkOptionMenu(self.frame_options, width=100, values=list(languages.keys()), dynamic_resizing=False)
        self.option_menu_language.grid(column=1, row=2, sticky='e', pady=5)
        last_language = get_config('last_language', 'auto')
        if last_language in languages.keys():
            self.option_menu_language.set(last_language)
        else:
            self.option_menu_language.set('Auto')
        
        # Whisper Model Selection   
        class CustomCTkOptionMenu(ctk.CTkOptionMenu):
            # Custom version that reads available models on drop down
            def __init__(self, noScribe_parent, master, width = 140, height = 28, corner_radius = None, bg_color = "transparent", fg_color = None, button_color = None, button_hover_color = None, text_color = None, text_color_disabled = None, dropdown_fg_color = None, dropdown_hover_color = None, dropdown_text_color = None, font = None, dropdown_font = None, values = None, variable = None, state = tk.NORMAL, hover = True, command = None, dynamic_resizing = True, anchor = "w", **kwargs):
                super().__init__(master, width, height, corner_radius, bg_color, fg_color, button_color, button_hover_color, text_color, text_color_disabled, dropdown_fg_color, dropdown_hover_color, dropdown_text_color, font, dropdown_font, values, variable, state, hover, command, dynamic_resizing, anchor, **kwargs)
                self.noScribe_parent = noScribe_parent
                self.old_value = ''

            def _clicked(self, event=0):
                self.old_value = self.get()
                self._values = self.noScribe_parent.get_whisper_models()
                self._values.append('--------------------')
                self._values.append(t('label_add_custom_models'))
                self._dropdown_menu.configure(values=self._values)
                super()._clicked(event)
                
            def _dropdown_callback(self, value: str):
                if value == self._values[-2]:  # divider
                    return
                if value == self._values[-1]:  # Add custom model
                    # show custom model folder
                    path = self.noScribe_parent.user_models_dir
                    try:
                        os_type = platform.system()
                        if os_type == "Windows":
                            os.startfile(path)
                        elif os_type == "Darwin":
                            run(["open", path])
                        elif os_type == "Linux":
                            run(["xdg-open", path])
                        else:
                            raise OSError(f"Unsupported operating system: {os_type}")
                    except Exception as e:
                        self.noScribe_parent.logn(f"Failed to open folder: {e}")
                else:
                    super()._dropdown_callback(value)
        
        self.label_whisper_model = ctk.CTkLabel(self.frame_options, text=t('label_whisper_model'))
        self.label_whisper_model.grid(column=0, row=3, sticky='w', pady=5)

        models = self.get_whisper_models()
        self.option_menu_whisper_model = CustomCTkOptionMenu(self, 
                                                       self.frame_options, 
                                                       width=100,
                                                       values=models,
                                                       dynamic_resizing=False)
        self.option_menu_whisper_model.grid(column=1, row=3, sticky='e', pady=5)
        last_whisper_model = get_config('last_whisper_model', 'precise')
        if last_whisper_model in models:
            self.option_menu_whisper_model.set(last_whisper_model)
        elif len(models) > 0:
            self.option_menu_whisper_model.set(models[0])

        # Mark pauses
        self.label_pause = ctk.CTkLabel(self.frame_options, text=t('label_pause'))
        self.label_pause.grid(column=0, row=4, sticky='w', pady=5)

        self.option_menu_pause = ctk.CTkOptionMenu(self.frame_options, width=100, values=['none', '1sec+', '2sec+', '3sec+'])
        self.option_menu_pause.grid(column=1, row=4, sticky='e', pady=5)
        self.option_menu_pause.set(get_config('last_pause', '1sec+'))

        # Speaker Detection (Diarization)
        self.label_speaker = ctk.CTkLabel(self.frame_options, text=t('label_speaker'))
        self.label_speaker.grid(column=0, row=5, sticky='w', pady=5)

        self.option_menu_speaker = ctk.CTkOptionMenu(self.frame_options, width=100, values=['none', 'auto', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
        self.option_menu_speaker.grid(column=1, row=5, sticky='e', pady=5)
        self.option_menu_speaker.set(get_config('last_speaker', 'auto'))

        # Overlapping Speech (Diarization)
        self.label_overlapping = ctk.CTkLabel(self.frame_options, text=t('label_overlapping'))
        self.label_overlapping.grid(column=0, row=6, sticky='w', pady=5)

        self.check_box_overlapping = ctk.CTkCheckBox(self.frame_options, text = '')
        self.check_box_overlapping.grid(column=1, row=6, sticky='e', pady=5)
        overlapping = config.get('last_overlapping', True)
        if overlapping:
            self.check_box_overlapping.select()
        else:
            self.check_box_overlapping.deselect()
            
        # Disfluencies
        self.label_disfluencies = ctk.CTkLabel(self.frame_options, text=t('label_disfluencies'))
        self.label_disfluencies.grid(column=0, row=7, sticky='w', pady=5)

        self.check_box_disfluencies = ctk.CTkCheckBox(self.frame_options, text = '')
        self.check_box_disfluencies.grid(column=1, row=7, sticky='e', pady=5)
        check_box_disfluencies = config.get('last_disfluencies', True)
        if check_box_disfluencies:
            self.check_box_disfluencies.select()
        else:
            self.check_box_disfluencies.deselect()

        # Timestamps in text
        self.label_timestamps = ctk.CTkLabel(self.frame_options, text=t('label_timestamps'))
        self.label_timestamps.grid(column=0, row=8, sticky='w', pady=5)

        self.check_box_timestamps = ctk.CTkCheckBox(self.frame_options, text = '')
        self.check_box_timestamps.grid(column=1, row=8, sticky='e', pady=5)
        check_box_timestamps = config.get('last_timestamps', False)
        if check_box_timestamps:
            self.check_box_timestamps.select()
        else:
            self.check_box_timestamps.deselect()
        
        # Start Button
        self.start_button = ctk.CTkButton(self.sidebar_frame, height=42, text=t('start_button'), command=self.button_start_event)
        self.start_button.pack(padx=[20, 0], pady=[20,30], expand=False, fill='x', anchor='sw')

        # Stop Button
        self.stop_button = ctk.CTkButton(self.sidebar_frame, height=42, fg_color='darkred', hover_color='darkred', text=t('stop_button'), command=self.button_stop_event)
        
        # create log textbox
        self.log_frame = ctk.CTkFrame(self.frame_main, corner_radius=0, fg_color='transparent')
        self.log_frame.pack(padx=0, pady=0, fill='both', expand=True, side='top')

        self.log_textbox = ctk.CTkTextbox(self.log_frame, wrap='word', state="disabled", font=("",16), text_color="lightgray")
        self.log_textbox.tag_config('highlight', foreground='darkorange')
        self.log_textbox.tag_config('error', foreground='yellow')
        self.log_textbox.pack(padx=20, pady=[20,0], expand=True, fill='both')

        self.hyperlink = HyperlinkManager(self.log_textbox._textbox)

        # Frame progress bar / edit button
        self.frame_edit = ctk.CTkFrame(self.frame_main, height=20, corner_radius=0, fg_color=self.log_textbox._fg_color)
        self.frame_edit.pack(padx=20, pady=[0,30], anchor='sw', fill='x', side='bottom')

        # Edit Button
        self.edit_button = ctk.CTkButton(self.frame_edit, fg_color=self.log_textbox._scrollbar_button_color, 
                                         text=t('editor_button'), command=self.launch_editor, width=140)
        self.edit_button.pack(padx=[20,10], pady=[10,10], expand=False, anchor='se', side='right')

        # Progress bar
        self.progress_textbox = ctk.CTkTextbox(self.frame_edit, wrap='none', height=15, state="disabled", font=("",16), text_color="lightgray")
        self.progress_textbox.pack(padx=[10,10], pady=[5,0], expand=True, fill='x', anchor='sw', side='left')

        self.update_scrollbar_visibility()        
        #self.progress_bar = ctk.CTkProgressBar(self.frame_edit, mode='determinate', progress_color='darkred', fg_color=self.log_textbox._fg_color)
        #self.progress_bar.set(0)
        # self.progress_bar.pack(padx=[10,10], pady=[10,10], expand=True, fill='x', anchor='sw', side='left')

        # status bar bottom
        #self.frame_status = ctk.CTkFrame(self, height=20, corner_radius=0)
        #self.frame_status.pack(padx=0, pady=[0,0], anchor='sw', fill='x', side='bottom')

        self.logn(t('welcome_message'), 'highlight')
        self.log(t('welcome_credits', v=app_version, y=app_year))
        self.logn('https://github.com/kaixxx/noScribe', link='https://github.com/kaixxx/noScribe#readme')
        self.logn(t('welcome_instructions'))
        
        # check for new releases
        if get_config('check_for_update', 'True') == 'True':
            try:
                latest_release = json.loads(urllib.request.urlopen(
                    urllib.request.Request('https://api.github.com/repos/kaixxx/noScribe/releases/latest',
                    headers={'Accept': 'application/vnd.github.v3+json'},),
                    timeout=2).read())
                latest_release_version = str(latest_release['tag_name']).lstrip('v')
                if version_higher(latest_release_version, app_version) == 1:
                    self.logn(t('new_release', v=latest_release_version), 'highlight')
                    self.logn(str(latest_release['body'])) # release info
                    self.log(t('new_release_download'))
                    self.logn(str(latest_release['html_url']), link=str(latest_release['html_url']))
                    self.logn()
            except:
                pass
            
    # Events and Methods

    def get_whisper_models(self):
        # This now uses the refactored function from transcriber.py
        self.whisper_model_paths = get_transcriber_whisper_models()
        return list(self.whisper_model_paths.keys())
    
    def on_whisper_model_selected(self, value):
        print(self.option_menu_whisper_model.old_value)
        print(value)
        
    def on_resize(self, event):
        self.update_scrollbar_visibility()

    def update_scrollbar_visibility(self):
        # Get the size of the scroll region and current canvas size
        canvas = self.scrollable_options._parent_canvas  
        scroll_region_height = canvas.bbox("all")[3]
        canvas_height = canvas.winfo_height()        
        
        scrollbar = self.scrollable_options._scrollbar

        if scroll_region_height > canvas_height:
            scrollbar.grid()
        else:
            scrollbar.grid_remove()  # Hide the scrollbar if not needed    

    def launch_editor(self, file=''):
        # Launch the editor in a seperate process so that in can stay running even if noScribe quits.
        # Source: https://stackoverflow.com/questions/13243807/popen-waiting-for-child-process-even-when-the-immediate-child-has-terminated/13256908#13256908 
        # set system/version dependent "start_new_session" analogs
        if file == '':
            file = self.transcript_file
        ext = os.path.splitext(self.transcript_file)[1][1:]
        if file != '' and ext != 'html':
            file = ''
            if not tk.messagebox.askyesno(title='noScribe', message=t('err_editor_invalid_format')):
                return
        program: str = None
        if platform.system() == 'Windows':
            program = os.path.join(app_dir, 'noScribeEdit', 'noScribeEdit.exe')
        elif platform.system() == "Darwin": # = MAC
            # use local copy in development, installed one if used as an app:
            program = os.path.join(app_dir, 'noScribeEdit', 'noScribeEdit')
            if not os.path.exists(program):
                program = os.path.join(os.sep, 'Applications', 'noScribeEdit.app', 'Contents', 'MacOS', 'noScribeEdit')
        elif platform.system() == "Linux":
            if hasattr(sys, "_MEIPASS"):
                program = os.path.join(sys._MEIPASS, 'noScribeEdit', "noScribeEdit")
            else:
                program = os.path.join(app_dir, 'noScribeEdit', "noScribeEdit.py")
        kwargs = {}
        if platform.system() == 'Windows':
            # from msdn [1]
            CREATE_NEW_PROCESS_GROUP = 0x00000200  # note: could get it from subprocess
            DETACHED_PROCESS = 0x00000008          # 0x8 | 0x200 == 0x208
            kwargs.update(creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)  
        else:  # should work on all POSIX systems, Linux and macOS 
            kwargs.update(start_new_session=True)

        if program is not None and os.path.exists(program):
            popenargs = [program]
            if platform.system() == "Linux" and not hasattr(sys, "_MEIPASS"): # only do this, if you run as python script; Linux python vs. executable needs refinement
                popenargs = [sys.executable, program]
            if file != '':
                popenargs.append(file)
            Popen(popenargs, **kwargs)
        else:
            self.logn(t('err_noScribeEdit_not_found'), 'error')

    def openLink(self, link: str) -> None:
        if link.startswith('file://') and link.endswith('.html'):
            self.launch_editor(link[7:])
        else: 
            webbrowser.open(link)
    


    def log(self, txt: str = '', tags: list = [], where: str = 'both', link: str = '', tb: str = '') -> None:
        """ Log to main window (where can be 'screen', 'file', or 'both') 
        tb = formatted traceback of the error, only logged to file
        """
        
        # Handle screen logging if requested and textbox exists
        if where != 'file' and hasattr(self, 'log_textbox') and self.log_textbox.winfo_exists():
            try:
                self.log_textbox.configure(state=tk.NORMAL)
                
                if link:
                    tags = tags + self.hyperlink.add(partial(self.openLink, link))
                
                self.log_textbox.insert(tk.END, txt, tags)
                self.log_textbox.yview_moveto(1)  # Scroll to last line
                
                # Schedule disabling the textbox in the main thread
                self.log_textbox.after(0, lambda: self.log_textbox.configure(state=tk.DISABLED))
            except Exception as e:
                # Log screen errors only to file to prevent recursion
                if where == 'both':
                    self.log(f"Error updating log_textbox: {str(e)}\nOriginal error: {txt}", tags='error', where='file', tb=tb)

        # Handle file logging if requested
        if where != 'screen' and self.log_file and not self.log_file.closed:
            try:
                if tags == 'error':
                    txt = f'ERROR: {txt}'
                if tb != '':
                    txt = f'{txt}\nTraceback:\n{tb}' 
                self.log_file.write(txt)
                self.log_file.flush()
            except Exception as e:
                # If we get here, both screen and file logging failed
                # As a last resort, print to stderr to not lose the error
                import sys
                print(f"Critical error - both screen and file logging failed: {str(e)}\nOriginal error: {txt}\nOriginal traceback:\n{tb}", file=sys.stderr)

    def logn(self, txt: str = '', tags: list = [], where: str = 'both', link:str = '', tb: str = '') -> None:
        """ Log with a newline appended """
        self.log(f'{txt}\n', tags, where, link, tb)

    def logr(self, txt: str = '', tags: list = [], where: str = 'both', link:str = '', tb: str = '') -> None:
        """ Replace the last line of the log """
        if where != 'file':
            self.log_textbox.configure(state=ctk.NORMAL)
            self.log_textbox.delete("end-1c linestart", "end-1c")
        self.log(txt, tags, where, link, tb)

    def button_audio_file_event(self):
        fn = tk.filedialog.askopenfilename(initialdir=os.path.dirname(self.audio_file), initialfile=os.path.basename(self.audio_file))
        if fn:
            self.audio_file = fn
            self.logn(t('log_audio_file_selected') + self.audio_file)
            self.button_audio_file_name.configure(text=os.path.basename(self.audio_file))

    def button_transcript_file_event(self):
        if self.transcript_file != '':
            _initialdir = os.path.dirname(self.transcript_file)
            _initialfile = os.path.basename(self.transcript_file)
        else:
            _initialdir = os.path.dirname(self.audio_file)
            _initialfile = Path(os.path.basename(self.audio_file)).stem
        if not ('last_filetype' in config):
            config['last_filetype'] = 'html'
        filetypes = [
            ('noScribe Transcript','*.html'), 
            ('Text only','*.txt'),
            ('WebVTT Subtitles (also for EXMARaLDA)', '*.vtt')
        ]
        for i, ft in enumerate(filetypes):
            if ft[1] == f'*.{config["last_filetype"]}':
                filetypes.insert(0, filetypes.pop(i))
                break
        fn = tk.filedialog.asksaveasfilename(initialdir=_initialdir, initialfile=_initialfile, 
                                             filetypes=filetypes, 
                                             defaultextension=config['last_filetype'])
        if fn:
            self.transcript_file = fn
            self.logn(t('log_transcript_filename') + self.transcript_file)
            self.button_transcript_file_name.configure(text=os.path.basename(self.transcript_file))
            config['last_filetype'] = os.path.splitext(self.transcript_file)[1][1:]
            
    def set_progress(self, step, value):
        """ Update state of the progress bar """
        progr = -1
        if step == 1:
            progr = value * 0.05 / 100
        elif step == 2:
            progr = 0.05 # (step 1)
            progr = progr + (value * 0.45 / 100)
        elif step == 3:
            if self.speaker_detection != 'none':
                progr = 0.05 + 0.45 # (step 1 + step 2)
                progr_factor = 0.5
            else:
                progr = 0.05 # (step 1)
                progr_factor = 0.95
            progr = progr + (value * progr_factor / 100)
        if progr >= 1:
            progr = 0.99 # whisper sometimes still needs some time to finish even if the progress is already at 100%. This can be confusing, so we never go above 99%...

        # Update progress_textbox
        if progr < 0:
            progr_str = ''
        else:
            progr_str = f'({t("overall_progress")}{round(progr * 100)}%)'
        self.progress_textbox.configure(state=ctk.NORMAL)        
        self.progress_textbox.delete('1.0', tk.END)
        self.progress_textbox.insert(tk.END, progr_str)
        self.progress_textbox.configure(state=ctk.DISABLED)


    ################################################################################################
    # Main function

    def transcription_worker(self):
        # This is the main function where all the magic happens
        # We put this in a seperate thread so that it does not block the main ui

        self.cancel = False

        # Show the stop button
        self.start_button.pack_forget() # hide
        self.stop_button.pack(padx=[20, 0], pady=[20,30], expand=False, fill='x', anchor='sw')

        try:
            # collect all the options
            if self.audio_file == '':
                self.logn(t('err_no_audio_file'), 'error')
                tk.messagebox.showerror(title='noScribe', message=t('err_no_audio_file'))
                return

            if self.transcript_file == '':
                self.logn(t('err_no_transcript_file'), 'error')
                tk.messagebox.showerror(title='noScribe', message=t('err_no_transcript_file'))
                return

            start_time = self.entry_start.get()
            stop_time = self.entry_stop.get()
            sel_whisper_model = self.option_menu_whisper_model.get()
            language_name = self.option_menu_language.get()
            speaker_detection = self.option_menu_speaker.get()
            overlapping = self.check_box_overlapping.get()
            timestamps = self.check_box_timestamps.get()
            disfluencies = self.check_box_disfluencies.get()
            pause_option = self.option_menu_pause.get()

            def log_callback(message, level='info'):
                tags = []
                if level == 'error':
                    tags.append('error')
                elif level == 'highlight':
                    tags.append('highlight')
                
                # Ensure we are running in the main thread for UI updates
                self.after(0, self.logn, message, tags)


            run_transcription(
                audio_file=self.audio_file,
                transcript_file=self.transcript_file,
                language_name=language_name,
                whisper_model_name=sel_whisper_model,
                speaker_detection=speaker_detection,
                start_time=start_time,
                stop_time=stop_time,
                overlapping=overlapping,
                timestamps=timestamps,
                disfluencies=disfluencies,
                pause_option=pause_option,
                log_callback=log_callback
            )

            # auto open transcript in editor
            auto_edit_transcript = get_config('auto_edit_transcript', 'True')
            file_ext = os.path.splitext(self.transcript_file)[1][1:]
            if (auto_edit_transcript == 'True') and (file_ext == 'html'):
                self.launch_editor(self.transcript_file)


        except Exception as e:
            self.logn(t('err_options'), 'error')
            traceback_str = traceback.format_exc()
            self.logn(e, 'error', tb=traceback_str)
            return

        finally:
            # hide the stop button
            self.stop_button.pack_forget() # hide
            self.start_button.pack(padx=[20, 0], pady=[20,30], expand=False, fill='x', anchor='sw')

            # hide progress
            self.set_progress(0, 0)
            
    def button_start_event(self):
        wkr = Thread(target=self.transcription_worker)
        wkr.start()
        #while wkr.is_alive():
        #    self.update()
        #    time.sleep(0.1)
    
    # End main function Button Start        
    ################################################################################################

    def button_stop_event(self):
        if tk.messagebox.askyesno(title='noScribe', message=t('transcription_canceled')) == True:
            self.logn()
            self.logn(t('start_canceling'))
            self.update()
            self.cancel = True

    def on_closing(self):
        # (see: https://stackoverflow.com/questions/111155/how-do-i-handle-the-window-close-event-in-tkinter)
        #if messagebox.askokcancel("Quit", "Do you want to quit?"):
        try:
            # remember some settings for the next run
            config['last_language'] = self.option_menu_language.get()
            config['last_speaker'] = self.option_menu_speaker.get()
            config['last_whisper_model'] = self.option_menu_whisper_model.get()
            config['last_pause'] = self.option_menu_pause.get()
            config['last_overlapping'] = self.check_box_overlapping.get()
            config['last_timestamps'] = self.check_box_timestamps.get()
            config['last_disfluencies'] = self.check_box_disfluencies.get()

            save_config()
        finally:
            self.destroy()

if __name__ == "__main__":

    app = App()

    app.mainloop()
