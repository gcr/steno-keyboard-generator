#!/usr/bin/env python2
# -*- coding: utf-8

from flask import Flask, make_response
from cStringIO import StringIO
from keyboard import draw_keyboard_to_png
from werkzeug.contrib.cache import FileSystemCache

app = Flask(__name__)

cache = FileSystemCache("./cache",
                        threshold=1024*8
                        default_timeout=6000)

def keys_key(pressed_keys,small):
    return "_".join(sorted(pressed_keys)) + ("_small" if small else "")

def get_board(pressed_keys, small,timeout=6000):
    k = keys_key(pressed_keys,small)
    if cache.get(k) == None:
        buf = StringIO()
        draw_keyboard_to_png(pressed_keys, buf, 0.5 if small else 1)
        cache.set(k,buf.getvalue(),timeout)
        return buf.getvalue()
    return cache.get(k)


VALID_KEYS = set(["S-","T-","P-","H","K","W","R-","A","O","*","E","U","F","-R","-P","B","G","L","G","-S","-T","D","Z"])

@app.route('/')
def show_page():
    return "Hello world"

@app.route('/board.png')
@app.route('/board_<keys>.png')
def keyboard(keys=""):
    pressed_keys = keys.upper().split("_")
    small = "SMALL" in pressed_keys
    pressed_keys = [k for k in pressed_keys if k in VALID_KEYS]
    res = make_response(
        get_board(pressed_keys, small,
                  timeout=(60*60*24*365
                           if len(pressed_keys)<2 else 3600)))
    res.headers['Content-type'] = 'image/png'
    return res

if __name__ == '__main__':
    app.run(debug=True)
