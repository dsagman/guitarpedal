import pyo
from signal import pause
s = pyo.Server().boot().start()
a = pyo.Sine(mul=0.1).out()
pause()
