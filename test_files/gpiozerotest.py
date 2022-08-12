from gpiozero import LED
from signal import pause

red = LED(16)
blue = LED(12)
blue.on()

red.on()

pause()