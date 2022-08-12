#!/usr/bin/env python3
from pyo import *

s = Server().boot()
s.start()

a = Input(chnl=0)

lfo = Sine(freq=[.2,.25], mul=.8, add=.5)
d = Disto(a, drive=lfo, slope=.8, mul=.15).out()
#d = Disto(a, drive=.8, slope=.5, mul=1.0).out()

scope_lfo = Scope(lfo)
scope = Scope(d)

s.gui()
