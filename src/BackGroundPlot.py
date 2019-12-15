import numpy as np
import matplotlib.pyplot as plt
from src.EuShieldingComparision import *


class BackgroundPlot:

    filename = 'Background-1364.txt'
    time = 1364

    def __init__(self, energy_channel_calibration):
        self.energy_channel_calibration = energy_channel_calibration

        plt.figure(figsize=(6, 4))
        plt.title('Plot of background count rate against channel number')
        plt.xlabel('Energy Channel')
        plt.ylabel(r'Count rate ($s^{-1}$)')
        energy_channels, counts = get_data('../raw_data/{}'.format(self.filename))
        counts = counts / self.time
        xs = np.array([])
        ys = np.array([])
        for x, y in zip(energy_channels, counts):
            if x < 30000:
                xs = np.append(xs, x)
                ys = np.append(ys, y)
        plt.plot(xs, ys, 'k')
        plt.grid(color='#bfbfbf', linestyle='-', linewidth=.5, axis='both')
        plt.savefig('../plots/background-against-counts.png')
        plt.show()

        plt.figure(figsize=(6, 4))
        plt.title('Plot of background count rate against energy')
        plt.xlabel('Energy (keV)')
        plt.ylabel(r'Count rate ($s^{-1}$)')
        energy_channels, counts = get_data('../raw_data/{}'.format(self.filename))
        counts = counts / self.time
        xs = np.array([])
        ys = np.array([])
        for x, y in zip(energy_channels, counts):
            if x < 30000:
                x = (x - self.energy_channel_calibration.y_intercept.value) / self.energy_channel_calibration.gradient.value
                xs = np.append(xs, x)
                ys = np.append(ys, y)
        plt.plot(xs, ys, 'k')
        plt.grid(color='#bfbfbf', linestyle='-', linewidth=.5, axis='both')
        plt.savefig('../plots/background-against-energy.png')
        plt.show()


