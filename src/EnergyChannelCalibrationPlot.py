import numpy as np
import matplotlib.pyplot as plt
from src.LinearPlot import *
from src.Data import *


class EnergyChannelCalibrationPlot(object):

    def __init__(self):
        xs = [59.5, 341, 478, 46.6]
        ys = [59.5 / 2.38, 310 / 2.38, 435 / 2.38, 20]
        y_errors = [1, 2, 3, 0.5]  # Plus or minus the error
        plt.figure()
        plt.errorbar(xs, ys, yerr=y_errors, fmt='kx')
        plt.show()

        plot = LinearPlot(Column(xs), Column(ys, y_errors))
        plot.title = 'Plot of channel number against energy'
        plot.x_label = 'Energy (keV)'
        plot.y_label = 'Channel Number'
        plot.include_best_fit = True
        plot.include_residual_plot = True
        plot.display_plot()

        self.gradient = plot.gradient_of_fit
        self.y_intercept = plot.y_intercept_of_fit

        plot.save_plot('../plots/channel-energy-calibration.png', ppi=300)
        plot.plot.show()
