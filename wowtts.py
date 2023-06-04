from gtts import gTTS
from playsound import playsound
import json
import multiprocessing
import subprocess
import sys
import vlc
import time
import tempfile
import threading

def play_audio(file_path):
    player = vlc.MediaPlayer(file_path)
    player.play()

def read_output(proc):
    for line in iter(proc.stdout.readline, b''):
        data = json.loads(line.decode('utf-8'))
        if "u" in data and "qtts" in data["u"] and len(data["u"]["qtts"]) > 0:
            qd = ""
            for k in data["u"]["qtts"]:
                qd += data["u"]["qtts"][k]
            print(f"Processing: {qd}")
            tts = gTTS(qd, 'com')
            temp_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
            temp_filename = temp_file.name
            tts.save(temp_filename)
            play_audio(temp_filename)

if __name__ == '__main__':
    proc = subprocess.Popen(['bin\parser.exe'], stdout=subprocess.PIPE)
    t = threading.Thread(target=read_output, args=(proc,))
    t.start()
