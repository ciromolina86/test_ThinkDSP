"""
 The envelope analysis is a very powerful tool used primarily for early detection of rolling element bearing .
 This analysis is used when the signal of interest has a form of repetitive impulses buried in a much stronger signal

 The spectrum of such a signal would consist of a harmonic series of frequency components spaced at the bearing defect
 frequency with the highest amplitude around the resonance frequency
"""




import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert, chirp
from xml.dom import minidom
from scipy.signal import butter, lfilter
import thinkdsp


# Functions
def getEmersonWaveFormData(filepath):
    """

    :param filepath: Emerson vibration sensor xml file
    :return: Dictionary with the parameters
    """

    data_list_len = 0
    data_final_list = []
    delta_time = 0
    timestamp = 0

    # Parse the given XML file:
    xmldoc = minidom.parse(filepath)

    entitiesDoc = xmldoc.documentElement
    entities = entitiesDoc.getElementsByTagName("Entity")

    # Looking into  "Entities"
    for entity in entities:
        record_type = entity.getAttribute('RecordType')

        # Find the record named 'Emerson.CSI.DataImport.MHM.WaveFormData'
        if record_type == 'Emerson.CSI.DataImport.MHM.WaveFormData':

            properties = entity.getElementsByTagName("Property")

            # looking into the emtity properties
            for property in properties:
                name = property.getAttribute('Name')

                # Time between points
                if name == 'DeltaTimeBetweenPoints':
                    delta_time = property.firstChild.data

                # Time tath the first point was read
                elif name == 'Date':
                    time = property.firstChild.data

                # RPM
                elif name == 'RPM':
                    rpm = property.firstChild.data
                # Raw Data
                elif name == 'Data':
                    # print (name)
                    # print (dataName)
                    data = entitiesDoc.getElementsByTagName("dataName")
                    data = property.getElementsByTagName("Data")
                    # print (data)
                    c = 0
                    for d in data:
                        c = c + 1

                        data_list = d.firstChild.data.split(',')
                        data_list_len = len(data_list)
                        for string_data in data_list:
                            float_data = float(string_data)
                            data_final_list.append(float_data)

                elif name == 'LastWrite_Time_as_UInt':
                    timestamp = property.firstChild.data

    return {'len': data_list_len, 'timestamp': timestamp, 'deltaTime': delta_time, 'signal': data_final_list}


'''=========================  Raw Vibration Signal   =================================='''
'''====================================================================================='''


''' Emerson vibration files path'''
filePath = '/home/developer/Documents/pyproject/test_ThinkDSP/Emerson Files/42b1b828-1fb7-4468-ac0d-7959be794f85.xml'

''' Get Emerson wave form data '''
wave_data = getEmersonWaveFormData(filePath)

''' Get Waveform parameters from Emerson data JSON'''
wave_JSON = wave_data['signal']
dt_JSON = float(wave_data['deltaTime'])
timeStamp_JSON = float(wave_data['timestamp'])
N_wave_JSON = wave_data['len']

''' Calculated parameters'''
fs = 1/dt_JSON
duration = N_wave_JSON*dt_JSON


''' creating linear time vector to create a wave object'''
t = np.linspace(0, duration, N_wave_JSON, endpoint=False)


'''=========================  Band-pas filter   =================================='''
'''====================================================================================='''

''' Creating a Wave object'''
raw_wave = thinkdsp.Wave(ys=wave_JSON, ts=t, framerate=fs)
''' working with the wave object'''
raw_wave.unbias()
raw_wave.normalize()
raw_wave.window(np.hanning(len(wave_JSON)))  # windowing = Hanning


''' Creating a spectrum object from a wave object'''
raw_spectrum = raw_wave.make_spectrum()

''' Filtering'''
raw_spectrum.high_pass(400)
raw_wave_filtered = raw_spectrum.make_wave()
filtered_signal = raw_wave_filtered.ys


''' Signal Enveloping using hilbert transform'''

analytic_signal = hilbert(filtered_signal)
amplitude_envelope = np.abs(analytic_signal)
instantaneous_phase = np.unwrap(np.angle(analytic_signal))
instantaneous_frequency = np.diff(instantaneous_phase) / (2.0*np.pi) * fs


'''=========================  Envelope Spectrum  =================================='''
'''====================================================================================='''


''' creating a Wave object'''
wave = thinkdsp.Wave(ys=amplitude_envelope, ts=t, framerate=fs)

''' working with the wave object'''
wave.unbias()
wave.normalize()
wave.window(np.hanning(len(wave_JSON)))  # windowing = Hanning


''' creating a spectrum object from a wave object'''
spectrum = wave.make_spectrum()

''' working with the spectrum'''
# spectrum.low_pass(cutoff=625)
# spectrum.high_pass(cutoff=625)
spectrum.hs *= 2/N_wave_JSON  # looking for a normalized magnitude value


'''=========================  Plotting  =================================='''
'''====================================================================================='''

fig = plt.figure()
ax0 = fig.add_subplot(211)
ax0.plot(t, filtered_signal, label='signal')
ax0.plot(t, amplitude_envelope, label='envelope')
ax0.set_xlabel("time in seconds")
ax0.legend()
plt.show()
plt.title('Spectrum')
spectrum.plot(high=625, linewidth=1, alpha=0.7)  # MaxFrequency = 625 (from xml data)
plt.show()
