import numpy as np
from src.Measurement import *
from src.utils import *


class Data:

    def __init__(self, filepath):
        """
        init: takes in the filepath as a string
        Parameters
        ----------
        filepath : str
        Returns
        ----------
        : Data
        """
        self.filepath = filepath
        self.headers, self.cols = self.get_data_from_filepath()

    def get_data_from_filepath(self):
        """
        Gets the data from a filepath and returns the header (1D array of strings) and columns (2D array)
        Returns
        ----------
        :[str]
        :[Column]
        """
        print("Getting filepath: ", self.filepath)
        file = open(self.filepath, "r")

        header = []
        columns = []

        line_counter = 0
        for line in file:
            row = []
            if line_counter != 0:
                columns.append([])

            index = 0

            while True:
                try:
                    row.append(line.split('\t')[index])
                    index += 1
                except IndexError:
                    break

            try:
                current_row_string = ""
                for i in range(len(row)):
                    row[i] = float(row[i])
                    number_of_spaces = len(header[i]) - len(str(row[i])) + 5
                    current_row_string += str(row[i]) + " " * number_of_spaces
                    columns[line_counter - 1].append(row[i])
                print(current_row_string)
            except ValueError:
                header_string = ""
                for i in range(len(row)):
                    header.append(row[i].replace('\n', ''))
                    if i == len(row) - 1:
                        header_string += header[i]
                    else:
                        header_string += header[i] + "  |  "
                print(header_string)

            line_counter += 1

        file.close()

        rows = columns

        print_value("cols before = ", columns)
        columns = np.zeros(shape=(len(columns[0]), len(columns)))

        for i in range(len(rows)):
            for j in range(len(rows[i])):
                columns[j][i] = rows[i][j]

        print_value("columns = ", columns)

        return header, columns


class Column:

    def __init__(self, values, uncertainties=None):
        self.values = values
        if uncertainties is None:
            # uncertainties = np.zeros(len(values))
            uncertainties = np.array([0] * len(values))
        self.uncertainties = uncertainties

    def to_measurements(self):
        """
        Returns an array of measurements
        :return:
        """
        measurements = []
        for val, uncertainty in zip(self.values, self.uncertainties):
            measurements.append(Measurement(val, uncertainty))
        return measurements

    def sum(self):
        """
        Returns the sum of the column in the form of a measurement
        Parameters
        ----------
        Returns
        ----------
        total: Measurement
        """
        measurements = self.to_measurements()
        total = Measurement(0, 0)
        for m in measurements:
            total = total + m
        return total

    def add_column(self, other):
        """
        Adds a column horizontally, propagating the errors each time using the Measurement class.
        Parameters
        ----------
        other : Column
        """
        for i in range(len(self.values)):
            measurement_one = Measurement(self.values[i], self.uncertainties[i])
            measurement_two = Measurement(self.values[i], other.uncertainties[i])

            new_measurement = measurement_one + measurement_two

            new_colunn_values = np.array([])
            new_colunn_uncertainties = np.array([])

            self.values[i] = new_measurement.value
            self.uncertainties[i] = new_measurement.uncertainty
