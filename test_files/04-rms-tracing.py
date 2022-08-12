"""
04-rms-tracing.py - Auto-wah effect.

The auto-wah effect (also know as "envelope following filter") is like a
wah-wah effect, but instead of being controlled by a pedal, it is the RMS
amplitude of the input sound which control it. The envelope follower (RMS)
is rescaled and used to change the frequency of a bandpass filter applied
to the source.

"""
from pyo import *
from signal import pause

s = Server().boot()
s.start()
MINFREQ = 300
MAXFREQ = 8000

# Play the drum lopp.
# sf = SfPlayer("/home/pi/guitar_audio/drumloop.wav", loop=True)
sf = Input()

# Follow the amplitude envelope of the input sound.
follow = Follower(sf)

# Scale the amplitude envelope (0 -> 1) to the desired frequency
# range (MINFREQ -> MAXFREQ).
freq = Scale(follow, outmin=MINFREQ, outmax=MAXFREQ)

# Filter the signal with a band pass. Play with the Q to make the
# effect more or less present.
filter = ButBP(sf, freq=freq, q=20, mul=10).out()

pause()
