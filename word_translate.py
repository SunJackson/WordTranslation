#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from Xlib import X, display
from Xlib.ext import record
from Xlib.protocol import rq
import notify2
from translate import google_translate

record_dpy = display.Display()
# Create a recording context; we only want key and mouse events
ctx = record_dpy.record_create_context(
    0,
    [record.AllClients],
    [{
        'core_requests': (0, 0),
        'core_replies': (0, 0),
        'ext_requests': (0, 0, 0, 0),
        'ext_replies': (0, 0, 0, 0),
        'delivered_events': (0, 0),
        'device_events': (X.KeyPress, X.MotionNotify),
        'errors': (0, 0),
        'client_started': False,
        'client_died': False,
    }])

pre_word = ""  # 上次翻译的词语

def get_translate_words(pre_word):
    trans = google_translate()
    result = trans.translate(pre_word)
    return result


def viewTranslate():
    global pre_word

    result = get_translate_words(pre_word)
    notify2.init("AutoTranslate")
    bubble = notify2.Notification('谷歌翻译', result)
    bubble.show()



def record_callback(reply):
    global pre_word
    if reply.category != record.FromServer:
        return
    if reply.client_swapped:
        return
    if not len(reply.data) or reply.data[0] < 2:  # not an event
        return
    data = reply.data
    while len(data):
        event, data = rq.EventField(None).parse_binary_value(data, record_dpy.display, None, None)
        if event.type == X.ButtonRelease:
            pipe = os.popen("xclip -o")
            text = pipe.read()
            pipe.readlines()  # 清空管道剩余部分
            pipe.close()
            text = text.strip('\r\n\x00').lower().strip()
            if pre_word != text and text != "":
                pre_word = text
                viewTranslate()




def gettext():
    os.system("xclip -f /dev/null")  # 清空剪切板
    record_dpy.record_enable_context(ctx, record_callback)
    record_dpy.record_free_context(ctx)



def main():
    gettext()


if __name__ == '__main__':
    main()
