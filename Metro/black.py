#!/usr/bin/env python
# -*- coding: utf-8 -*-

__title__ = ''
__author__ = 'zjingcong'

from pyglet import image

from cocos.layer import *
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.director import director
from cocos.actions import *

import ConfigParser
import os

CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]


class blackViewScene(Scene):
    class windowLayer(Layer):
        def __init__(self, background_image_path):
            super(blackViewScene.windowLayer, self).__init__()
            self.w, self.h = director.get_window_size()

            self.sprite1 = Sprite(background_image_path)
            self.sprite1.scale = float(self.h) / self.sprite1.height    # sprite(1920, 720)
            self.sprite2 = Sprite(background_image_path)
            self.sprite2.scale = float(self.h) / self.sprite2.height
            self.sprite2.position = self.sprite2.width * 1.5, self.sprite2.height / 2

            self.add(self.sprite1)
            self.add(self.sprite2)
            self.action1(self.sprite1)
            self.action2(self.sprite2)

        def action1(self, sprite):
            sprite.position = sprite.width / 2, sprite.height / 2
            sprite.do(MoveBy((-sprite.width, 0), 10) + CallFuncS(self.action1))

        def action2(self, sprite):
            sprite.position = sprite.width * 1.5, sprite.height / 2
            sprite.do(MoveBy((-sprite.width, 0), 10) + CallFuncS(self.action2))

    class metroLayer(Layer):
        def __init__(self, metro_image_path):
            super(blackViewScene.metroLayer, self).__init__()
            self.w, self.h = director.get_window_size()
            self.sprite = Sprite(metro_image_path)
            self.sprite.scale = float(self.h) / self.sprite.height
            self.sprite.position = self.sprite.width / 2, self.sprite.height / 2
            self.add(self.sprite)
            self.action(self.sprite)

        def action(self, sprite):
            sprite.position = sprite.width / 2, sprite.height / 2
            move = MoveBy((2, -3), 0.5)
            for i in xrange(15):
                if float((i + 10)) / 2 == (i + 10) / 2:
                    delta_y = 3
                    delta_x = -2
                else:
                    delta_y = -3
                    delta_x = 2
                move += MoveBy((delta_x, delta_y), 0.5)
            move += CallFuncS(self.action)
            sprite.do(move)

    class animLayer(Layer):
        def __init__(self, interval, *animation_frames):
            super(blackViewScene.animLayer, self).__init__()
            self.w, self.h = director.get_window_size()
            frame_list = [image.AnimationFrame(frame, interval) for frame in animation_frames]
            action_images = image.Animation(frame_list)
            self.sprite = Sprite(action_images)
            self.sprite.scale = float(self.h) / self.sprite.height
            self.sprite.position = self.w / 2, self.h / 2
            self.add(self.sprite)

    class titleLayer(Layer):
        def __init__(self, title):
            super(blackViewScene.titleLayer, self).__init__()
            self.w, self.h = director.get_window_size()
            self.sprite = Sprite(title)
            self.sprite.scale = float(self.h) / self.sprite.height
            self.sprite.position = self.w / 2, self.h / 2
            self.sprite.opacity = 0
            self.add(self.sprite)
            self.sprite.do(Delay(8) + FadeIn(5) + Delay(5) + FadeOut(2))    # total: 20

    def __init__(self):
        super(blackViewScene, self).__init__()

        conf = ConfigParser.ConfigParser()
        conf.read("config.conf")
        pyglet.resource.path = [conf.get("path", "SCENE_BLACK_IMAGE")]
        pyglet.resource.reindex()

        self.w, self.h = director.get_window_size()

        self.background_image_path = "background.png"
        self.metro_image_path = "metro_black.png"
        self.title_path = "metro_title.png"

        def _get_anim_images(image_name):
            anim_image = image.load("{current_dir}/{path}{name}".format(current_dir=CURRENT_DIR,
                                                                        path=conf.get("path", "SCENE_BLACK_IMAGE"),
                                                                        name=image_name))
            return anim_image

        path_list = ["hand_1.png", "hand_2.png", "fat_man_1.png", "fat_man_2.png", "short_man_1.png", "short_man_2.png"]
        self.images = map(_get_anim_images, path_list)

        self.layout()

    def layout(self):
        self.add(self.windowLayer(self.background_image_path))
        self.add(self.metroLayer(self.metro_image_path))
        self.add(self.animLayer(0.5, self.images[0], self.images[1]))
        self.add(self.animLayer(0.5, self.images[2], self.images[3]))
        self.add(self.animLayer(0.5, self.images[4], self.images[5]))
        self.add(self.titleLayer(self.title_path))
