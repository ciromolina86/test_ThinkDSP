import Emerson
import numpy as np

spectra = np.full(shape=10, fill_value=Emerson.spectrum)

for s in spectra:
    print(s.amps)
    print()
