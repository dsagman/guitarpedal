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

debug = True
leds_on = False

from gpiozero import MCP3008
if leds_on:
    import LEDBoard
import pyo
import time
import sys

sys.setswitchinterval(1)                           # reduce interpreter thread checking interval 
pot_poll_time = 0.5

def pyo_callback():
    global pots, debug, leds, numlines             # global variables
    global delay, distort, reverb, chorus, clipped # effects   
    if debug:
        for n in range(numlines):
            print('Pot ', n, ' set at: ', pots[n].value)
        print(f'\033[{numlines}F', end='')
    if leds_on:
        leds.value = [pots[n].value for n in range(len(leds))]
    reverb.size = pots[0].value
    distort.drive = pots[1].value**0.05
    clipped.max = pots[2].value
    clipped.min = -pots[2].value
    chorus.depth = pots[3].value*2 # bit shift?


s = pyo.Server(nchnls=1).boot().start()
a = pyo.Input(chnl=0)
den = pyo.Denorm(a)
# den = a
delay = pyo.Delay(den)
reverb = pyo.Freeverb(den)
distort = pyo.Disto(den)
chorus = pyo.Chorus(den)
clipped = pyo.Clip(den)
#out = pyo.Mix([reverb, distort, chorus, clipped]).out() # would it be better to use pyo.Selector?
out = pyo.Selector(inputs=[reverb, distort], voice=0.5).out(chnl=0)

numlines = 8
if leds_on:
    leds = LEDBoard(5, pwm=True)
pots = [MCP3008(channel=n) for n in range(numlines)]     
p = pyo.Pattern(pyo_callback, time=pot_poll_time)
p.play()

# ascope = pyo.Scope([a,out],gain=500)
#out.ctrl()
#s.gui()

#samples = 0
#start = time.time()
#try:
#    print('\033c\033[?25l')  # clear the terminal screen and hide cursor
#    while True:
#        samples += 1
#        for n in range(numlines):
#            vals[n] = pots[n]
#            print('Pot ', n, ' set at: ', vals[n])
#        
#        print(f'\033[{numlines}F', end='')
#                     
#        delay.delay = vals[0][-1]*2

#except KeyboardInterrupt:
#    end = time.time()
#    print('\n\n\n\n\n\n\n\n\033c')  # clear the terminal screen 
#    print(f'{samples} samples gathered in {end-start:5.2f} seconds.')
#    print(f'{samples/(end-start):5.2f} samples per second.')
#    print('\033[?25h') # turn cursor back on
#    exit()




