#!/usr/bin/env python3
# A guitar effects application for raspberry pi
import os
import shutil
from gpiozero import MCP3008, LEDBoard, LEDBarGraph, Button, LED
import signal, time, argparse
import pyo


ap = argparse.ArgumentParser(description='A guitar effects application for raspberry pi using pyo and a bunch of wires. There was some blood involved in the making.')
ap.add_argument('--debug', action='store_true', help='Turn on printing of potentiometer values')
ap.add_argument('--no_leds', action='store_false', help='Turn on LED funcionality')
ap.add_argument('--meter', action='store_true', help='Show the volume/amplitude meter')
ap.add_argument('--looptest', action='store_true', help='Print the status of the looper switch')
args = ap.parse_args()

debug = args.debug
leds_on = args.no_leds
meter = args.meter
looptest = args.looptest

numlines = 8
pot_leds = LEDBoard(4, 27, 13, 26, 23, 22, 12, 24, pwm=True)
vu_leds  = LEDBarGraph(14, 16, 25, 6, 5, 17)

pots = [MCP3008(channel=n) for n in range(numlines)]     
vals = [0] * numlines

def ctrl_c_signal_handler(sig_num, stack_frame):
    global samples, start_time, debug
    end_time = time.time()
    print('\n\n\n\n\n\n\n\n\n\nSo long and thanks for all the fish.\n')
    print(f'We had fun for \033[36m{end_time-start_time:,.2f}\033[0m seconds.')
    if debug:
        print(f'{samples/(end_time-start_time):5.2f} samples per second.')
    print('\033[?25h\033[30m') # turn cursor back on, reset color if changed
    exit()

def RMS_meter_callback(*args):
    global max_RMS, VU_factor, meter
    # set VU max to highest value, but back off highest value over time
    if args[0] > max_RMS:
        max_RMS = args[0]
        VU_factor = 20/max_RMS # number of VU bars is 20
    elif max_RMS > 0.05:  
        max_RMS -= 0.005
    if leds_on:
        vu_leds.value = min([1,args[0]*VU_factor/20])
    if meter:
        amp = int(args[0]*VU_factor)
        if amp < 11:
            print('\033[5G\033[32m'+'|'*amp+' '*20)
        elif amp < 17:
            print('\033[5G\033[32m'+'|'*10+'\033[33m'+'|'*(amp-10)+' '*10)
        else:
            print('\033[5G\033[32m'+'|'*10+'\033[33m'+'|'*6+'\033[31m'+'|'*(amp-16)+' '*5)
        print('\033[1F', end='')


def looper_func():
    global loop_button_clicked
    loop_button_clicked = 1+(loop_button_clicked%3)
    return
                  

max_RMS = 0
VU_factor = 1

# set up pyo input and effectgs
s = pyo.Server().boot()
s.start()
audio    = pyo.Input()
dry      = pyo.Input()

# wah effect
follow   = pyo.Follower(audio)
wahfq    = pyo.Scale(follow, outmin=300, outmax=20000)

delay    = pyo.SmoothDelay(audio, feedback=0.15)
reverb   = pyo.Freeverb(delay)
distort  = pyo.Disto(reverb)
eq       = pyo.MultiBand(distort, num=3, mul=[1,1,1])
wet      = pyo.Mix([eq])
wah      = pyo.ButBP(wet, freq=wahfq, q=30)
mix       = pyo.Mix([dry,wet,wah]).out()
amplitude = pyo.RMS(mix, function=RMS_meter_callback)


# looper stuff
cdir        = os.path.dirname(os.path.abspath(__file__))
silence     = cdir+'/silent.wav'
loop_file   = cdir+'/pedalloop.wav'
shutil.copy(silence,loop_file)
loop_button_clicked = 0
loop_button = Button(2)
loop_button.when_pressed = looper_func
loop_vol    = 0.3
looper      = pyo.SfPlayer(loop_file, loop=True, mul=loop_vol)
loop_led    = LED(15)
loop_led.off()


# use signal to wait for ctrl-c to exit
signal.signal(signal.SIGINT, ctrl_c_signal_handler)
if not debug:
    print('\033c\033[?25l\033[5G')  # clear the terminal screen, hide cursor, move to column 5
