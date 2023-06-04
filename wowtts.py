from gtts import gTTS
import json
import subprocess
import sys
import vlc
import time
import tempfile
import threading
import version

current_player = None

def play_audio(file_path):
    global current_player

    if current_player is not None:
        current_player.stop()

    print("Playing")
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(file_path)
    player.set_media(media)
    player.play()

    current_player = player

def read_output(proc):
    for line in iter(proc.stdout.readline, b''):
        try:
            data = json.loads(line.decode('utf-8'))
        except:
            continue
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
    print("https://github.com/alex-berliner/WoWTTS")
    print(f"Version {version.VERSION}")
    proc = subprocess.Popen(['bin\parser.exe'], stdout=subprocess.PIPE)
    t = threading.Thread(target=read_output, args=(proc,))
    t.start()
