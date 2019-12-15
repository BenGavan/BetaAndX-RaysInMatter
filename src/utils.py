import numpy as np



def print_separator():
    print("--------------")


def print_value(label, value):
    print_separator()
    print(label)
    print(value)



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



