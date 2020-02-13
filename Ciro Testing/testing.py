import thinkdsp
import thinkplot
import thinkstats2

import numpy as np
import matplotlib.pyplot as plt

cos_sig = thinkdsp.CosSignal(freq=440, amp=1.5, offset=0)
sin_sig = thinkdsp.SinSignal(freq=880, amp=0.5, offset=0)
mix = cos_sig + sin_sig

wave = mix.make_wave(duration=0.5, start=0, framerate=11025)
# wave.unbias()
wave.normalize()
wave.hamming()  # windowing options: .hamming(), .blackman()
wave.plot()
plt.show()

'''
period = mix.period
segment = wave.segment(start=0, duration=period*3)
segment.plot()
plt.show()
'''

spectrum = wave.make_spectrum()
# print(spectrum.max_freq)  # max frequency = fs/2 (nyquist frequency)
# peaks = spectrum.peaks()
# print(peaks[:5])
# spectrum.
spectrum.plot()
plt.show()
'''
spectrum.low_pass(cutoff=600, factor=0.01)
spectrum.plot()
plt.show()
'''
wave = spectrum.make_wave()
wave.plot()
plt.show()
