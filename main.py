import webbrowser
import json
import sys
import os
import random
import pyautogui as pag
import subprocess
import threading
from vosk import Model, KaldiRecognizer
import pyaudio, json
from flask import Flask, request, render_template
import webview

app = Flask(__name__)
window = webview.create_window('Midori', app)

try:
    model = Model('model_small') 
    rec = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16, 
        channels=1, 
        rate=16000, 
        input=True, 
        frames_per_buffer=44100
    )
    stream.start_stream()
except OSError:
    print("Не обнаружены аудио выходы, проверте свое устройство и повторите попытку.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/voice-assistant', methods=['POST'])
def process_speech():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data) and len(data) > 0:
            data = json.loads(rec.Result())["text"]
            
            if 'мидори' in data:
                    text = data.replace('мидори', '').strip()
                    commands(text)


def commands(text):
    # browser
    if text == 'открой браузер' or text == 'запусти браузер':
        webbrowser.open('https://google.com/')
    # how are you
    elif text == 'как дела':
        print('У меня все хорошо!')
    # buy
    elif text == 'пока':
        quit()
    # hello
    elif text == 'привет': 
        hi_list = ['Привет', 'Приветик', 'Добрый день']
        hi_random = random.choice(hi_list)
        print(hi_random)
    # explorer
    elif text == 'открой проводник' or text == 'запусти проводник':
        os.startfile(r'C:\Windows\explorer.exe')
    # task manager
    elif text == 'открой диспетчер задач' or text == 'запусти диспетчер задач':
        os.system('taskmgr')
    # youtube
    elif text == 'открой ютуб' or text == 'запусти ютуб':
        webbrowser.open('https://youtube.com/')
    # terminal
    elif text == 'открой терминал' or text == 'запусти терминал':
        os.system('cmd')
    # off
    elif text == 'выключи компьютер':
        os.system('shutdown -s')
    # trash
    elif text == 'очисти корзину' or text == 'освободи корзину':
        os.system(r'rd /s /q %systemdrive%\$Recycle.bin')
    # screenshot
    elif text == 'сделай скриншот' or text == 'сделай снимок экрана':
        pag.keyDown('win')
        pag.press('prtsc')
        pag.keyUp('win')
    # create folder
    elif text == 'создай папку' or text == 'создай новую папку':
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') # Получаем путь до рабочего стола

        name_folder = "New Folder"
        number_folder = 0
        folder_exist = False

        # Проверяем есть ли папка с таким именем
        while not folder_exist:
            folder_path = os.path.join(desktop, name_folder)
            if os.path.isdir(folder_path):
                number_folder += 1
                name_folder = f"New Folder{number_folder}"
            else:
                folder_exist = True
                os.mkdir(folder_path)
                print("Папка создана")
        return

    else:
        print("Простите, Я не понимаю вас.")

speech_thread = threading.Thread(target=process_speech)
speech_thread.daemon = True
speech_thread.start()

if __name__ == "__main__":
    webview.start()