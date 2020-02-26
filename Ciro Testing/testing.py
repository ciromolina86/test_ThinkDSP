import thinkdsp
import thinkplot
import thinkstats2

import numpy as np
import matplotlib.pyplot as plt

'''
# testing differentiation
sig = thinkdsp.SinSignal(freq=1, amp=1, offset=0)
wave = sig.make_wave(duration=1, start=0, framerate=100)
spectrum = wave.make_spectrum()
new_spectrum = spectrum.differentiate()
new_wave = new_spectrum.make_wave()

# create a figure
fig = plt.figure()
# create a subplot
ax = fig.add_subplot(221)
# plot a wave
wave.plot(label='wave', color='b')
ax.legend()
# create a subplot
ax = fig.add_subplot(222)
# plot a spectrum
spectrum.plot(label='spec', color='b')
ax.legend()

# create a subplot
ax = fig.add_subplot(223)
# plot a wave
new_wave.plot(label='new wave', color='b')
ax.legend()
# create a subplot
ax = fig.add_subplot(224)
# plot a spectrum
new_spectrum.plot(label='new spec', color='b')
ax.legend()

plt.show()
'''

# testing integration
sig = thinkdsp.CosSignal(freq=1, amp=1, offset=0)
wave = sig.make_wave(duration=1, start=0, framerate=100)
spectrum = wave.make_spectrum()
new_spectrum = spectrum.integrate()
new_wave = new_spectrum.make_wave()

# create a figure
fig = plt.figure()
# create a subplot
ax = fig.add_subplot(221)
# plot a wave
wave.plot(label='wave', color='b')
ax.legend()
# create a subplot
ax = fig.add_subplot(222)
# plot a spectrum
spectrum.plot(label='spec', color='b')
ax.legend()

# create a subplot
ax = fig.add_subplot(223)
# plot a wave
new_wave.plot(label='new wave', color='b')
ax.legend()
# create a subplot
ax = fig.add_subplot(224)
# plot a spectrum
new_spectrum.plot(label='new spec', color='b')
ax.legend()

plt.show()
