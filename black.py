#!/usr/bin/env python
# -*- coding: utf-8 -*-

__title__ = ''
__author__ = 'zjingcong'

import pyglet
from pyglet import image
from cocos.layer import Layer
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.director import director
from cocos.actions import *

import ConfigParser
import os

CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]


class blackScene(Scene):
    class windowLayer(Layer):
        def __init__(self, background_image):
            super(blackScene.windowLayer, self).__init__()
            self.w, self.h = director.get_window_size()

            self.sprite1 = Sprite(background_image)
            self.sprite1.scale = float(self.h) / self.sprite1.height    # sprite(1920, 720)
            self.sprite2 = Sprite(background_image)
            self.sprite2.scale = float(self.h) / self.sprite2.height
            self.sprite2.position = self.sprite2.width * 1.5, self.sprite2.height / 2

            self.add(self.sprite1)
            self.add(self.sprite2)
            self.action1(self.sprite1)
            self.action2(self.sprite2)

        def action1(self, sprite):
            sprite.position = sprite.width / 2, sprite.height / 2
            move = MoveBy((-120, -10), 0.5)
            for i in xrange(15):
                if float((i + 10)) / 2 == (i + 10) / 2:
                    delta_y = 10
                else:
                    delta_y = -10
                move += MoveBy((-120, delta_y), 0.5)
            move += CallFuncS(self.action1)
            sprite.do(move)

        def action2(self, sprite):
            sprite.position = sprite.width * 1.5, sprite.height / 2
            move = MoveBy((-120, -10), 0.5)
            for i in xrange(15):
                if float((i + 10)) / 2 == (i + 10) / 2:
                    delta_y = 10
                else:
                    delta_y = -10
                move += MoveBy((-120, delta_y), 0.5)
            move += CallFuncS(self.action2)
            sprite.do(move)

    class metroLayer(Layer):
        def __init__(self, metro_image):
            super(blackScene.metroLayer, self).__init__()
            self.w, self.h = director.get_window_size()
            self.sprite = Sprite(metro_image)
            self.sprite.scale = float(self.h) / self.sprite.height
            self.sprite.position = self.w / 2, self.h / 2
            self.add(self.sprite)

    class animLayer(Layer):
        def __init__(self, *animation_frames):
            super(blackScene.animLayer, self).__init__()
            self.w, self.h = director.get_window_size()
            hand_frame_list = [image.AnimationFrame(frame, 0.5) for frame in animation_frames]
            hand_action_images = image.Animation(hand_frame_list)
            self.sprite = Sprite(hand_action_images)
            self.sprite.scale = float(self.h) / self.sprite.height
            self.sprite.position = self.w / 2, self.h / 2
            self.add(self.sprite)

    def __init__(self):
        super(blackScene, self).__init__()

        conf = ConfigParser.ConfigParser()
        conf.read("config.conf")
        pyglet.resource.path = [conf.get("path", "SCENE_BLACK_IMAGE")]
        pyglet.resource.reindex()

        self.w, self.h = director.get_window_size()

        self.background_image = "background.png"
        self.metro_image = "metro_black.png"

        self.hand_1 = image.load("{current_dir}/{path}{name}".format(current_dir=CURRENT_DIR,
                                                                     path=conf.get("path", "SCENE_BLACK_IMAGE"),
                                                                     name="hand_1.png"))
        self.hand_2 = image.load("{current_dir}/{path}{name}".format(current_dir=CURRENT_DIR,
                                                                     path=conf.get("path", "SCENE_BLACK_IMAGE"),
                                                                     name="hand_2.png"))

        self.layout()

    def layout(self):
        self.add(self.windowLayer(self.background_image))
        self.add(self.metroLayer(self.metro_image))
        self.add(self.animLayer(self.hand_1, self.hand_2))
