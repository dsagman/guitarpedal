#!/usr/bin/env python3
import sys
sys.settrace
import pyo
from signal import pause

s = pyo.Server().boot()
s.start()

looper = pyo.SfPlayer('/home/pi/guitar_audio/test_files/myloop.wav', loop=True)
looper.out()
pause()
