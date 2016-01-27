#!/usr/bin/env python
# -*- coding: utf-8 -*-

__title__ = ''
__author__ = 'zjingcong'


import ConfigParser
import logging
import cocos
from cocos.director import director
from black import blackScene


def init():
    conf = ConfigParser.ConfigParser()
    conf.read("config.conf")

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='Metro.log',
                        filemode='w')

    window_l = int(conf.get("window", "WINDOW_L"))
    window_h = int(conf.get("window", "WINDOW_H"))

    return window_l, window_h


def main():
    window_l, window_h = init()
    director.init(window_l, window_h)
    main_scene = cocos.scene.Scene()

    black = blackScene()
    black.scale = 1.0
    main_scene.add(black)

    director.run(main_scene)

if __name__ == '__main__':
    main()
