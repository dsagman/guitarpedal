#!/usr/bin/env python
# encoding: utf-8
from pyo import *
from random import uniform

class Synth:
    def __init__(self, transpo=1):
        self.transpo = Sig(transpo)
        self.note = Notein(poly=8, scale=1, first=0, last=127)
        self.pit = self.note['pitch'] * self.transpo
        self.amp = MidiAdsr(self.note['velocity'], attack=0.001,
                            decay=.1, sustain=.7, release=1, mul=.3)

        self.osc1 = LFO(freq=self.pit, sharp=0.25, mul=self.amp).mix(1)
        self.osc2 = LFO(freq=self.pit*0.997, sharp=0.25, mul=self.amp).mix(1)
        self.osc3 = LFO(freq=self.pit*1.004, sharp=0.25, mul=self.amp).mix(1)
        self.osc4 = LFO(freq=self.pit*1.009, sharp=0.25, mul=self.amp).mix(1)

        # Mix stereo (osc1 et osc3 a gauche, osc2 et osc4 a droite)
        self.mix = Mix([self.osc1+self.osc3, self.osc2+self.osc4], voices=2)

        # Distortion avec LFO sur le drive
        self.lfo = Sine(freq=uniform(.2,.4), mul=0.45, add=0.5)
        self.disto = Disto(self.mix, drive=self.lfo, slope=0.95, mul=.2)

    def out(self):
        self.disto.out()
        return self

    def sig(self):
        return self.disto

idev = pm_get_default_input()
s = Server()
s.setMidiInputDevice(idev)
s.boot()

# roue de modulation = amplitude du vibrato
ctl = Midictl(1, minscale=0, maxscale=.2)
bend = Bendin(brange=2, scale=1) # Pitch bend
lf = Sine(freq=5, mul=ctl, add=1) # Vibrato

a1 = Synth(lf * bend)
comp = Compress(a1.sig(), thresh=-20, ratio=6)
rev = WGVerb(comp, feedback=.8, cutoff=3500, bal=.3).out()

s.gui(locals())
