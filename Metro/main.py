#!/usr/bin/env python
# -*- coding: utf-8 -*-

__title__ = ''
__author__ = 'zjingcong'

from black import *
from bright import *
import waveform

from cocos.scenes.transitions import *
from cocos.director import director
from pyglet.window import key

import ConfigParser
import logging
import os

CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]


def init():
    conf = ConfigParser.ConfigParser()
    conf.read("config.conf")
    pyglet.resource.path = [conf.get("path", "SCENE_BLACK_IMAGE")]
    pyglet.resource.reindex()

    global enter_path, music_path

    enter_path = "enter.png"
    music_path = "{current_dir}/{path}{name}".format(current_dir=CURRENT_DIR,
                                                     path=conf.get("music", "MUSIC"),
                                                     name="Kung Fu Fighting.wav")

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='Metro.log',
                        filemode='w')

    window_l = int(conf.get("window", "WINDOW_L"))
    window_h = int(conf.get("window", "WINDOW_H"))

    director.init(window_l, window_h)


class controlLayer(Layer):
    is_event_handler = True     #: enable pyglet's events

    def __init__(self, control_enter):
        super(controlLayer, self).__init__()
        self.w, self.h = director.get_window_size()
        self.sprite = Sprite(control_enter)
        self.sprite.scale = float(self.h) / self.sprite.height
        self.sprite.position = self.w / 2, self.h / 2
        self.sprite.opacity = 0
        self.add(self.sprite)
        self.sprite.do(Delay(23) + FadeIn(3))

    def on_key_press(self, k, m):
        global control_p

        if k == key.ENTER:
            director.replace(SplitRowsTransition(control_list[control_p + 1], 1))
            metro_audio.set_volume(0.2)
            main_scene.remove(black_scene)
            bright_scene.main()

            return True

if __name__ == '__main__':
    init()

    control = controlLayer(enter_path)

    metro_audio = metroAudio()
    music_audio = musicAudio()

    main_scene = Scene()
    black_scene = blackViewScene()
    black_scene.add(control)
    main_scene.add(black_scene)
    wave = waveform.main(music_path)    # wave(wave data, music length)
    bright_scene = brightViewScene(wave, music_audio)

    control_p = 0
    control_list = [main_scene, bright_scene]

    metro_audio.play(loops=-1)

    director.run(black_scene)
