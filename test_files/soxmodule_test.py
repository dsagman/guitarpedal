#!/usr/bin/env python3
import os
import pyo
import time
import shlex
import sox

loop_file = os.path.dirname(os.path.abspath(__file__))+'/myloop.wav'
loop_play_command = shlex.split('play '+loop_file+' -t alsa repeat -')
print(loop_play_command)

sox.core.play(loop_play_command)



# os.system(f'play {loop_file} -t alsa repeat -')

