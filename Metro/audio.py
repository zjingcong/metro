#!/usr/bin/env python
# -*- coding: utf-8 -*-

__title__ = ''
__author__ = 'zjingcong'

import cocos.audio.pygame.mixer as mixer
from cocos.audio.pygame.mixer import Sound

import ConfigParser
import os

CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]


class metroAudio(Sound):
    def __init__(self):
        mixer.init()

        conf = ConfigParser.ConfigParser()
        conf.read("config.conf")
        self.metro_sound_file = "{current_dir}/{path}{name}".format(current_dir=CURRENT_DIR,
                                                                    path=conf.get("path", "SCENE_BLACK_AUDIO"),
                                                                    name="metro.wav")
        super(metroAudio, self).__init__(self.metro_sound_file)


class musicAudio(Sound):
    def __init__(self):
        mixer.init()

        conf = ConfigParser.ConfigParser()
        conf.read("config.conf")
        self.music_path = "{current_dir}/{path}{name}".format(current_dir=CURRENT_DIR,
                                                              path=conf.get("music", "MUSIC"),
                                                              name="Kung Fu Fighting.wav")
        super(musicAudio, self).__init__(self.music_path)
