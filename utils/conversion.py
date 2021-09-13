import subprocess as sp
import tempfile
import os
import speech_recognition as sr
import io
from gtts import gTTS
from data.languages import Languages
from utils import translation
from utils.ffmpeg_config import FfmpegConfig


def audio_to_text(file, lang_in):
    """конвертирование аудио в текст"""
    try:
        res = sr.Recognizer()
        with sr.AudioFile(io.BytesIO(file)) as source:
            audio = res.record(source)
        return res.recognize_google(audio, language=lang_in)

    except Exception as error:
        print(error)
        return


def convert(in_filename=None, in_bytes=None, ogg=False):
    """ конвертер аудио ogg -> wav и mp3 -> ogg """
    with tempfile.NamedTemporaryFile() as temp_out_file:
        temp_in_file = None
        if in_bytes:
            temp_in_file = tempfile.NamedTemporaryFile(delete=False)
            temp_in_file.write(in_bytes)
            in_filename = temp_in_file.name
            temp_in_file.close()

        if not in_filename:
            raise Exception('Не указаны входные данные')

        sp.Popen(FfmpegConfig().setup_command(in_filename, ogg), stdout=temp_out_file, stderr=sp.DEVNULL).wait()

        if temp_in_file:
            os.remove(in_filename)
        temp_out_file.seek(0)

        return temp_out_file.read()


def text_to_audio(message, text):
    """ конвертирование текста в аудио """
    lang_out = translation.base_lang(message, read=True)[1]
    if lang_out not in Languages.dict_not_text_audio:
        mp3_fp = io.BytesIO()
        gTTS(text=text, lang=lang_out.split(sep='-')[0], slow=False).write_to_fp(mp3_fp)
        return convert(in_bytes=mp3_fp.getvalue(), ogg=False)
    else:
        return False
