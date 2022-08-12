import RPi.GPIO as GPIO
import time
from icecream import ic

GPIO.setmode(GPIO.BCM)

pin1 = 25
pin2 = 24

while True:
    # discharge
#     GPIO.setup(pin2, GPIO.IN)
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.output(pin1, False)
    time.sleep(0.2)
    
    #charge
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.output(pin2, True)
    GPIO.setup(pin1, GPIO.IN)
    count = 0
    while not GPIO.input(pin1):
        count = count + 1
    print(count)
#     GPIO.output(pin2, False)
    time.sleep(0.2)