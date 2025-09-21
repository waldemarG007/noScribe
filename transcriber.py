# transcriber.py

import sys
import os
import platform
import yaml
import appdirs
from subprocess import Popen, PIPE, STDOUT
if platform.system() == 'Windows':
    from subprocess import STARTUPINFO, STARTF_USESHOWWINDOW
from ctranslate2 import get_cuda_device_count
import torch
import re
if platform.system() == "Darwin": # = MAC
    from subprocess import check_output
    if platform.machine() == "x86_64":
        os.environ['KMP_DUPLICATE_LIB_OK']='True'
from faster_whisper.audio import decode_audio
from faster_whisper.vad import VadOptions, get_speech_timestamps
import AdvancedHTMLParser
import html
from tempfile import TemporaryDirectory
import datetime
from pathlib import Path
if platform.system() in ("Darwin", "Linux"):
    import shlex
if platform.system() == 'Windows':
    try:
        import cpufeature
    except ImportError:
        pass
import logging
import gc
import traceback

logging.basicConfig()
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

app_dir = os.path.abspath(os.path.dirname(__file__))

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
    "Auto": "auto", "Multilingual": "multilingual", "Afrikaans": "af", "Arabic": "ar", "Armenian": "hy", "Azerbaijani": "az", "Belarusian": "be", "Bosnian": "bs", "Bulgarian": "bg", "Catalan": "ca", "Chinese": "zh", "Croatian": "hr", "Czech": "cs", "Danish": "da", "Dutch": "nl", "English": "en", "Estonian": "et", "Finnish": "fi", "French": "fr", "Galician": "gl", "German": "de", "Greek": "el", "Hebrew": "he", "Hindi": "hi", "Hungarian": "hu", "Icelandic": "is", "Indonesian": "id", "Italian": "it", "Japanese": "ja", "Kannada": "kn", "Kazakh": "kk", "Korean": "ko", "Latvian": "lv", "Lithuanian": "lt", "Macedonian": "mk", "Malay": "ms", "Marathi": "mr", "Maori": "mi", "Nepali": "ne", "Norwegian": "no", "Persian": "fa", "Polish": "pl", "Portuguese": "pt", "Romanian": "ro", "Russian": "ru", "Serbian": "sr", "Slovak": "sk", "Slovenian": "sl", "Spanish": "es", "Swahili": "sw", "Swedish": "sv", "Tagalog": "tl", "Tamil": "ta", "Thai": "th", "Turkish": "tr", "Ukrainian": "uk", "Urdu": "ur", "Vietnamese": "vi", "Welsh": "cy",
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
            config = {}
except:
    config = {}

def get_config(key: str, default):
    if key not in config:
        config[key] = default
    return config[key]

# determine optimal number of threads for faster-whisper (depending on cpu cores)
if platform.system() == 'Windows':
    try:
        number_threads = get_config('threads', cpufeature.CPUFeature["num_physical_cores"])
    except:
        number_threads = get_config('threads', 4)
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

# Helper functions
def millisec(timeStr: str) -> int:
    try:
        h, m, s = timeStr.split(':')
        return (int(h) * 3600 + int(m) * 60 + int(s)) * 1000
    except:
        raise Exception(f'Invalid time string: {timeStr}')

