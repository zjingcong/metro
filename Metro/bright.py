#!/usr/bin/env python
# -*- coding: utf-8 -*-

__title__ = ''
__author__ = 'zjingcong'

from cocos.layer import *
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.director import director
from cocos.actions import *

from pyglet import image

import random

from audio import *


CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]
TREE_TIME = 8


class brightViewScene(Scene):
    class windowLayer(Layer):
        def __init__(self, images_path, interval):
            super(brightViewScene.windowLayer, self).__init__()
            self.w, self.h = director.get_window_size()

            self.images_path = images_path
            self.interval = interval

            self.sprite1 = self._get_anim_sprite()
            self.sprite1.scale = float(self.h) / self.sprite1.height    # sprite(1920, 720)
            self.sprite2 = self._get_anim_sprite()
            self.sprite2.scale = float(self.h) / self.sprite2.height
            self.sprite2.position = self.sprite2.width * 1.5, self.sprite2.height / 2

            self.add(self.sprite1)
            self.add(self.sprite2)
            self.action1(self.sprite1)
            self.action2(self.sprite2)

        def _get_anim_sprite(self):
            view_image_list = []
            direct_path = "{current_dir}/{path}".format(current_dir=CURRENT_DIR, path=self.images_path)
            for root, dirs, files in os.walk(direct_path):
                    for file in files:
                        if file.startswith('background_bright_'):
                            view_image_list.append(file)

            view_image_list.sort()
            conf = ConfigParser.ConfigParser()
            conf.read("config.conf")

            def _get_anim_images(image_name):
                anim_image = image.load("{current_dir}/{path}{name}".format(current_dir=CURRENT_DIR,
                                                                            path=conf.get("path", "SCENE_BRIGHT_IMAGE"),
                                                                            name=image_name))
                return anim_image
            anim_image_list = map(_get_anim_images, view_image_list)

            frame_list = [image.AnimationFrame(frame, self.interval) for frame in anim_image_list]
            action_images = image.Animation(frame_list)
            sprite = Sprite(action_images)

            return sprite

        def action1(self, sprite):
            sprite.position = sprite.width / 2, sprite.height / 2
            sprite.do(MoveBy((-sprite.width, 0), 10) + CallFuncS(self.action1))

        def action2(self, sprite):
            sprite.position = sprite.width * 1.5, sprite.height / 2
            sprite.do(MoveBy((-sprite.width, 0), 10) + CallFuncS(self.action2))

    class metroLayer(Layer):
        def __init__(self, metro_image_path):
            super(brightViewScene.metroLayer, self).__init__()
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
            super(brightViewScene.animLayer, self).__init__()
            self.w, self.h = director.get_window_size()
            frame_list = [image.AnimationFrame(frame, interval) for frame in animation_frames]
            action_images = image.Animation(frame_list)
            self.sprite = Sprite(action_images)
            self.sprite.scale = float(self.h) / self.sprite.height
            self.sprite.position = self.w / 2, self.h / 2
            self.add(self.sprite)

    class treeLayer(Layer):
        class treeSprite(Sprite):
            def __init__(self, images_path, level):
                self.images_path = images_path
                self.level = level

                self.image_dict = self._get_tree_image_dict()
                self.tree_image_path = self._get_tree_image()

                super(brightViewScene.treeLayer.treeSprite, self).__init__(self.tree_image_path)
                self.scale = 0.8
                self.w, self.h = director.get_window_size()
                self.position = self.w / 2, self.h / 2

            def _get_tree_image_dict(self):
                direct_path = "{current_dir}/{path}".format(current_dir=CURRENT_DIR, path=self.images_path)
                level_1_list = []
                level_2_list = []
                level_3_list = []
                for root, dirs, files in os.walk(direct_path):
                    for file in files:
                        if file.startswith('tree_level_1'):
                            level_1_list.append(file)
                        elif file.startswith('tree_level_2'):
                            level_2_list.append(file)
                        elif file.startswith('tree_level_3'):
                            level_3_list.append(file)

                image_dict = {1: level_1_list, 2: level_2_list, 3: level_3_list}

                return image_dict

            def _get_tree_image(self):
                tree_image = random.choice(self.image_dict[self.level])

                return tree_image

        def __init__(self, images_path, wave_data, interval, music_audio):
            self.images_path = images_path
            self.wave_data = wave_data
            self.interval = interval
            self.music_audio = music_audio
            self.num = 15

            super(brightViewScene.treeLayer, self).__init__()
            self.w, self.h = director.get_window_size()
            self.init_position = {1: (self.w + 150, self.h / 2 - 100),
                                  2: (self.w + 150, self.h / 2),
                                  3: (self.w + 150, self.h / 2)}

            self.sprite_dict = self._get_sprite_dict()
            self.music_audio.play()
            self.move_tree()

        def move_tree(self):
            def _tree(l, level):
                print "_tree level: ", level
                for index in l:
                    remain = index - (index / self.num) * self.num
                    tree = self.sprite_dict[level][remain]
                    tree.do(Delay(index * self.interval) + MoveBy((-1920, 0), TREE_TIME) + MoveBy((1920, 0), 0))

            level_1 = [i for i in xrange(len(self.wave_data)) if self.wave_data[i] == 1]
            level_2 = [i for i in xrange(len(self.wave_data)) if self.wave_data[i] == 2]
            level_3 = [i for i in xrange(len(self.wave_data)) if self.wave_data[i] == 3]

            print level_1
            print level_2
            print level_3

            _tree(level_1, 1)
            _tree(level_2, 2)
            _tree(level_3, 3)

        def _fresh_status(self):
            for level in self.sprite_dict:
                for sprite in self.sprite_dict[level]:
                    if sprite.position[0] <= self.init_position[level][0] - 1920:
                        sprite.position = self.init_position[level]

        def _get_sprite_dict(self):
            def _get_sprite_list(level):
                sprite_list = []
                num = self.num
                for i in xrange(num):
                    sprite = self.treeSprite(self.images_path, level)
                    sprite.position = self.init_position[level]
                    sprite_list.append(sprite)
                    self.add(sprite)

                return sprite_list

            sprite_dict = {3: _get_sprite_list(3), 2: _get_sprite_list(2), 1: _get_sprite_list(1)}

            return sprite_dict

    def __init__(self, wave, audio):
        self.wave_data = wave[0]
        self.wave_time = wave[1]

        self.music_audio = audio

        self.interval = float(self.wave_time) / len(self.wave_data)

        print "interval: ", self.interval

        super(brightViewScene, self).__init__()

        conf = ConfigParser.ConfigParser()
        conf.read("config.conf")
        self.image_path = conf.get("path", "SCENE_BRIGHT_IMAGE")
        pyglet.resource.path = [self.image_path]
        pyglet.resource.reindex()

        self.w, self.h = director.get_window_size()
        self.metro_image_path = "metro_bright.png"

        def _get_anim_images(image_name):
            anim_image = image.load("{current_dir}/{path}{name}".format(current_dir=CURRENT_DIR,
                                                                        path=conf.get("path", "SCENE_BRIGHT_IMAGE"),
                                                                        name=image_name))
            return anim_image

        path_list = ["hand_1_bright.png", "hand_2_bright.png", "fat_man_1_bright.png", "fat_man_2_bright.png",
                     "short_man_1_bright.png", "short_man_2_bright.png"]
        self.images = map(_get_anim_images, path_list)

        self.add(self.windowLayer(self.image_path, 10))

    def main(self):
        self.add(self.treeLayer(self.image_path, self.wave_data, self.interval, self.music_audio))
        self.add(self.metroLayer(self.metro_image_path))
        self.add(self.animLayer(0.5, self.images[0], self.images[1]))
        self.add(self.animLayer(0.5, self.images[2], self.images[3]))
        self.add(self.animLayer(0.5, self.images[4], self.images[5]))
