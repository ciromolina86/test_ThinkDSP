import thinkdsp
import thinkplot
import thinkstats2

import numpy as np
import matplotlib.pyplot as plt

# ''' triangular signal analysis'''
# signal1 = thinkdsp.TriangleSignal(200)
# signal1.plot()
# plt.show()
#
# wave1 = signal1.make_wave(duration=0.5, framerate=10000)
# spectrum1 = wave1.make_spectrum()
# spectrum1.plot()
# plt.show()
#
# ''' square signal analysis'''
# signal2= thinkdsp.SquareSignal(100)
# signal2.plot()
# plt.show()
#
# wave2 = signal2.make_wave(duration=0.5, framerate=10000)
# spectrum2 = wave2.make_spectrum()
# spectrum2.plot()
# plt.show()

''' aliasing analysis'''
framerate = 10000

signal = thinkdsp.CosSignal(4500)
duration = signal.period*5
segment = signal.make_wave(duration, framerate=framerate)
segment.plot()
plt.show()

signal = thinkdsp.CosSignal(5500)
segment = signal.make_wave(duration, framerate=framerate)
segment.plot()
plt.show()
