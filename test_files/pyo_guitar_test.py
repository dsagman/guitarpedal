#!/usr/bin/env python3
 
# Disto(input, drive=0.75, slope=0.5, mul=1, add=0)[source]
# Delay(input, delay=0.25, feedback=0, maxdelay=1, mul=1, add=0)
# SDelay(input, delay=0.25, maxdelay=1, mul=1, add=0)
# Waveguide(input, freq=100, dur=10, minfreq=20, mul=1, add=0)
# AllpassWG(input, freq=100, feed=0.95, detune=0.5, minfreq=20, mul=1, add=0)
# Freeverb(input, size=0.5, damp=0.5, bal=0.5, mul=1, add=0)
# WGVerb(input, feedback=0.5, cutoff=5000, bal=0.5, mul=1, add=0)
# Chorus(input, depth=1, feedback=0.25, bal=0.5, mul=1, add=0)
# Harmonizer(input, transpo=- 7.0, feedback=0, winsize=0.1, mul=1, add=0)
# FreqShift(input, shift=100, mul=1, add=0)
# STRev(input, inpos=0.5, revtime=1, cutoff=5000, bal=0.5, roomSize=1, firstRefGain=- 3, mul=1, add=0)
# SmoothDelay(input, delay=0.25, feedback=0, crossfade=0.05, maxdelay=1, mul=1, add=0)
# Clip(input, min=- 1.0, max=1.0, mul=1, add=0)
# Degrade(input, bitdepth=16, srscale=1.0, mul=1, add=0)
# Mirror(input, min=0.0, max=1.0, mul=1, add=0)
# Compress(input, thresh=- 20, ratio=2, risetime=0.01, falltime=0.1, lookahead=5.0, knee=0, outputAmp=False, mul=1, add=0)
# Gate(input, thresh=- 70, risetime=0.01, falltime=0.05, lookahead=5.0, outputAmp=False, mul=1, add=0)
# Expand(input, downthresh=- 40, upthresh=- 10, ratio=2, risetime=0.01, falltime=0.1, lookahead=5.0, outputAmp=False, mul=1, add=0)


import pyo


s = pyo.Server(duplex=1, nchnls=1).boot().start()
#sine = pyo.Sine(freq=[400,800], mul=0.001).out()
a = pyo.Input(chnl=0, mul=1)
reverb = pyo.Freeverb(a, size=0.9, mul=1).out()






