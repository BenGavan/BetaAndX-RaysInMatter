import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from src.Measurement import *

def print_separator():
    print("--------------")


def print_value(label, value):
    print_separator()
    print(label)
    print(value)


class LinearPlot:
    """
    A class that holds everthing required for a linear plot.
    Includes:
     - Linear regression fit (includes y-intercept and gradient)
     - Chi-squared of the linear regression fit
     -
    """

    chi2 = None
    gradient_of_fit = None
    y_intercept_of_fit = None
    plot = None

    x_label = ""
    y_label = ""
    title = ""

    include_best_fit = False
    include_residual_plot = False

    vertical_marker = None
    horizontal_marker = None

    def __init__(self, xs, ys):
        """
        Init from either two 2 elements wide column np.arrays
        or if either are only 1 element wide, the uncertainty is taken to be 0 and are added.
        Parameters
        ----------
        xs : Column
        ys : Column
        """
        self.xs = xs
        self.ys = ys

        self.gradient_of_fit, self.y_intercept_of_fit = self.calculate_linear_fit_with_uncertainty()
        self.chi2, self.reduced_chi2 = self.calculate_chi2()
        print_value('grad = ', self.gradient_of_fit.to_string())
        print_value('intercept = ', self.y_intercept_of_fit.to_string())

    def calculate_chi2_old(self):
        """
        Calculates the chi-squared of a linear fit
        :return: chi2 and the reduced chi2
        """
        x_values = self.xs.values
        y_values = self.ys.values
        errors = self.ys.uncertainties
        weight_of_each_point = self.calculate_weight_of_each_point(errors)
        number_of_parameters = 2
        order = 1
        fitted_structure = np.polyfit(x_values, y_values, order, cov=True, w=weight_of_each_point)
        degrees_of_freedom = len(x_values) - number_of_parameters

        chisqrd = 0
        p = fitted_structure[0]

        print_separator()
        print_separator()
        print()
        print(errors)
        print_separator()
        print_separator()
        print_separator()

        for i, j, k in zip(x_values, y_values, errors):
            c = pow(((j - np.polyval(p, i)) / k), 2)
            chisqrd += c

        reduced_chi2 = chisqrd / degrees_of_freedom

        return chisqrd, reduced_chi2

    def calculate_chi2(self):
        """
        Calculates the chi-squared of a linear fit
        :return: chi2 and the reduced chi2
        """
        x_values = self.xs.values
        y_values = self.ys.values
        errors = self.ys.uncertainties
        # weight_of_each_point = self.calculate_weight_of_each_point(errors)
        number_of_parameters = 2
        # order = 1
        # fitted_structure = np.polyfit(x_values, y_values, order, cov=True, w=weight_of_each_point)
        degrees_of_freedom = len(x_values) - number_of_parameters

        chisqrd = 0
        # p = fitted_structure[0]

        for x, y, e in zip(x_values, y_values, errors):
            c = pow(((y - (x * self.gradient_of_fit.value + self.y_intercept_of_fit.value)) / e), 2)
            chisqrd += c

        reduced_chi2 = chisqrd / degrees_of_freedom

        return chisqrd, reduced_chi2

    def calculate_weight_of_each_point(self, errors):
        weight_of_each_point = []

        if min(errors) > 0:
            for error in errors:
                weight_of_each_point.append(1 / error)
        return weight_of_each_point

    def calculate_residuals(self):
        """
        Calculates the residuals of the already calculated linear fit, returns the x values and a column of the residuals
        :return: Array of x values and an Array of residuals
        """
        residuals = []
        for i in range(len(self.xs.values)):
            current_x = self.xs.to_measurements()[i]
            bestfit_y = (self.gradient_of_fit * current_x) + self.y_intercept_of_fit

            residual = self.ys.values[i] - bestfit_y.value
            residuals.append(residual)
        return self.xs.values, residuals

    def calculate_linear_fit_without_uncertainty(self):
        """
        Calculates the linear fit, returns the gradient and y-intercept values without uncertainties
        Returns
        ----------
        gradient: []
        y-intercept: []
        """
        x_values = self.xs.values
        y_values = self.ys.values

        gradient = self.calculate_gradient_without_uncertainty()

        average_x = sum(x_values) / len(x_values)
        average_y = sum(y_values) / len(y_values)

        y_intercept = average_y - (gradient * average_x)

        return Measurement(gradient, 0), Measurement(y_intercept, 0)
        # return [gradient, 0], [y_intercept, 0]

    def calculate_gradient_without_uncertainty(self):
        """
        Calculates and returns the gradient
        Returns
        ----------
        gradient: float
        """
        x_values = self.xs.values
        y_values = self.ys.values

        print_value("x_values", x_values)
        print_value("y_values", y_values)

        average_x = sum(x_values) / len(x_values)
        average_y = sum(y_values) / len(y_values)

        xy_values = x_values * y_values
        average_xy = sum(xy_values) / len(xy_values)

        x_squared_values = pow(x_values, 2)
        average_squared_x = sum(x_squared_values) / len(x_squared_values)

        gradient = ((average_x * average_y) - average_xy) / (pow(average_x, 2) - average_squared_x)
        return gradient

    def calculate_linear_fit_with_uncertainty(self):
        """
        Calculates the linear fit, returns the gradient and y-intercept values with uncertainties
        Returns
        ----------
        gradient: Measurement
        y-intercept: Measurement
        """
        xs = self.xs.to_measurements()
        ys = self.ys.to_measurements()

        print_separator()
        print_separator()
        print_separator()
        print_value('xs and ys', xs)
        for x, y in zip(xs, ys):
            print(x.to_string(), y.to_string())
        print_separator()
        print_separator()
        print_separator()

        gradient = self.calc_gradient_with_uncertainty()

        average_x = self.average_measurements(xs)
        average_y = self.average_measurements(ys)

        y_intercept = average_y - (gradient * average_x)

        return gradient, y_intercept

    # solve for m and c
    def best_linear_fit(self, x_col, y_col):
        """
        Generates m and c of the best fit line
        Parameters
        ----------
        x_col : Column
        y_col : Column
        ----------
        """

        x_col = x_col.to_measurements()
        y_col = y_col.to_measurements()

        total_x = Measurement(0, 0)
        for x in x_col:
            total_x += x
        average_x = total_x / Measurement(len(x_col), 0)
        total_y = Measurement(0, 0)
        for y in y_col:
            total_y += y
        average_y = total_y / Measurement(len(y_col), 0)

        total_xy = Measurement(0, 0)
        for x, y in zip(x_col, y_col):
            total_xy += x * y
        average_xy = total_xy / Measurement(len(x_col), 0)

        total_x_2 = Measurement(0, 0)
        for x in x_col:
            total_x_2 += x * x
        average_x_2 = total_x_2 / Measurement(len(x_col), 0)

        gradient = ((average_x * average_y) - average_xy) / ((average_x * average_x) - average_x_2)

        y_intercept = average_y - gradient * average_x

        print('best fit line:\ny = {:} + {:}x'.format(y_intercept.to_string(), gradient.to_string()))
        return y_intercept, gradient

    # def calc_gradient_with_uncertainty(self):
    #     """
    #     Calculates and return the gradient of the linear fit
    #     Returns
    #     ----------
    #     gradient : Measurement
    #     """
    #     xs = self.xs.to_measurements()
    #     ys = self.ys.to_measurements()
    #
    #     x_sum = self.sum_measurements(xs)
    #     y_sum = self.sum_measurements(ys)
    #
    #     average_x = x_sum.divide_by_value(len(xs))
    #     average_y = y_sum.divide_by_value(len(ys))
    #
    #     xys = self.multiply_two_measurement_arrays(xs, ys)
    #     xys_sum = self.sum_measurements(xys)
    #     average_xy = xys_sum.divide_by_value(len(xys))
    #
    #     x_squared = self.multiply_two_measurement_arrays(xs, xs)
    #     x_squared_sum = self.sum_measurements(x_squared)
    #     average_x_squared = x_squared_sum.divide_by_value(len(x_squared))
    #
    #     gradient = ((average_x * average_y) - average_xy) / ((average_x * average_x) - average_x_squared)
    #     return gradient

    def calc_gradient_with_uncertainty(self):
        """
        Calculates and return the gradient of the linear fit
        Returns
        ----------
        gradient : Measurement
        """
        xs = self.xs.to_measurements()
        ys = self.ys.to_measurements()

        xys = self.multiply_two_measurement_arrays(xs, ys)
        x2s = self.multiply_two_measurement_arrays(xs, xs)

        average_x = self.average_measurements(xs)
        average_y = self.average_measurements(ys)

        average_xys = self.average_measurements(xys)
        average_x2s = self.average_measurements(x2s)

        numerator = (average_x * average_y) - average_xys
        denomenator = (average_x * average_x) - average_x2s

        gradient = numerator / denomenator

        return gradient

    def sum_measurements(self, measurements):
        """
        Returns the sum of the array of measrements in the form of a measurement
        Parameters
        ----------
        measurements: [Measurements]
        Returns
        ----------
        total: Measurement
        """
        total = Measurement(0, 0)
        for m in measurements:
            total += m
        return total

    def average_measurements(self, measurements):
        """
        Returns average of the array of measurements
        Parameters
        ----------
        measurements: [Measurements]
        Returns
        ----------
        average: Measurement
        """
        sum_m = self.sum_measurements(measurements)
        return sum_m.divide_by_value(len(measurements))

    def multiply_two_measurement_arrays(self, xs, ys):
        """
        Returns a new array of tow measurement arrays multiplied together
        Parameters
        ----------
        xs: [Measurements]
        ys: [Measurements]
        Returns
        ----------
        new: Array(Measurements)
        """
        ms = []
        for x, y in zip(xs, ys):
            print(x, y)
            if x.value == 0:
                x.value = pow(10, -5)
            m = x * y
            ms.append(m)
        return ms

    def display_plot(self):
        """
        Displays the generated plot with ot without residuals
        """
        if self.include_residual_plot:
            self.display_plot_with_residuals()
        else:
            self.display_plot_without_residuals()

    def calculate_linear_fit(self):
        """
        Calculates the linear regression fit and returns the gradient and y-intercept
        Returns
        ----------
        gradient : Measurement
        y-intercept : Measurement
        """
        gradient = self.calculate_gradient()

    def calculate_gradient(self):
        """
        Calculates and returns the linear regression fit gradient
        Returns
        ----------
        gradient : Measurement
        """

    def display_plot_with_residuals(self):
        """
        Generates plot with residuals
        :return:
        """
        m, c = self.calculate_linear_fit_with_uncertainty()

        print_separator()
        print(m.value, c.to_string())
        print_separator()

        print_value("m", m.value)
        print_value('c', c.value)

        y_best_fit_vals = []
        for x in self.xs.values:
            y = c.value + m.value * x
            y_best_fit_vals.append(y)

        print_value('bestfit vals y = ', y_best_fit_vals)

        # Create Overall Plot figure
        plt.figure(figsize=(10, 9))
        gs = gridspec.GridSpec(2, 1, height_ratios=[6, 1])
        # Main sub plot
        plt.subplot(gs[0])
        plt.title(self.title)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)

        plt.errorbar(self.xs.values, self.ys.values, self.ys.uncertainties, fmt='kx')

        plt.plot(self.xs.values, y_best_fit_vals, 'b')
        plt.annotate('y = ({:.4f} ± {:.4f})x + ({:.4f} ± {:.4f}),'.format(m.value, m.uncertainty, c.value, c.uncertainty), (0, 0), (0, -40),
                     xycoords='axes fraction', textcoords='offset points',
                     va='top')

        plt.annotate('chi2 = {:.4f},'.format(self.chi2), (0, 0), (0, -60),
                     xycoords='axes fraction', textcoords='offset points',
                     va='top')
        plt.annotate('reduced chi2 = {:.4f}'.format(self.reduced_chi2), (0, 0), (160, -60),
                     xycoords='axes fraction', textcoords='offset points',
                     va='top')

        # Residual Sub-plot
        plt.subplot(gs[1])

        x_values, y_residual_values = self.calculate_residuals()
        plt.title('Residuals in ')
        plt.errorbar(x_values, y_residual_values, yerr=self.ys.uncertainties, fmt='kx')
        min_x = min(self.xs.values)
        max_x = max(self.xs.values)
        plt.plot([min_x, max_x], [0, 0])

        if self.vertical_marker is not None:
            min_y = min(self.ys.values)
            max_y = max(self.ys.values)
            plt.plot([self.vertical_marker, self.vertical_marker], [min_y, max_y])

        if self.horizontal_marker is not None:
            min_x = min(self.xs.values)
            max_x = max(self.xs.values)
            plt.plot([min_x, max_x], [self.horizontal_marker, self.horizontal_marker])

        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title('Residuals in {}'.format(self.y_label))

        plt.tight_layout()
        self.plot = plt
        # plt.show()

    def display_plot_without_residuals(self):
        """
        Generates plot without residuals
        :return:
        """
        m, c = self.calculate_linear_fit_with_uncertainty()
        y_best_fit_vals = [c.value + m.value * xi for xi in self.xs.values]

        plt.errorbar(self.xs.values, self.ys.values, self.ys.uncertainties, fmt='kx')

        if self.include_best_fit:
            plt.plot(self.xs.values, y_best_fit_vals, 'b')
            plt.annotate('y = ({:.4f} ± {:.4f})x + ({:.4f} ± {:.4f}),'.format(m.value, m.uncertainty, c.value, c.uncertainty), (0, 0), (0, -40),
                         xycoords='axes fraction', textcoords='offset points',
                         va='top')

            plt.annotate('chi2 = {:.4f},'.format(self.chi2), (0, 0), (0, -60),
                         xycoords='axes fraction', textcoords='offset points',
                         va='top')
            plt.annotate('reduced chi2 = {:.4f}'.format(self.reduced_chi2), (0, 0), (160, -60),
                         xycoords='axes fraction', textcoords='offset points',
                         va='top')

        if self.vertical_marker is not None:
            min_y = min(self.ys.values)
            max_y = max(self.ys.values)
            plt.plot([self.vertical_marker, self.vertical_marker], [min_y, max_y])

        if self.horizontal_marker is not None:
            min_x = min(self.xs.values)
            max_x = max(self.xs.values)
            plt.plot([min_x, max_x], [self.horizontal_marker, self.horizontal_marker])

        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self.title)

        self.plot = plt
        plt.show()

    def show(self):
        self.plot.show()

    def save_plot(self, filepath, ppi=300):
        """
        Saves the produced plot.
        :return:
        """
        self.plot.savefig(filepath, ppi=ppi)

    def product_moment_correlation_coefficient(self):
        """
        Calculates and returns the product moment coefficient (r) (a measure of how linearly correlated the data is)
        Parameters
        ----------
        self : LinearPlot
        Returns
        ----------
        r : float
        """
        xs = self.xs.values
        ys = self.ys.values

        S_xy = self.calculate_s_xy(xs, ys)
        S_xx = self.calculate_s_xy(xs, xs)
        S_yy = self.calculate_s_xy(ys, ys)

        r = S_xy / pow(S_xx * S_yy, 0.5)
        return r

    def calculate_s_xy(self, xs, ys):
        """
        Calculates and returns S_xy
        Parameters
        ----------
        xs: float
        ys: float
        Returns
        ----------
        s : float
        """
        s = 0.0
        average_x = sum(xs) / len(xs)
        average_y = sum(ys) / len(ys)

        for x, y in zip(xs, ys):
            s += (x - average_x) * (y - average_y)

        return s
