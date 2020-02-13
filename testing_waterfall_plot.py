import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_toolkits.mplot3d import axes3d
import matplotlib.ticker as ticker
import thinkdsp

def plot_waterfall_test():
    '''
    waterfall plot for up to 10 spectra

    :param parameters: list of spectra
    :return: void
    '''

    # Create a figure
    fig = plt.figure()

    # add a 3D subplot
    # ax1 = fig.add_subplot(111, projection='3d')
    ax1 = fig.add_subplot(projection='3d')

    # data arrays, Z must be a bi-dimensional array
    x = np.linspace(0, 1, 10, endpoint=False)
    z = np.array(np.sin(2*np.pi*x), ndmin=2)
    y = np.array([0,1,2,3,4,5,6,7,8,9])
    # y0 = np.zeros(10)
    # y1 = np.ones(10)
    # y2 = np.full(shape=(1,10), fill_value=2)
    # y3 = np.full(shape=(1,10), fill_value=3)
    # y4 = np.full(shape=(1,10), fill_value=4)
    # y5 = np.full(shape=(1,10), fill_value=5)
    # y6 = np.full(shape=(1,10), fill_value=6)
    # y7 = np.full(shape=(1,10), fill_value=7)
    # y8 = np.full(shape=(1,10), fill_value=8)
    # y9 = np.full(shape=(1,10), fill_value=9)

    # set the title and axis labels
    ax1.set_title('Spectrum comparison')
    ax1.set_xlabel('Frequency (Hz)')
    ax1.set_ylabel('Samples')
    ax1.set_zlabel('Magnitude')

    # set the axis limits
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 10)
    ax1.set_zlim(-1, 1)

    # set the tick of an axis to a specific spacing
    tick_spacing = 1
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    # plot x, y, z on 3D plot
    ax1.plot_wireframe(x, y[0], z)
    ax1.plot_wireframe(x, y[1], z)
    ax1.plot_wireframe(x, y[2], z)
    ax1.plot_wireframe(x, y[3], z)
    ax1.plot_wireframe(x, y[4], z)
    ax1.plot_wireframe(x, y[5], z)
    ax1.plot_wireframe(x, y[6], z)
    ax1.plot_wireframe(x, y[7], z)
    ax1.plot_wireframe(x, y[8], z)
    ax1.plot_wireframe(x, y[9], z)

    # Show plot
    plt.show()


def plot_waterfall(spectra, maxfreq):
    '''
    waterfall plot for 10 Spectrum objects

    :param parameters: list of 10 Spectrum objects
    :return: void
    '''

    # Create a figure
    fig = plt.figure()

    # add a 3D subplot
    # ax1 = fig.add_subplot(111, projection='3d')
    ax1 = fig.add_subplot(projection='3d')

    # creating samples vector
    # vector of samples
    y = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    # data arrays, Z must be a bi-dimensional array
    for s in spectra:
        i = 0
        # vector of frequencies
        x = np.linspace(0, maxfreq, 10, endpoint=False)

        # vector of magnitudes
        # z = np.array([[s.amps]])
        z = np.array(np.sin(2 * np.pi * x), ndmin=2)

        # set the title and axis labels
        ax1.set_title('Spectra comparison')
        ax1.set_xlabel('Frequency (Hz)')
        ax1.set_ylabel('Samples')
        ax1.set_zlabel('Magnitude')

        # set the tick of an axis to a specific spacing
        tick_spacing = 1
        ax1.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

        # plot x, y, z on 3D plot
        ax1.plot_wireframe(x, y[i], z)

        # increment index by 1
        i += 1

    # Show plot
    plt.show()

plot_waterfall_test()