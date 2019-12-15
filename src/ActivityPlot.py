import numpy as np
import matplotlib.pyplot as plt
from src.EuShieldingComparision import *


class ActivityPlot:

    def __init__(self, energy_channel_calibration, absorption_calibration, filename, shielding):
        self.energy_channel_calibration = energy_channel_calibration
        self.absorption_calibration = absorption_calibration
        self.shielding = shielding

        element_name = filename[:2]
        time = float(filename[3:7])
        print('time = ', time, '| ', filename)

        plt.figure(figsize=(6, 4))
        plt.title('Plot of count rate against channel number - {} - {} shielding'.format(element_name, shielding), fontsize=10)
        plt.xlabel('Energy Channel')
        plt.ylabel(r'Count rate ($s^{-1}$)')
        energy_channels, counts = get_data('../raw_data/{}'.format(filename))
        counts = counts / time
        xs = np.array([])
        ys = np.array([])
        for x, y in zip(energy_channels, counts):
            if x < 30000:
                xs = np.append(xs, x)
                ys = np.append(ys, y)
        plt.plot(xs, ys, 'k')
        plt.grid(color='#bfbfbf', linestyle='-', linewidth=.5, axis='both')
        plt.tight_layout()
        plt.savefig('../plots/{}/activity-against-counts-{}-{}.png'.format(element_name.lower(), time, shielding))
        plt.show()

        plt.figure(figsize=(6, 4))
        plt.title('Plot of count rate against energy - {} - {} shielding'.format(element_name, shielding), fontsize=10)
        plt.xlabel('Energy (keV)')
        plt.ylabel(r'Count rate ($s^{-1}$)')
        energy_channels, counts = get_data('../raw_data/{}'.format(filename))
        counts = counts / time
        xs = np.array([])
        ys = np.array([])
        for x, y in zip(energy_channels, counts):
            if x < 30000:
                x = (x - self.energy_channel_calibration.y_intercept.value) / self.energy_channel_calibration.gradient.value
                xs = np.append(xs, x)
                ys = np.append(ys, y)
        plt.plot(xs, ys, 'k')
        plt.grid(color='#bfbfbf', linestyle='-', linewidth=.5, axis='both')
        plt.tight_layout()
        plt.savefig('../plots/{}/activity-against-energy-{}s-{}.png'.format(element_name.lower(), time, shielding))
        plt.show()

        plt.figure(figsize=(6, 4))
        plt.title('Plot of count rate against energy - {} - {} shielding - Adjusted for photon response'.format(element_name, shielding), fontsize=8)
        plt.xlabel('Energy (keV)')
        plt.ylabel(r'Count rate ($s^{-1}$)')
        energy_channels, counts = get_data('../raw_data/{}'.format(filename))
        counts = counts / time
        xs = np.array([])
        ys = np.array([])
        for x, y in zip(energy_channels, counts):
            if x < 30000:
                x = (x - self.energy_channel_calibration.y_intercept.value) / self.energy_channel_calibration.gradient.value
                if x > 1000:
                    continue
                y = y * pow(10, - absorption_calibration.absorption_calibration(np.log10(x))) * 100
                xs = np.append(xs, x)
                ys = np.append(ys, y)
        plt.plot(xs, ys, 'k')
        plt.grid(color='#bfbfbf', linestyle='-', linewidth=.5, axis='both')
        plt.tight_layout()
        plt.savefig('../plots/{}/activity-against-energy-{}s-{}-adjusted.png'.format(element_name.lower(), time, shielding))
        plt.show()