print('Pedal amp and effects running. Press Ctrl-C to stop.')
start_time = time.time()
samples = 0
if meter:
    print('\033[5G\033[35m'+'VU')
    print('\033[5G\033[32m'+'-'*10+'\033[33m'+'-'*6+'\033[31m'+'-'*4)    

recording = False
looping   = False
if looptest:
    print("Waiting")
while True:
    samples += debug
    if loop_button_clicked == 1 and not recording:
        if looptest:
            print("Recording")
        recording = True
        looping   = False
        looper.stop()
        loop_led.blink(on_time=0.3, off_time=0.3)
        loop_rec = pyo.Record(mix, filename=loop_file, fileformat=0, sampletype=1)
    if loop_button_clicked == 2 and recording:
        if looptest:
            print("Looping")
        recording = False
        looping   = True
        loop_rec.stop()
        loop_led.on()
        looper = pyo.SfPlayer(loop_file, loop=True, mul=loop_vol).out() #playback a little quieter than current volume
    if loop_button_clicked == 3 and looping:
        if looptest:
            print("Waiting")
        recording = False
        looping = False
        loop_led.off()
        looper.stop()

    #I wired all my pots backwards, so the "1.0-" below compensates for that
    #You can swap the outermost wire to the other outermost pin on the pot to the same effect
    new_vals = [1.0-int(pots[n].value*100)/100 for n in range(numlines)]
    for i, nv in enumerate(new_vals):
        if abs(vals[i]-nv) > 0.05:
            vals[i] = nv
    if debug:
        print()
        for n in range(numlines):
            print(f'Pot {n} set at: {vals[n]:.5f}     ')
        print(f'\033[{numlines+1}F', end='')
    if leds_on:
        pot_leds.value = [vals[n] for n in range(len(pot_leds))]
    dry.mul         = 1 - vals[0]
    wet.mul         = vals[0] 
    delay.delay     = vals[1]
    reverb.size     = vals[2]
    distort.drive   = vals[3]**0.05
    wah.mul         = vals[4]*30
    eq.mul          = [vals[5]*2, vals[6]*2, vals[7]*2]


# Available effects in the pyo module are:
#   Disto(input, drive=0.75, slope=0.5, mul=1, add=0)[source]
#   Delay(input, delay=0.25, feedback=0, maxdelay=1, mul=1, add=0)
#   SDelay(input, delay=0.25, maxdelay=1, mul=1, add=0)
#   Waveguide(input, freq=100, dur=10, minfreq=20, mul=1, add=0)
#   AllpassWG(input, freq=100, feed=0.95, detune=0.5, minfreq=20, mul=1, add=0)
#   Freeverb(input, size=0.5, damp=0.5, bal=0.5, mul=1, add=0)
#   WGVerb(input, feedback=0.5, cutoff=5000, bal=0.5, mul=1, add=0)
#   Chorus(input, depth=1, feedback=0.25, bal=0.5, mul=1, add=0)
#   Harmonizer(input, transpo=- 7.0, feedback=0, winsize=0.1, mul=1, add=0)
#   FreqShift(input, shift=100, mul=1, add=0)
#   STRev(input, inpos=0.5, revtime=1, cutoff=5000, bal=0.5, roomSize=1, firstRefGain=- 3, mul=1, add=0)
#   SmoothDelay(input, delay=0.25, feedback=0, crossfade=0.05, maxdelay=1, mul=1, add=0)
#   Clip(input, min=- 1.0, max=1.0, mul=1, add=0)
#   Degrade(input, bitdepth=16, srscale=1.0, mul=1, add=0)
#   Mirror(input, min=0.0, max=1.0, mul=1, add=0)
#   Compress(input, thresh=- 20, ratio=2, risetime=0.01, falltime=0.1, lookahead=5.0, knee=0, outputAmp=False, mul=1, add=0)
#   Gate(input, thresh=- 70, risetime=0.01, falltime=0.05, lookahead=5.0, outputAmp=False, mul=1, add=0)
#   Expand(input, downthresh=- 40, upthresh=- 10, ratio=2, risetime=0.01, falltime=0.1, lookahead=5.0, outputAmp=False, mul=1, add=0)
