'''
import useful modules for vibration analysis
'''
import os
from xml.dom import minidom
import matplotlib.pyplot as plt
import numpy as np
import warnings

import scipy.fftpack
import scipy.signal
import scipy.io.wavfile

import thinkdsp
import thinkplot

'''==========================================================='''

'''function to extract the Emerson wave form information'''
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

'''function to extract the Emerson spectrum information'''
def getEmersonSpectrumData(filepath):
    """

    :param filepath: filepath
    :return: dictionary with the parameters
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
        if record_type == 'Emerson.CSI.DataImport.MHM.SpectraData':

            properties = entity.getElementsByTagName("Property")

            # looking into the emtity properties
            for property in properties:
                name = property.getAttribute('Name')

                # Time between points
                if name == 'DeltaTimeBetweenPoints':
                    delta_time = property.firstChild.data

                # Raw Data
                elif name == 'Data':
                    # print (name)
                    # print (dataName)
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

'''==========================================================='''

''' Emerson vibration files path'''
filePath = 'Emerson Files//42b1b828-1fb7-4468-ac0d-7959be794f85.xml'

''' Get Emerson wave form data '''
wave_data = getEmersonWaveFormData(filePath)

''' Get Emerson wave form data '''
spectrum_data = getEmersonSpectrumData(filePath)

'''==========================================================='''

''' Get parameters from Emerson data JSON'''
ys = wave_data['signal']
d = float(wave_data['deltaTime'])
timeStamp = float(wave_data['timestamp'])
N = wave_data['len']

''' Get parameters from Emerson data JSON'''
N_JSON = spectrum_data['len']
Max_Freq = spectrum_data['MaxFrequency']
spectrum_JSON = spectrum_data['signal']

''' Calculated parameters'''
framerate = 1/d
duration = N*d
ts = np.linspace(0, duration, N)
fs = np.linspace(0, framerate*N, N)
# fs = np.arange(N2)
spectrum_calc = np.zeros(N)
spectrum_calc[:len(spectrum_JSON)] = spectrum_JSON

'''==========================================================='''

''' Print data to inspect parameters'''
# print('data: ', wave_data)
# print('number of samples: ', N)
# print('sample frequency: ', framerate)
# print('duration of wave: ', duration)

# print('original spectrum data: ', spectrum2[:10])
# print('thinkdsp spectrum data: ', spectrum.amps[:10])

'''==========================================================='''

wave = thinkdsp.Wave(ys, ts=ts, framerate=framerate)
# wave.normalize()
# wave.hamming()
# wave.plot()
# plt.show()

'''==========================================================='''

spectrum = wave.make_spectrum()
# spectrum.plot_power()
print(spectrum.max_freq)
spectrum.max_freq = Max_Freq
print(spectrum.max_freq) #
spectrum.plot()
plt.show()

'''==========================================================='''

plt.plot(fs, spectrum_calc)
plt.show()



