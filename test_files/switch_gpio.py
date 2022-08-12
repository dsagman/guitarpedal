#!/usr/bin/env python3
from gpiozero import Button
from signal import pause

def say_hello():
    print("Hello!")


switch = Button(2)
switch.when_pressed = say_hello

pause()