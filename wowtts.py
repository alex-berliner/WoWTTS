from gtts import gTTS
from playsound import playsound
import json
import multiprocessing
import os
import subprocess
import threading
import sys

def change_to_executable_dir():
    if getattr(sys, 'frozen', False):
        # Executable running in PyInstaller bundle
        executable_dir = os.path.dirname(sys.executable)
    else:
        # Executable running in regular Python environment
        executable_dir = os.path.dirname(os.path.abspath(__file__))

    os.chdir(executable_dir)

def read_output(proc):
    for line in iter(proc.stdout.readline, b''):
        data = json.loads(line.decode('utf-8'))
        if "u" in data and "qtts" in data["u"] and len(data["u"]["qtts"]) > 0:
            qd = ""
            for k in data["u"]["qtts"]:
                qd += data["u"]["qtts"][k]
            print(f"Processing: {qd}")
            tts = gTTS(qd, 'com')
            tts.save("out.mp3")
            print("Playing")
            p = multiprocessing.Process(target=playsound, args=("out.mp3",))
            p.start()

if __name__ == '__main__':
    change_to_executable_dir()
    proc = subprocess.Popen(['bin\parser.exe'], stdout=subprocess.PIPE)
    t = threading.Thread(target=read_output, args=(proc,))
    t.start()
