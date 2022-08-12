import RPi.GPIO as GPIO
import time
import pyo
import random
from icecream import ic

GPIO.setmode(GPIO.BCM)

pin = 17
s = pyo.Server().boot()
s.start()
a = pyo.Input(chnl=0).out()
effect = .2
delay = pyo.Delay(a, delay=effect).out()
# for i in range(10000):
#     time.sleep(3)
#     delay.delay = random.random()*2
#     ic(delay.delay)

while True:
    # discharge
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)
    time.sleep(0.01)
    
    #charge
    GPIO.setup(pin, GPIO.IN)
    count = 0
    while not GPIO.input(pin):
        count = count + 1
    time.sleep(5)
    
    new_effect = min(count, 5000)/3000
    print(str(count).rjust(10)+" "+str(new_effect).rjust(15), end="\r")
    
    if new_effect != effect:
        delay.delay = new_effect
        effect = new_effect
        

    #lfo = pyo.Sine(freq=220, phase=0, mul=.3, add=.3)
    # delay = pyo.Delay(a, delay=.3, feedback=lfo, maxdelay=3).out()
    
    scope0 = pyo.Scope(a)
    scope = pyo.Scope(delay)
#     s.gui()
 
