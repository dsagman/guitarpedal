#!/usr/bin/env python3
from pyo import *
import random

s = Server().boot()

env = Fader(0.005, 0.09, 0.1, mul=0.2)
jit = Randi(min=1.0, max=1.02, freq=3)
# Create a `Sig` object to hold the frequency value.
frq = Sig(100)
# Create the `Dummy` objects only once at initialization.
sig = RCOsc(freq=[frq+jit, frq-jit], mul=env).out()

def change():
    freq = midiToHz(random.randrange(60, 72, 2))
    # Only change the `value` attribute of the Sig object.
    frq.value = freq
    env.play()

pat = Pattern(change, time=0.125).play()

s.gui(locals())
