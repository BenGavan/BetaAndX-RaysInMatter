import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from src.LinearPlot import *
from src.Data import *
from src.EnergyChannelCalibrationPlot import *
from src.GammaAbsorptionCalibration import *
from src.ThicknessLogCountPlots import *
from src.EuShieldingComparision import *
from src.PlotActivityAgainstChannel import *
from src.BackGroundPlot import *
from src.ActivityPlot import *
from src.LnCountThicknessPlots import *


def main():
    print('Hey :)')

    # energy_channel_calibration = EnergyChannelCalibrationPlot()
    # absorption_calibration = GammaAbsorptionCalibration()

    # PlotActivityAgainstChannel(energy_channel_calibration, absorption_calibration)

    # BackgroundPlot(energy_channel_calibration)

    # EuShieldingComparision()

    # ThicknessLogCountPlots()

    # plot_calibration_plots()

    LnCountThicknessPlots()



    file_names = [
        'Am-3888s-20mmPer.txt',
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
        'Sr-0481-Nothing.txt',
        'Sr-0674s-Nothing.txt',
        'Sr-5111-no-Per.txt'
    ]



    legend_string = [
        '8.4 mm Aluminium',
        '0.75 mm Aluminium',
        '20 mm Perspex',
        '2.45 mm Lead',
        '1.225 mm Lead',
        'No shielding',
        '6 mm Aluminium',
        '3.9 mm Aluminium'
    ]

    shielding = [
        '20 mm perspex',
        '20 mm perspex',
        '8.40 mm Aluminium',
        '0.75 mm Aluminium',
        '20 mm perspex',
        '2.45 mm Lead',
        '1.225 mm Lead',
        'No shielding',
        '6 mm Aluminium',
        '3.9 mm Aluminium',
        '20 mm Perspex',
        'No',
        'No',
        'No',
        'No',
        'No',
    ]

    # index = 0
    # for filename in file_names:
    #     ActivityPlot(energy_channel_calibration, absorption_calibration, filename, shielding=shielding[index])
    #     index += 1


    # energy_channel, counts = get_data('../raw_data/Eu-2310-Nothing.txt')
    #
    # plot_data_energy_channel_adjusted(energy_channel, counts, 'Eu', 2310, energy_channel_calibration)
    # process_file(file_names[1], energy_channel_calibration, absorbion_calibration)

    # energy_channel, counts = get_data('../raw_data/Am-3888s-20mmPer.txt')
    #
    # plot_data_energy_channel_adjusted(energy_channel, counts, 'Am', 3888, energy_channel_calibration)

    # energy_channel, counts = get_data('../raw_data/Sr-5111-no-Per.txt')
    #
    # plot_data_energy_channel_adjusted(energy_channel, counts, 'Sr', 5111, energy_channel_calibration, vline=200.6)

    # energy_channel, counts = get_data('../raw_data/Pb-2380-nothing.txt')
    #
    # plot_data_energy_channel_adjusted(energy_channel, counts, 'Pb', 2380, energy_channel_calibration, vlines=[15, 61.5, 46.6,49.6], upper_limit=100)


    # for filename in file_names:
    #     process_file(filename)


def plot_every_individual_plot(file_names, shielding, energy_channel_calibration, absorption_calibration):
    index = 0
    for filename in file_names:
        ActivityPlot(energy_channel_calibration, absorption_calibration, filename, shielding=shielding[index])
        index += 1


def plot_calibration_plots():
    energy_channel, counts = get_data('../raw_data/Am-3888s-20mmPer.txt')

    # plot_data_energy_channel_adjusted(energy_channel, counts, 'Am', 3888, energy_channel_calibration,
    #                                   vlines=[59.5], upper_limit=1000)

    plot_data(energy_channel, counts, 'Am', '20 mm perspex', 3888, vlines=[25], upper_limit=1000)

    energy_channel, counts = get_data('../raw_data/Na-1819s-20mmPer.txt')
    plot_data(energy_channel, counts, 'Na', '20 mm perspex', 1819, vlines=[130], upper_limit=1000)

    energy_channel, counts = get_data('../raw_data/Cs-1321s-20mmPer.txt')
    plot_data(energy_channel, counts, 'Cs', '20 mm perspex', 1321, vlines=[183], upper_limit=1000)

    energy_channel, counts = get_data('../raw_data/Pb-2380-nothing.txt')
    plot_data(energy_channel, counts, 'Pb', 'no', 2380, vlines=[20], upper_limit=100)

# plot_adjusted(energy_channels, counts, file_name[:2], absorbion_calibration)
# print('Here')

def process_file(filename, energy_channel_calibration, absorption_calibration):
    """
    Parameters
    ----------
    filename : str
    energy_channel_calibration : EnergyChannelCalibrationPlot
    absorption_calibration : GammaAbsorptionCalibration
    """
    filepath = '../raw_data/{}'.format(filename)
    energy_channels, counts = get_data(filepath)
    energy = (energy_channels * (1 / energy_channel_calibration.gradient.value)) + (1 / energy_channel_calibration.y_intercept.value)

    xs = np.array([])
    ys = np.array([])
    for x, y in zip(energy, counts):
        if x > 100 and x < 500:
            xs = np.append(xs, x)
            ys = np.append(ys, y)

    energy = xs
    counts = ys

    plot_data(energy, counts, filename[:2], filename[3:7], [0], 100000)
    x = get_max(energy, counts)
    print(x)

    plot_adjusted(energy, counts, filename[:2], absorption_calibration)


