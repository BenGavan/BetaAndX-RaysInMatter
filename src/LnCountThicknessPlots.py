import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from src.LinearPlot import *
from src.Data import *
from src.EnergyChannelCalibrationPlot import *
from src.GammaAbsorptionCalibration import *


class LnCountThicknessPlots:

    filenames = [
        'Eu-1205s-8.4mmAluminium.txt',
        'Eu-1231s-0.75mmAluminium.txt',
        'Eu-2393-6mmAl.txt',
        'Eu-2714-3.9mmAl.txt',
        # 'Eu-2310-Nothing.txt'
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
        # pow(10, -10)
    ]

    thickness_errors = [
        0.17,
        0.05,
        0.11,
        0.11,
        # pow(10, -10)
    ]

    def __init__(self):
        all_energy_channels = []
        all_counts = []
        for filename in self.filenames:
            energy_channels, counts = get_data('../raw_data/' + filename)
            all_energy_channels.append(energy_channels)
            all_counts.append(counts)

        for current_channel in range(511):
            if current_channel < 1 or current_channel > 50:
                continue
            counts_for_chan = []
            for counts in all_counts:
                counts_for_chan.append(counts[current_channel])

            xs = []
            x_is_zero = False
            index = 0
            for x in counts_for_chan:
                if x == 0:
                    x_is_zero = True
                    break
                # x = x / self.times[index]
                xs.append(np.log(x))
                index += 1

            if x_is_zero:
                continue

            ys = xs
            y_errors = 1 / np.sqrt(np.abs(ys))
            # xs = self.thickness
            xs = []
            for x in self.thickness:
                xs.append(x * 0.1)







            print(xs, ys, y_errors)

            # plt.figure()
            # plt.errorbar(xs, ys, y_errors, fmt='kx')
            # plt.xlabel('ln(counts)')
            # plt.ylabel('Thickness (mm)')
            # plt.savefig('../log_plots/{}.png'.format(current_channel), ppi=100)
            # plt.close()

            plot = LinearPlot(Column(xs), Column(ys, y_errors))
            plot.title = 'Plot of the natural log of the measured counts against aluminium shielding thickness for ' \
                         'energy channel {}'.format(current_channel)
            plot.x_label = 'Thickness (cm)'
            plot.y_label = 'ln(counts)'
            plot.include_residual_plot = True
            plot.include_best_fit = True
            plot.display_plot()
            plot.save_plot('../log_plots_alt/{}.png'.format(current_channel))
            plot.plot.show()
            plot.plot.close()


