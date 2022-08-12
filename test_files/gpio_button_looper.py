# Looperr. This is test code that:
# on GPIO connected button press: starts a recording
# second press: stops listening and plays a loop of the recording
# third press: stops looping and returns to initial state
#!/usr/bin/env python3
from gpiozero import Button
from signal import pause
import pyo
import os

s = pyo.Server().boot()
s.start()
audio = pyo.Input()
file_name = os.path.dirname(os.path.abspath(__file__))+"/myloop.wav"
times_clicked = 0

def looper_func(key):
    global times_clicked, rec, looper, audio, file_name
    if times_clicked == 0:
        print("Recording")
        rec = pyo.Record(audio, filename=file_name, fileformat=0, sampletype=1).out()
    if times_clicked == 1:
        print("Looping")
        rec.stop()
        looper = pyo.SfPlayer(file_name, loop=True).out()
    if times_clicked == 2:
        print("Waiting")
        looper.stop()
    times_clicked = (times_clicked+1)%3
    print(times_clicked)

switch = Button(2)
switch.when_pressed = looper_func

pause()
