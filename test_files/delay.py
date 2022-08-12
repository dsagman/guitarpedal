import pyo

s = pyo.Server().boot()
s.start()

a = pyo.Input(chnl=0).out()


lfo = pyo.Sine(freq=220, phase=0, mul=.3, add=.3)
# delay = pyo.Delay(a, delay=.3, feedback=lfo, maxdelay=3).out()
delay = pyo.Delay(a).out()
# scope0 = pyo.Scope(a)
# scope = pyo.Scope(a+delay+lfo)

# s.gui()
