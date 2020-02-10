# import
import os
from xml.dom import minidom
import matplotlib.pyplot as plt
import numpy as np
import warnings

import scipy.fftpack
import scipy.signal
import scipy.io.wavfile




# function to extract the Emerson wave form information
def getEmersonWaveFormaData(filepath):
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

# function to extract the Emerson spectrum information
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

# FFT from internet
def fftPlot(sig, dt=None, block=False, plot=True):
    # here it's assumes analytic signal (real signal...)- so only half of the axis is required

    if dt is None:
        dt = 1
        t = np.arange(0, sig.shape[-1])
        xLabel = 'samples'
    else:
        t = np.arange(0, sig.shape[-1]) * dt
        xLabel = 'freq [Hz]'

    if sig.shape[0] % 2 != 0:
        warnings.warn("signal prefered to be even in size, autoFixing it...")
        t = t[0:-1]
        sig = sig[0:-1]

    sigFFT = np.fft.fft(sig) / t.shape[0]  # divided by size t for coherent magnitude

    freq = np.fft.fftfreq(t.shape[0], d=dt)

    # plot analytic signal - right half of freq axis needed only...
    firstNegInd = np.argmax(freq < 0)
    freqAxisPos = freq[0:firstNegInd]
    sigFFTPos = 2 * sigFFT[0:firstNegInd]  # *2 because of magnitude of analytic signal

    if plot:
        plt.figure()
        plt.plot(freqAxisPos, np.abs(sigFFTPos))
        plt.xlabel(xLabel)
        plt.ylabel('mag')
        plt.title('Analytic FFT plot')
        plt.show(block=block)

    return sigFFTPos, freqAxisPos





# getting variables
filePath = '42b1b828-1fb7-4468-ac0d-7959be794f85.xml'

# get Emerson wave form data******************************************************************
wave_data = getEmersonWaveFormaData(filePath)

print(wave_data)

# get parameter from Emerson wave form data
signal = wave_data['signal']
deltaTime = float(wave_data['deltaTime'])
timeStamp = float(wave_data['timestamp'])
signalLen = wave_data['len']

# time vector*********************************
time = []
t = 0

for n in range(signalLen):
    if n == 0:
        t = timeStamp
    else:
        t = t + deltaTime
    time.append(t)
# end time vector calculation*******************

print(signal)
print(time)

# possible normalizations...
signal = signal - np.mean(signal)

# fft
fft_signal = np.fft.fft(signal)
# fft_signal  = scipy.fftpack.fft( signal )

# positive portion
signalpow = np.abs(fft_signal)**2

# signalpow = np.abs( fft_signal /signalLen )**2
hz = np.linspace(0,625,signalLen)

print('signal power')
print (signalpow)

# plot time
plt.plot(time,signal)
plt.xlabel('Time (s)')
plt.show()

#plot frequency
plt.plot(hz,signalpow,'ms-')
plt.xlabel('Frequency (norm.)')
plt.ylabel('Search power')
plt.xlim([0, 625])
plt.show()




# Calculate FFT parameter to plot from emerson *******************************************************
spectrum_data = getEmersonSpectrumData(filePath)
print (spectrum_data)
esignalLen = spectrum_data['len']
esignal = spectrum_data['signal']
ehz = np.linspace(0,625, esignalLen)
# print (len(ehz))
#
#
# plot frequency from Emerson
plt.plot(ehz,esignal,'ms-')
plt.xlabel('EFrequency (norm.)')
plt.ylabel('Search power')
plt.xlim([0, 625])
plt.show()
#
#
# fftPlot(signal)