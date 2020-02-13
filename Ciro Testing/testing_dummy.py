import Emerson
import numpy as np

# create spectrum objects array
spectra = np.full(shape=10, fill_value=Emerson.spectrum)

# print(len(spectra[0].amps))

i = 0
for s in spectra:
    # print(s.amps)
    # print(len(s.amps))
    print(i)
    i+=1

