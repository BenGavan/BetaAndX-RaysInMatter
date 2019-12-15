import numpy as np
import matplotlib.pyplot as plt
from src.EnergyChannelCalibrationPlot import *


class EuShieldingComparision:

    filenames = [
        'Eu-1205s-8.4mmAluminium.txt',
        'Eu-1231s-0.75mmAluminium.txt',
        'Eu-2393-6mmAl.txt',
        'Eu-2714-3.9mmAl.txt',
        'Eu-2310-Nothing.txt'
    ]

    times = [
        1205,
        1231,
        2393,
        2714,
        2310
    ]

    thickness = [
        8.4,
        0.75,
        6,
        3.9,
        pow(10, -10)
    ]

    thickness_errors = [
        0.17,
        0.05,
        0.11,
        0.11,
        pow(10, -10)
    ]

    colors = ['r', 'b', 'y', 'g', 'k']

    def __init__(self):
        energy_channel_calibration_plot = EnergyChannelCalibrationPlot()

        print()
        plt.figure()
        plt.title('Plot comparing the count rate when using different aluminium shielding thicknesses')
        plt.xlabel('Energy (keV)')
        plt.ylabel('Count')
        index = 0
        for filename in self.filenames:
            energy_channels, counts = self.get_data('../raw_data/{}'.format(filename))
            energy_channels = (energy_channels * energy_channel_calibration_plot.gradient.value) + energy_channel_calibration_plot.y_intercept.value
            counts = counts / self.times[index]
            fmt = self.colors[index] + '.'
            plt.plot(energy_channels, counts, fmt, ms = 1)
            index += 1
        plt.savefig('../plots/EuShieldingComparision.png', ppi=300)
        plt.show()



    def get_data(self, filepath):
        """
        Opens and reads in the two column data for the given filepath
        Parameters
        ----------
        filepath : str
        Returns
        ------
        energy_channels : np.ndarray
        counts : np.ndarray
        """
        file = open(filepath, 'r')

        energy_channels = np.array([])
        counts = np.array([])

        for line in file:
            split_line = line.split(' ')

            energy_channel = float(split_line[0])
            count = int(split_line[1])

            energy_channels = np.append(energy_channels, energy_channel)
            counts = np.append(counts, count)

        file.close()

        return energy_channels, counts



