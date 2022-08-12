#!/usr/bin/env python3
from gpiozero import PWMLED, MCP3008
import pyo
import time
from collections import deque
import threading
from icecream import ic

#def pyogui(pserver):
    #pserver.gui()

s = pyo.Server(audio="portaudio").boot().start()
a = pyo.Input(chnl=0).out()
delay = pyo.Delay(a).out()
harmony = pyo.Harmonizer(a).out()
chorus = pyo.Chorus(a).out()
fshift = pyo.FreqShift(a).out()
#pscope = pyo.Scope([a,delay], gain=1000)
#t = threading.Thread(target=pyogui,args=(s,))
#t.start()

smoothing = 100 
numlines = 8
pots = [MCP3008(channel=n) for n in range(numlines)]
vals = [deque(maxlen=smoothing) for n in range (numlines)]
smoothed = [None] * numlines
        
samples = 0
start = time.time()
try:
    print('\033c\033[?25l')  # clear the terminal screen and hide cursor
    while True:
        samples += 1
        for n in range(numlines):
            vals[n].appendleft(round(pots[n].value,5))
            smoothed[n] = sum(vals[n])/smoothing 
            print('Pot ', n, ' set at: ', smoothed[n])
        
        print(f'\033[{numlines}F', end='')
                     
        delay.delay = vals[0][-1]*2

except KeyboardInterrupt:
    end = time.time()
    print('\n\n\n\n\n\n\n\n\033c')  # clear the terminal screen 
    print(f'{samples} samples gathered in {end-start:5.2f} seconds.')
    print(f'{samples/(end-start):5.2f} samples per second.')
    print('\033[?25h') # turn cursor back on
    exit()



