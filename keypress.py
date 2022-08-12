# Working on a looper. This is test code that:
# on any keypress: starts a recording
# second keypress: stops listening and plays a loop of the recording
# third keypress: stops looping and waits

from pynput import keyboard
from signal import pause
import pyo
import os

s = pyo.Server(audio='jack').boot()
s.start()
home = os.path.dirname(os.path.abspath(__file__))
file_name = home+"/myloop.wav"


pyo_inp = pyo.Input()
times_clicked = 0

def on_press(key):
    global times_clicked, rec, looper, pyo_inp, file_name
    if times_clicked == 0:
        print("Recording")
        rec = pyo.Record(pyo_inp, filename=file_name, fileformat=0, sampletype=1).out()
    if times_clicked == 1:
        print("Looping")
        rec.stop()
        looper = pyo.SfPlayer(file_name, loop=True).out()
    if times_clicked == 2:
        print("Waiting")
        looper.stop()
    times_clicked = (times_clicked+1)%3
    # print(times_clicked)
    # print(key)

listener = keyboard.Listener(on_press=on_press)
listener.start()

pause()
