#!/usr/bin/env python
# -*- coding: utf-8 -*-

__title__ = ''
__author__ = 'zjingcong'
__mtime__ = '2016/1/25'

import wave
import numpy as np

import ConfigParser
import logging
import os

SAMPLE_INTERVAL = 100
CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]


def get_waveform(music_path):
    music_file = wave.open(music_path, "rb")
    # (nchannels, sampwidth, framerate, nframes, comptype, compname)
    params = music_file.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]

    str_data = music_file.readframes(nframes)
    music_file.close()

    wave_data = np.fromstring(str_data, dtype=np.short)
    wave_data.shape = -1, 2
    wave_data = wave_data.T[0]
    l = int(len(wave_data) / 100)
    wave_data = map(int, wave_data)[0: l]
    time_list = list(np.arange(0, nframes) * (1.0 / framerate))
    m_time = time_list[len(time_list) - 1]      # the length of music: s

    return wave_data, m_time


def pcm(raw_data):
    wave_max = max(raw_data)
    wave_min = min(raw_data)

    delta = int((wave_max - wave_min) / 3)

    def _pcm(data):
        if (data >= wave_min) and (data < wave_min + delta):
            return 1
        elif (data >= wave_min + delta) and (data < wave_min + 2 * delta):
            return 2
        else:
            return 3

    pcm_data = map(_pcm, raw_data)

    return pcm_data


def sample(sample_interval, raw_data):
    sample_data = [raw_data[i * sample_interval] for i in xrange(len(raw_data) / sample_interval)]

    return sample_data


def main(music_path):
    wave_data, time = get_waveform(music_path)
    sample_data = sample(SAMPLE_INTERVAL, wave_data)
    pcm_data = pcm(sample_data)

    return pcm_data, time
