#!/usr/bin/env python3
# Looper. This is test code that:
# on GPIO connected button press: starts a recording
# second press: stops listening and plays a loop of the recording
# third press: stops looping and returns to initial state

# from xml.dom.minidom import parseString
from gpiozero import Button
from signal import pause
import pyo
import os
# import shlex
# import subprocess
# import threading
# import asyncio

s = pyo.Server().boot()
s.start()
audio = pyo.Input()
loop_file = os.path.dirname(os.path.abspath(__file__))+'/myloop.wav'
# loop_play_command = shlex.split('play '+loop_file+' -t alsa repeat -')
times_clicked = 0

def loop_play_thread():
    pass
    
def looper_func():
    global times_clicked, rec, looper, audio, loop_file, loop_process
    if times_clicked == 0:
        print("Recording")
        rec = pyo.Record(audio, filename=loop_file, fileformat=0, sampletype=1).out()
    if times_clicked == 1:
        print("Looping")
        rec.stop()
        looper = pyo.SfPlayer(loop_file, loop=True).out()
        # update SfPlayer is fixed!!
        # invoking SOX aplay command via subprocess
        # loop_process = asyncio.create_subprocess_exec(loop_play_command)
        # loop_process = threading.Thread()
        # loop_process = subprocess.Popen(loop_play_command, shell=True, preexec_fn=os.setsid)
        # loop_process.wait()
    if times_clicked == 2:
        print("Waiting")
        looper.stop()
        # loop_process.kill()
    times_clicked = (times_clicked+1)%3
    print(times_clicked)

print('Ready to record!')
switch = Button(2)
switch.when_pressed = looper_func

pause()