def get_data(filepath):
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


def plot_data(energy_channels, counts, source, shielding, duration, vlines, upper_limit):
    plt.figure(figsize=(6, 4))
    # plt.plot(energy_channels[:len(counts) - 400], counts[:len(counts) - 400], 'k.', ms=2)
    # maximums = get_max(energy_channels, counts)
    print_separator()
    print(energy_channels, counts)
    print_separator()
    xs = []
    ys = []
    for x, y in zip(energy_channels, counts):
        if x > upper_limit:
            continue
        y = y / duration
        xs.append(x)
        ys.append(y)

    legend_strings = []

    for x in vlines:

        plt.plot([x, x], [min(ys), max(ys) + 0.02 * max(ys)])
        legend_strings.append('Channel Number = {}'.format(x))

    legend_strings.append('Recorded data')

    plt.plot(xs, ys, 'k-', ms=2)
    plt.title('Number of counts against energy channel - {} - {} shielding'.format(source, shielding), fontsize=10)
    plt.xlabel('Energy channel')
    plt.ylabel(r'Count rate ($s^{-1}$)')
    plt.grid(color='#7a7a7a', linestyle='-', linewidth=.5, axis='y')
    plt.legend(legend_strings)
    plt.tight_layout()
    plt.savefig('../plots/{}-{}s-{}.png'.format(source, duration, shielding))
    plt.show()

def plot_data_energy_channel_adjusted(energy_channels, counts, source, duration, energy_channel_calibration, vlines, upper_limit):
    plt.figure(figsize=(6, 4))
    # plt.plot(energy_channels[:len(counts) - 400], counts[:len(counts) - 400], 'k.', ms=2)
    # maximums = get_max(energy_channels, counts)
    xs = []
    ys = []
    for x, y in zip(energy_channels, counts):

        x = (x - energy_channel_calibration.y_intercept.value) / energy_channel_calibration.gradient.value
        if x > upper_limit:
            continue
        y = y / duration
        # y = y / duration
        xs.append(x)
        ys.append(y)

    legend_strings = []

    for x in vlines:
        plt.plot([x, x], [min(ys), max(ys) + 0.02 * max(ys)])
        legend_strings.append('Energy = {} keV'.format(x))

    legend_strings.append('Recorded data')


    print(xs, ys)
    # plt.plot(xs, ys, 'rx')
    plt.plot(xs, ys, 'k-', ms=2)
    plt.title('Number of counts against energy channel - {}'.format(source))
    plt.xlabel('Energy (keV)')
    plt.ylabel(r'Count rate ($s^{-1}$)')
    plt.grid(color='#7a7a7a', linestyle='-', linewidth=.5, axis='y')
    plt.legend(legend_strings)
    plt.tight_layout()
    plt.savefig('../plots/{}-{}s-energy-channel-adjusted.png'.format(source, duration))
    plt.show()


def plot_adjusted(energy_channels, counts, source, absorption_calibration):
    plt.figure(figsize=(6, 4))
    # plt.plot(energy_channels[:len(counts) - 400], counts[:len(counts) - 400], 'k.', ms=2)
    # maximums = get_max(energy_channels, counts)
    xs = []
    ys = []
    for x, y in zip(energy_channels, counts):
        y = y * (1 / pow(10, absorption_calibration.absorption_calibration(np.log10(x))))
        xs.append(x)
        ys.append(y)

    x = 434
    uncert = 3

    print(xs, ys)
    # plt.plot(xs, ys, 'rx')
    plt.plot(xs, ys, 'k-', ms=2)
    plt.plot([x, x], [min(ys), max(ys)])
    plt.plot([x - uncert, x - uncert], [min(ys), max(ys)])
    plt.plot([x + uncert, x + uncert], [min(ys), max(ys)])
    plt.title('Number of counts against energy channel - {}'.format(source))
    plt.xlabel('Energy channels')
    plt.ylabel('Counts')
    plt.grid(color='#7a7a7a', linestyle='-', linewidth=.5, axis='y')
    plt.tight_layout()
    plt.savefig('../plots/{}-adjusted.png'.format(source))
    plt.show()


def get_max(xs, ys):
    if len(xs) != len(ys):
        print('ERROR: xs and ys needs to be the same length')
        return -1
    maximums = []
    current_max_y = ys[0]
    current_max_x = xs[0]
    i = 1
    while i < len(xs):
        if ys[i] > current_max_y:
            current_max_x = xs[i]
            current_max_y = ys[i]
        elif ys[i] < current_max_y:
            maximums.append([current_max_x, current_max_y])
            current_max_y = -1

        i += 1
    return maximums


if __name__ == '__main__':
    main()


