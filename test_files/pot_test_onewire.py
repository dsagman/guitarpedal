import RPi.GPIO as GPIO
import time
from icecream import ic

GPIO.setmode(GPIO.BCM)

pin = 17

while True:
    # discharge
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)
    time.sleep(0.2)
    
    #charge
    GPIO.setup(pin, GPIO.IN)
    count = 0
    while not GPIO.input(pin):
        count = count + 1
    print(count)
    time.sleep(0.2)