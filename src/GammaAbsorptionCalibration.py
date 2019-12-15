import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from src.LinearPlot import *
from src.Data import *
from src.EnergyChannelCalibrationPlot import *


class GammaAbsorptionCalibration:

    def __init__(self):
        gamma_energies, percentages = self.get_absorption_data()
        gamma_energies = np.log10(gamma_energies)
        percentages = np.log10(percentages)
        legend_string = [
            'Data retrieved from specification',
            'Cubic interpolation fit'
        ]
        plt.figure()
        plt.title('Plot of energy absorption rate of gamma rays against gamma energy')
        plt.xlabel(r'log$_{10}$(Gamma energy (keV))')
        plt.ylabel(r'log$_{10}$(Absorption rate (%))')
        plt.plot(gamma_energies, percentages, 'kx')

        f = interp1d(gamma_energies, percentages, kind='cubic')
        x_fitted = np.linspace(min(gamma_energies), max(gamma_energies), num=10000, endpoint=True)

        self.absorption_calibration = f

        plt.plot(x_fitted, f(x_fitted), '-', linewidth=1.5)
        plt.grid(color='#bfbfbf', linestyle='-', linewidth=.5, axis='both')
        plt.legend(legend_string)
        plt.savefig('../plots/absorption-probability.png', ppi=300)
        plt.show()

    def get_absorption_data(self):
        """
        Opens and reads in the two column data for the given filepath
        Parameters
        ----------
        Returns
        ------
        gamma_energies : np.ndarray
        percentages : np.ndarray
        """
        filepath = '../calibation/absorption-probability.csv'
        file = open(filepath, 'r')

        gamma_energies = np.array([])
        percentages = np.array([])

        for line in file:
            split_line = line.split(',')

            gamma_energy = float(split_line[0])
            percentage = float(split_line[1])

            gamma_energies = np.append(gamma_energies, gamma_energy)
            percentages = np.append(percentages, percentage)

        return gamma_energies, percentages

