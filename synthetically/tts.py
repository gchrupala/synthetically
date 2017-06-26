import requests
import time
from gtts import gTTS
import StringIO
import scipy.io.wavfile as wav
import pydub
import logging
import hashlib
import os
from itertools import izip

def encode(s):
    return hashlib.md5(s).hexdigest()

def speak(words):
    f = StringIO.StringIO()
    gTTS(text=words, lang='en-us').write_to_fp(f)
    return f.getvalue()

def decodemp3(s):
    seg = from_mp3(s)
    io = StringIO.StringIO()
    seg.export(io, format='wav')
    return io.getvalue()

def from_mp3(s):
    return pydub.AudioSegment.from_mp3(StringIO.StringIO(s))

def synthesize(text, attempt=1):
    logging.info("Synthesizing {}".format(text))
    try:
        return decodemp3(speak(text))
    except requests.exceptions.HTTPError:
        if attempt > 10:
            raise RuntimeError("HTTPError: giving up after 10 attempts")
        else:
            logging.info("HTTPError on attempt {}, waiting for 5 sec".format(attempt))
            time.sleep(5)
            return synthesize(text,  attempt=attempt+1)

def save_audio(texts, audios, audio_dir):
    logging.info("Storing wav files")
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    for text, audio in izip(texts, audios):
        logging.info("Storing audio for {}".format(text))

        path = encode(text)
        with open("{}/{}.wav".format(audio_dir, path), 'w') as out:
            out.write(audio)
