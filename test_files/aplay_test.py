#!/usr/bin/env python3
import os
import pyo
import time
import shlex
from signal import pause

import subprocess

s = pyo.Server().boot()
s.start()
a = pyo.Sine(freq=440, mul=0.01).out()

# audio = pyo.Input()
loop_file = os.path.dirname(os.path.abspath(__file__))+'/myloop.wav'
loop_play_command = shlex.split('play '+loop_file+' -t alsa repeat -')
print(loop_play_command)

process = subprocess.Popen(loop_play_command)
try:
    print('Running in process', process.pid)
    process.wait(timeout=2)
except subprocess.TimeoutExpired:
    print('Timed out - killing', process.pid)
    process.kill()
print("Done")


# os.system(f'play {loop_file} -t alsa repeat -')
# time.sleep(1)
# os.system('killall play')
# s = pyo.Server().boot()
# s.start()
# looper = pyo.SfPlayer('/home/pi/guitar_audio/test_files/M1F1-int32-AFsp.aif')
# looper.out()