def ms_to_str(milliseconds: float, include_ms=False):
    seconds, milliseconds = divmod(milliseconds,1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    formatted = f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'
    if include_ms:
        formatted += f'.{int(milliseconds):03d}'
    return formatted

def html_node_to_text(node: AdvancedHTMLParser.AdvancedTag) -> str:
    if AdvancedHTMLParser.isTextNode(node):
        return html.unescape(node.text)
    elif AdvancedHTMLParser.isTagNode(node):
        text_parts = []
        for child in node.childNodes:
            text = html_node_to_text(child)
            if text:
                text_parts.append(text)
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

def vtt_escape(txt: str) -> str:
    txt = html.escape(txt)
    while txt.find('\n\n') > -1:
        txt = txt.replace('\n\n', '\n')
    return txt

def ms_to_webvtt(milliseconds) -> str:
    hours, milliseconds = divmod(milliseconds, 3600000)
    minutes, milliseconds = divmod(milliseconds, 60000)
    seconds, milliseconds = divmod(milliseconds, 1000)
    return "{:02d}:{:02d}:{:02d}.{:03d}".format(int(hours), int(minutes), int(seconds), int(milliseconds))

def html_to_webvtt(parser: AdvancedHTMLParser.AdvancedHTMLParser, media_path: str):
    vtt = 'WEBVTT '
    paragraphs = parser.getElementsByTagName('p')
    vtt += vtt_escape(paragraphs[0].textContent) + '\n\n'
    vtt += vtt_escape('NOTE\n' + html_node_to_text(paragraphs[1])) + '\n\n'
    vtt += f'NOTE media: {media_path}\n\n'
    segments = parser.getElementsByTagName('a')
    for i, segment in enumerate(segments):
        name = segment.attributes.get('name')
        if name:
            name_elems = name.split('_', 4)
            if len(name_elems) > 1 and name_elems[0] == 'ts':
                start = ms_to_webvtt(int(name_elems[1]))
                end = ms_to_webvtt(int(name_elems[2]))
                spkr = name_elems[3]
                txt = vtt_escape(html_node_to_text(segment))
                vtt += f'{i+1}\n{start} --> {end}\n<v {spkr}>{txt.lstrip()}\n\n'
    return vtt

def get_whisper_models():
    whisper_model_paths = {}
    user_models_dir = os.path.join(config_dir, 'whisper_models')
    def collect_models(dir):
        if not os.path.isdir(dir):
            return
        for entry in os.listdir(dir):
            entry_path = os.path.join(dir, entry)
            if os.path.isdir(entry_path):
                if entry in whisper_model_paths:
                    print(f'Ignored double name for whisper model: "{entry}"')
                else:
                    whisper_model_paths[entry]=entry_path
    collect_models(os.path.join(app_dir, 'models'))
    collect_models(user_models_dir)
    return whisper_model_paths


# Main function
def run_transcription(
    audio_file: str,
    transcript_file: str,
    language_name: str,
    whisper_model_name: str,
    speaker_detection: str,
    start_time: str = '00:00:00',
    stop_time: str = '',
    overlapping: bool = True,
    timestamps: bool = False,
    disfluencies: bool = True,
    pause_option: str = '1sec+',
    log_callback=print
):
    proc_start_time = datetime.datetime.now()
    tmpdir = TemporaryDirectory(prefix='noScribe-')
    tmp_audio_file = os.path.join(tmpdir.name, 'tmp_audio.wav')

    try:
        if not audio_file:
            raise ValueError("Audio file not provided.")
        if not transcript_file:
            raise ValueError("Transcript file not provided.")

        my_transcript_file = transcript_file
        file_ext = os.path.splitext(my_transcript_file)[1][1:]

        # options
        whisper_beam_size = get_config('whisper_beam_size', 1)
        whisper_temperature = get_config('whisper_temperature', 0.0)
        whisper_compute_type = get_config('whisper_compute_type', 'default')
        timestamp_interval = get_config('timestamp_interval', 60_000)
        timestamp_color = get_config('timestamp_color', '#78909C')

        start = millisec(start_time) if start_time and start_time != '00:00:00' else 0
        stop = millisec(stop_time) if stop_time else 0

        whisper_model_paths = get_whisper_models()
        if whisper_model_name in whisper_model_paths:
            whisper_model = whisper_model_paths[whisper_model_name]
        else:
            raise FileNotFoundError(f"The whisper model '{whisper_model_name}' does not exist.")

        pause = ['none', '1sec+', '2sec+', '3sec+'].index(pause_option)
        pause_marker = get_config('pause_seconds_marker', '.')

        if file_ext == 'vtt' and (pause > 0 or overlapping or timestamps):
            log_callback("VTT output does not support pause, overlapping, or timestamp options. Disabling them.")
            pause = 0
            overlapping = False
            timestamps = False

        pyannote_xpu = 'cpu'
        whisper_xpu = 'cpu'
        if platform.system() in ('Windows', 'Linux'):
            cuda_available = torch.cuda.is_available() and get_cuda_device_count() > 0
            pyannote_xpu = get_config('pyannote_xpu', 'cuda' if cuda_available else 'cpu')
            whisper_xpu = get_config('whisper_xpu', 'cuda' if cuda_available else 'cpu')


        # 1) Convert Audio
        log_callback("Starting audio conversion...")
        end_pos_cmd = f'-to {stop_time}' if stop > 0 else ''
        arguments = f' -loglevel warning -hwaccel auto -y -ss {start_time} {end_pos_cmd} -i "{audio_file}" -ar 16000 -ac 1 -c:a pcm_s16le "{tmp_audio_file}"'

        ffmpeg_path = ""
        local_ffmpeg_paths = {
            'Windows': os.path.join(app_dir, 'ffmpeg.exe'),
            'Darwin': os.path.join(app_dir, 'ffmpeg'),
            'Linux': os.path.join(app_dir, 'ffmpeg-linux-x86_64')
        }
        local_ffmpeg = local_ffmpeg_paths.get(platform.system())

        if local_ffmpeg and os.path.exists(local_ffmpeg):
            ffmpeg_path = local_ffmpeg
        else:
            import shutil
            ffmpeg_path_in_path = shutil.which("ffmpeg")
            if ffmpeg_path_in_path:
                ffmpeg_path = ffmpeg_path_in_path
            else:
                raise FileNotFoundError("ffmpeg not found in app directory or system PATH.")

        ffmpeg_cmd = f'"{ffmpeg_path}"' + arguments

        if platform.system() in ("Darwin", "Linux"):
            ffmpeg_cmd = shlex.split(ffmpeg_cmd)

        startupinfo = None
        if platform.system() == 'Windows':
            startupinfo = STARTUPINFO()
            startupinfo.dwFlags |= STARTF_USESHOWWINDOW

        with Popen(ffmpeg_cmd, stdout=PIPE, stderr=STDOUT, bufsize=1, universal_newlines=True, encoding='utf-8', startupinfo=startupinfo) as ffmpeg_proc:
            for line in ffmpeg_proc.stdout:
                log_callback(f'ffmpeg: {line.strip()}')
        if ffmpeg_proc.returncode != 0:
            raise Exception(f'ffmpeg conversion failed with code {ffmpeg_proc.returncode}.')
        log_callback("Audio conversion finished.")

        # 2) Speaker identification
        diarization = []
        if speaker_detection != 'none':
            log_callback("Starting speaker identification...")
            diarize_output = os.path.join(tmpdir.name, 'diarize_out.yaml')

            python_executable = sys.executable or "python"
            diarize_script_path = os.path.join(app_dir, 'diarize.py')
            diarize_cmd = f'"{python_executable}" "{diarize_script_path}" {pyannote_xpu} "{tmp_audio_file}" "{diarize_output}" {speaker_detection}'

            diarize_env = os.environ.copy()

            if platform.system() in ('Darwin', 'Linux'):
                diarize_cmd = shlex.split(diarize_cmd)

            with Popen(diarize_cmd, stdout=PIPE, stderr=STDOUT, encoding='UTF-8', startupinfo=startupinfo, env=diarize_env) as pyannote_proc:
                for line in pyannote_proc.stdout:
                    log_callback(f'diarize: {line.strip()}')

            if pyannote_proc.returncode != 0:
                raise Exception(f"Speaker diarization failed with code {pyannote_proc.returncode}.")

            with open(diarize_output, 'r') as file:
                diarization = yaml.safe_load(file)
            log_callback("Speaker identification finished.")

        # Helper for diarization
        def find_speaker(diarization_data, transcript_start, transcript_end):
            spkr, max_overlap = '', 0.0
            for segment in diarization_data:
                overlap_start = max(segment["start"], transcript_start)
                overlap_end = min(segment["end"], transcript_end)
                overlap_duration = overlap_end - overlap_start
                if overlap_duration > max_overlap:
                    max_overlap = overlap_duration
                    spkr = f'S{segment["label"][8:]}'
            return spkr

        # 3) Transcribe with faster-whisper
        log_callback("Starting transcription...")
        from faster_whisper import WhisperModel

        model = WhisperModel(whisper_model, device=whisper_xpu, cpu_threads=number_threads, compute_type=whisper_compute_type, local_files_only=True)

        whisper_lang = languages.get(language_name)

        vad_threshold = float(get_config('voice_activity_detection_threshold', '0.5'))
        vad_parameters = VadOptions(min_silence_duration_ms=1000, threshold=vad_threshold, speech_pad_ms=400)

        if language_name == 'Auto':
            # Need to decode audio for language detection
            sampling_rate = model.feature_extractor.sampling_rate
            audio = decode_audio(tmp_audio_file, sampling_rate=sampling_rate)
            lang_info = model.detect_language(audio, vad_filter=True, vad_parameters=vad_parameters)
            if lang_info and lang_info[0]:
                 whisper_lang = lang_info[0][0]
                 log_callback(f"Detected language: {whisper_lang} with probability {lang_info[0][1]}")
            else:
                 whisper_lang = "en" # Default to english if detection fails
                 log_callback("Language detection failed, defaulting to English.")
            del audio
            gc.collect()


        prompt = ""
        if disfluencies:
            try:
                with open(os.path.join(app_dir, 'prompt.yml'), 'r', encoding='utf-8') as file:
                    prompts = yaml.safe_load(file)
                prompt = prompts.get(whisper_lang, '')
            except FileNotFoundError:
                log_callback("prompt.yml not found, continuing without prompt.")

        segments, info = model.transcribe(
            tmp_audio_file, language=whisper_lang, beam_size=5, word_timestamps=True,
            hotwords=prompt, vad_filter=True, vad_parameters=vad_parameters
        )

        # Prepare output document
        d = AdvancedHTMLParser.AdvancedHTMLParser()
        d.parseStr(default_html)
        main_body = d.createElement('div')
        d.body.appendChild(main_body)

        # Header
        p = d.createElement('p')
        p.setStyle('font-weight', '600')
        p.appendText(Path(audio_file).stem)
        main_body.appendChild(p)
        p = d.createElement('p')
        s = d.createElement('span')
        s.setStyle('color', '#909090'); s.setStyle('font-size', '0.8em')
        s.appendText(f"Transcribed with noScribe. Audio: {audio_file}")
        p.appendChild(s)
        main_body.appendChild(p)

        # Active paragraph for writing
        p = d.createElement('p')
        main_body.appendChild(p)

        speaker = ''
        log_callback("Processing segments...")
        full_text = ""
        for segment in segments:
            start_ms = round(segment.start * 1000.0)
            end_ms = round(segment.end * 1000.0)
            orig_audio_start = start + start_ms
            orig_audio_end = start + end_ms

            seg_text = segment.text
            seg_html = html.escape(seg_text)

            if speaker_detection != 'none':
                new_speaker = find_speaker(diarization, start_ms, end_ms)
                if speaker != new_speaker and new_speaker != '':
                    p = d.createElement('p')
                    main_body.appendChild(p)
                    speaker = new_speaker
                    if file_ext != 'vtt':
                        speaker_prefix = f'{speaker}:'
                        seg_text = f'{speaker_prefix}{seg_text}'
                        seg_html = f'{html.escape(speaker_prefix)}{seg_html}'
                        full_text += f"\n\n{speaker_prefix}"

            # Append segment text
            a_html = f'<a name="ts_{orig_audio_start}_{orig_audio_end}_{speaker}" >{seg_html}</a>'
            a = d.createElementFromHTML(a_html)
            p.appendChild(a)
            full_text += seg_text

        log_callback("\nTranscription finished.")

        # Save final output
        output_content = ""
        if file_ext == 'html':
            output_content = d.asHTML()
        elif file_ext == 'txt':
            output_content = html_to_text(d)
        elif file_ext == 'vtt':
            output_content = html_to_webvtt(d, audio_file)

        with open(my_transcript_file, 'w', encoding="utf-8") as f:
            f.write(output_content)

        proc_time = datetime.datetime.now() - proc_start_time
        log_callback(f'Transcription time: {proc_time}')
        return my_transcript_file

    except Exception as e:
        traceback_str = traceback.format_exc()
        log_callback(f"An error occurred: {e}\n{traceback_str}")
        raise
    finally:
        tmpdir.cleanup()
        log_callback("Process complete.")
