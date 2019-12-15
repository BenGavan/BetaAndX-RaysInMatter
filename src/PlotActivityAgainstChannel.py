import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from src.LinearPlot import *
from src.Data import *
from src.EnergyChannelCalibrationPlot import *
from src.GammaAbsorptionCalibration import *
from src.ThicknessLogCountPlots import *
from src.EuShieldingComparision import *


class PlotActivityAgainstChannel:

    file_names = [
        'Am-3888s-20mmPer.txt',
        'Background-1364.txt',
        'Cs-1321s-20mmPer.txt',
        'Eu-1205s-8.4mmAluminium.txt',
        'Eu-1231s-0.75mmAluminium.txt',
        'Eu-1806s-20mmPer.txt',
        'Eu-1847s-2-lead.txt',
        'Eu-2139s-1-lead.txt',
        'Eu-2310-Nothing.txt',
        'Eu-2393-6mmAl.txt',
        'Eu-2714-3.9mmAl.txt',
        'Na-1819s-20mmPer.txt',
        'Na-5900-Nothing.txt',
        'Pb-2380-nothing.txt',
        'Sr-481-Nothing.txt',
        'Sr-674s-Nothing.txt',
        'Sr-5111-no-Per.txt'
    ]

    colors = [
        '#000000',  # Black
        '#020ef2',  # Dark blue
        '#f00202',  # Red
        '#f06d02',  # Orange
        '#05c902',  # Green
        '#02f2ee',  # Cyan
        '#3495eb',  # Blue
        '#8602f2',  # Purple
    ]

    def __init__(self, energy_channel_calibration, gamma_calibration):
        self.energy_channel_calibration = energy_channel_calibration
        self.gamma_calibration = gamma_calibration
        self.plot_eu()
        self.plot_na()
        self.plot_one_of_each_eu()
        self.plot_varying_aluminium_eu()
        pass

    def plot_eu(self):
        filenames = [
            'Eu-2310-Nothing.txt',
            'Eu-1205s-8.4mmAluminium.txt',
            'Eu-1231s-0.75mmAluminium.txt',
            'Eu-1806s-20mmPer.txt',
            'Eu-1847s-2-lead.txt',
            'Eu-2139s-1-lead.txt',
            'Eu-2393-6mmAl.txt',
            'Eu-2714-3.9mmAl.txt',
        ]

        times = [
            2310,
            1205,
            1231,
            1806,
            1847,
            2139,
            2393,
            2714
        ]

        legend_string = [
            'No shielding',
            '8.4 mm Aluminium',
            '0.75 mm Aluminium',
            '20 mm Perspex',
            '2.45 mm Lead',
            '1.225 mm Lead',
            '6 mm Aluminium',
            '3.9 mm Aluminium'
        ]

        plt.figure(figsize=(6, 4))
        plt.title('Plot of count rate against energy channel number - Eu')
        plt.xlabel('Energy Channel')
        plt.ylabel(r'Count rate ($s^{-1}$)')
        index = 0
        for filename in filenames:
            energy_channels, counts = get_data('../raw_data/{}'.format(filename))
            counts = counts / times[index]
            xs = np.array([])
            ys = np.array([])
            for x, y in zip(energy_channels, counts):
                xs = np.append(xs, x)
                ys = np.append(ys, y)
            plt.plot(xs, ys, self.colors[index])
            index += 1
        plt.legend(legend_string)
        plt.grid(color='#bfbfbf', linestyle='-', linewidth=.5, axis='both')
        plt.savefig('../plots/eu/eu-combined-activity-against-counts.png')
        plt.show()

        plt.figure(figsize=(6, 4))
        plt.title('Plot of count rate against energy - Eu')
        plt.xlabel('Energy (keV)')
        plt.ylabel(r'Count rate ($s^{-1}$)')
        index = 0
        for filename in filenames:
            energy_channels, counts = get_data('../raw_data/{}'.format(filename))
            counts = counts / times[index]
            xs = np.array([])
            ys = np.array([])
            for x, y in zip(energy_channels, counts):
                x = (x - self.energy_channel_calibration.y_intercept.value) / self.energy_channel_calibration.gradient.value
                if x > 1000:
                    continue
                xs = np.append(xs, x)
                ys = np.append(ys, y)
            plt.plot(xs, ys, self.colors[index], linewidth=0.75)
            index += 1
        plt.legend(legend_string)
        plt.grid(color='#bfbfbf', linestyle='-', linewidth=.5, axis='both')
        plt.savefig('../plots/eu/eu-combined-activity-against-energy.png')
        plt.show()

        plt.figure(figsize=(6, 4))
        plt.title('Plot of count rate against energy (Adjusted for gamma absorption) - Eu', fontsize=10)
        plt.xlabel('Energy (keV))')
        plt.ylabel(r'Count rate ($s^{-1}$)')
        index = 0
        for filename in filenames:
            energy_channels, counts = get_data('../raw_data/{}'.format(filename))
            counts = counts / times[index]
            xs = np.array([])
            ys = np.array([])
            for x, y in zip(energy_channels, counts):
                if np.log10(x) < 0:
                    continue
                x = (x - self.energy_channel_calibration.y_intercept.value) / self.energy_channel_calibration.gradient.value
                if x > 1000:
                    continue
                y = y * (1 / pow(10, self.gamma_calibration.absorption_calibration(np.log10(x))))
                xs = np.append(xs, x)
                ys = np.append(ys, y)
            plt.plot(xs, ys, self.colors[index])
            index += 1
        # plt.ylim(0, 0.007)
        plt.legend(legend_string, loc='upper center', bbox_to_anchor=(0.42,1), frameon=False, fontsize=8)
        plt.grid(color='#bfbfbf', linestyle='-', linewidth=.5, axis='both')
        plt.savefig('../plots/eu/eu-combined-activity-against-energy-(adjusted-gamma).png')
        plt.show()

    def plot_one_of_each_eu(self):
        filenames = [
            'Eu-1205s-8.4mmAluminium.txt',
            'Eu-1806s-20mmPer.txt',
            'Eu-2139s-1-lead.txt',
            'Eu-1847s-2-lead.txt',
            'Eu-2310-Nothing.txt',
        ]

        times = [
            1205,
            1806,
            2139,
            1847,
            2310
        ]

        legend_string = [
            '8.4 mm Aluminium',
            '20 mm Perspex',
            '1.225 mm Lead',
            '2.45 mm Lead',
            'No Shielding',
        ]

        colors = [
            'k',
            'b',
            'y',
            'r',
            'g'
        ]

        plt.figure(figsize=(6, 4))
        plt.title('Plot of count rate against energy with various shielding - Eu', fontsize=9.5)
        plt.xlabel('Energy (keV))')
        plt.ylabel(r'Count rate ($s^{-1}$)')
        index = 0
        for filename in filenames:
            energy_channels, counts = get_data('../raw_data/{}'.format(filename))
            counts = counts / times[index]
            xs = np.array([])
            ys = np.array([])
            for x, y in zip(energy_channels, counts):
                if np.log10(x) < 0:
                    continue
                x = (x - self.energy_channel_calibration.y_intercept.value) / self.energy_channel_calibration.gradient.value
                if x > 1000:
                    continue
                xs = np.append(xs, x)
                ys = np.append(ys, y)
            plt.plot(xs, ys, colors[index])
            index += 1
        # plt.ylim(0, 0.007)
        plt.legend(legend_string, frameon=False, fontsize=8)
        plt.grid(color='#bfbfbf', linestyle='-', linewidth=.5, axis='both')
        plt.savefig('../plots/eu/eu-combined-(one-of-each-shielding)-activity-against-energy.png')
        plt.show()


    def plot_varying_aluminium_eu(self):
        filenames = [
            'Eu-1205s-8.4mmAluminium.txt',
            'Eu-2393-6mmAl.txt',
            'Eu-2714-3.9mmAl.txt',
            'Eu-1231s-0.75mmAluminium.txt',
            'Eu-2310-Nothing.txt',
        ]

        times = [
            1205,
            2393,
            2714,
            1231,
            2310,
        ]

        legend_string = [
            '8.4 mm Aluminium',
            '6 mm Aluminium',
            '3.9 mm Aluminium',
            '0.75 mm Aluminium',
            'No shielding',
        ]

        title_strings = [
            '8.4 mm Aluminium',
            '6 mm Aluminium',
            '3.9 mm Aluminium',
            '0.75 mm Aluminium',
            'No shielding',
        ]

        colors = [
            'k',
            'b',
            'y',
            'r',
            'g'
        ]

        plt.figure(figsize=(6, 4))
        plt.title('Plot of count rate against energy with various aluminium shielding thickness - Eu', fontsize=9.5)
        plt.xlabel('Energy (keV))')
        plt.ylabel(r'Count rate ($s^{-1}$)')
        index = 0
        for filename in filenames:
            energy_channels, counts = get_data('../raw_data/{}'.format(filename))
            counts = counts / times[index]
            xs = np.array([])
            ys = np.array([])
            for x, y in zip(energy_channels, counts):
                if np.log10(x) < 0:
                    continue
                x = (x - self.energy_channel_calibration.y_intercept.value) / self.energy_channel_calibration.gradient.value
                if x > 1000:
                    continue
                xs = np.append(xs, x)
                ys = np.append(ys, y)
            plt.plot(xs, ys, colors[index])
            index += 1
        # plt.ylim(0, 0.007)
        plt.legend(legend_string, frameon=False, fontsize=8)
        plt.grid(color='#bfbfbf', linestyle='-', linewidth=.5, axis='both')
        plt.tight_layout()
        plt.savefig('../plots/eu/eu-combined-(varying-aluminium)-activity-against-energy.png')
        plt.show()


    def plot_na(self):
        filenames = [
            'Na-1819s-20mmPer.txt',
            'Na-5900-Nothing.txt',
        ]

        times = [
            1819,
            5900
        ]

        legend_string = [
            '20 mm Perspex',
            'No Shielding',
        ]

        title_strings = [
            '20 mm Perspex',
            'No',
        ]

        colors = [
            'b',
            'k'
        ]

        plt.figure(figsize=(6, 4))
        plt.title('Plot of count rate against energy channel channel number - Na')
        plt.xlabel('Energy Channel')
        plt.ylabel(r'Count rate ($s^{-1}$)')
        index = 0
        for filename in filenames:
            energy_channels, counts = get_data('../raw_data/{}'.format(filename))
            counts = counts / times[index]
            xs = np.array([])
            ys = np.array([])
            for x, y in zip(energy_channels, counts):
                if x < 300:
                    xs = np.append(xs, x)
                    ys = np.append(ys, y)
            plt.plot(xs, ys, colors[index])
            index += 1
        plt.legend(legend_string)
        plt.grid(color='#bfbfbf', linestyle='-', linewidth=.5, axis='both')
        plt.tight_layout()
        plt.savefig('../plots/na/na-combined-activity-against-counts.png')
        plt.show()


        plt.figure(figsize=(6, 4))
        plt.title('Plot of count rate against energy - Na')
        plt.xlabel('Energy (keV)')
        plt.ylabel(r'Count rate ($s^{-1}$)')
        index = 0
        for filename in filenames:
            energy_channels, counts = get_data('../raw_data/{}'.format(filename))
            counts = counts / times[index]
            xs = np.array([])
            ys = np.array([])
            for x, y in zip(energy_channels, counts):
                if x < 300:
                    x = (x - self.energy_channel_calibration.y_intercept.value) / self.energy_channel_calibration.gradient.value
                    xs = np.append(xs, x)
                    ys = np.append(ys, y)
            plt.plot(xs, ys, colors[index])
            index += 1
        plt.legend(legend_string)
        plt.grid(color='#bfbfbf', linestyle='-', linewidth=.5, axis='both')
        plt.tight_layout()
        plt.savefig('../plots/na/na-combined-activity-against-energy.png')
        plt.show()

        plt.figure(figsize=(6, 4))
        plt.title('Plot of count rate against energy - Na - Adjusted for photon response', fontsize=10)
        plt.xlabel('Energy (keV)')
        plt.ylabel(r'Count rate ($s^{-1}$)')
        index = 0
        for filename in filenames:
            energy_channels, counts = get_data('../raw_data/{}'.format(filename))
            counts = counts / times[index]
            xs = np.array([])
            ys = np.array([])
            for x, y in zip(energy_channels, counts):
                if x < 300:
                    x = (x - self.energy_channel_calibration.y_intercept.value) / self.energy_channel_calibration.gradient.value
                    if x > 1000:
                        continue
                    y = y * pow(10, - self.gamma_calibration.absorption_calibration(np.log10(x))) * 100
                    xs = np.append(xs, x)
                    ys = np.append(ys, y)
            plt.plot(xs, ys, colors[index])
            index += 1
        plt.legend(legend_string)
        plt.grid(color='#bfbfbf', linestyle='-', linewidth=.5, axis='both')
        plt.tight_layout()
        plt.savefig('../plots/na/na-combined-activity-against-energy-(adjusted).png')
        plt.show()


