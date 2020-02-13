'''
import useful modules for fft analysis
'''
import numpy as np

from xml.dom import minidom
import matplotlib.pyplot as plt

import thinkdsp


'''==========================================================='''
''' Emerson parsing function definition'''
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

            # looking into the entity properties
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

                elif name == 'MaxFrequency':
                    MaxFrequency = property.firstChild.data

    return {'len': data_list_len, 'timestamp': timestamp, 'deltaTime': delta_time, 'MaxFrequency': MaxFrequency, 'signal': data_final_list}

'''==========================================================='''
''' Emerson vibration files path'''
filePath = 'C://Users//cmolina//PycharmProjects//test_ThinkDSP//Emerson Files//42b1b828-1fb7-4468-ac0d-7959be794f85.xml'

'''==========================================================='''
''' Get Emerson wave form data '''
wave_data = getEmersonWaveFormData(filePath)

''' Get Waveform parameters from Emerson data JSON'''
wave_JSON = wave_data['signal']
dt_JSON = float(wave_data['deltaTime'])
timeStamp_JSON = float(wave_data['timestamp'])
N_wave_JSON = wave_data['len']

'''==========================================================='''
''' Get Emerson wave form data '''
spectrum_data = getEmersonSpectrumData(filePath)

''' Get Spectrum parameters from Emerson data JSON'''
N_spectrum_JSON = spectrum_data['len']
spectrum_JSON = spectrum_data['signal']
MaxFrequency_JSON = float(spectrum_data['MaxFrequency'])

'''==========================================================='''
''' Calculated parameters'''
framerate = 1/dt_JSON
duration = N_wave_JSON*dt_JSON

''' Print data to inspect parameters'''
# print('data: ', wave_data)
# print('number of samples: ', N_wave_JSON)
# print('sample frequency: ', framerate)
# print('duration of wave: ', duration)

''' creating linear time vector to create a wave object'''
ts = np.linspace(0, duration, N_wave_JSON, endpoint=False)

''' creating a Wave object'''
wave = thinkdsp.Wave(ys=wave_JSON, ts=ts, framerate=framerate)

''' working with the wave object'''
wave.unbias()
wave.normalize()
wave.window(np.hanning(len(wave_JSON)))  # windowing = Hanning

plt.subplot(221)
plt.title('Waveform')
plt.ylabel('Axis X')
wave.plot()

plt.subplot(223)
plt.ylabel('Axis Z')
plt.xlabel('Time (s)')
wave.plot()


# plt.show()

# plt.plot(wave.ts, wave.ys)
# plt.subplot(212)
# plt.psd(x=wave.ys, NFFT=N_wave_JSON, Fs=framerate, pad_to=N_wave_JSON*2)  # power spectrum density
# plt.show()

'''==========================================================='''
''' creating a spectrum object from a wave object'''
spectrum = wave.make_spectrum()

''' working with the spectrum'''
# spectrum.low_pass(cutoff=625)
# spectrum.high_pass(cutoff=625)
spectrum.hs *= 2/N_wave_JSON  # looking for a normalized magnitude value


''' printing data to inspect '''
# print(spectrum.max_freq)  # max_freq = 800 Hz
# print(spectrum.amps[:5], '===', len(spectrum))
# print(spectrum_JSON[:5], '===', len(spectrum_JSON))

''' plotting spectrum'''
plt.subplot(222)
plt.title('Spectrum')
spectrum.plot(high=MaxFrequency_JSON, linewidth=1, alpha=0.7)  # MaxFrequency = 625 (from xml data)

plt.subplot(224)
plt.xlabel('Freq (Hz)')
spectrum.plot(high=MaxFrequency_JSON, linewidth=1, alpha=0.7)  # MaxFrequency = 625 (from xml data)

# plt.subplot(313)
# spectrum.plot_power(high=MaxFrequency_JSON, linewidth=1, alpha=0.7)  # MaxFrequency = 625 (from xml data)
# plt.ylabel('Power')

plt.show()

'''==========================================================='''
''' creating linear frequency vector to plot original spectrum'''
fs_JSON = np.linspace(0, MaxFrequency_JSON, N_spectrum_JSON)

''' plotting original spectrum'''
# plt.plot(fs_JSON, spectrum_JSON, linewidth=1, alpha=0.7)
# plt.show()


'''==========================================================='''
''' testing code '''
# fs_JSON = np.arange(N_JSON)  # indexes
# spectrum_calc = np.zeros(N)  # creating an array of zeros
# spectrum_calc[:len(spectrum_JSON)] = spectrum_JSON  # inserting spectrum_JSON into the array of zeros

# plt.plot(fs_JSON, spectrum_JSON, linewidth=1, alpha=0.7)

# plt.plot(fs_JSON,spectrum_JSON)
# plt.plot(spectrum.fs, spectrum.amps)
# plt.show()

# ys2 = np.zeros(2*N)
# ys2[round(N/2):round(3*N/2)] = ys
# ts2 = np.linspace(0, duration*2, N*2, endpoint=False)

# temp1_zeros = np.zeros(int(N/2))
# temp1_zeros[:len(spectrum_JSON)] = spectrum_JSON
# temp2_zeros = np.zeros(int(N/2))
# temp2_zeros[:len(fs_JSON)] = fs_JSON
# spectrum2 = thinkdsp.Spectrum(hs=temp1_zeros, fs=temp2_zeros, framerate=framerate)

# ''' reconstructing wave back from Emerson Spectrum data'''
# wave2 = spectrum2.make_wave()
#
# ''' plotting original wave back'''
# wave2.plot()  # does not look like the original wave
# plt.show()

# ''' creating a spectrum from Emerson data'''
# spectrum2 = thinkdsp.Spectrum(hs=spectrum_JSON, fs=fs_JSON, framerate=framerate)

# ''' plotting a spectrum from Emerson data'''
# spectrum2.plot(linewidth=1, alpha=0.7)

# ''' reconstructing wave back from Spectrum data'''
# spectrum.hs /= N/2  # spectrum.hs needs to be without change to reconstruct the original signal
# wave1 = spectrum.make_wave()
#
# ''' plotting original wave back'''
# wave1.plot()
# plt.show()

