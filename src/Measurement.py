
class Measurement:

    def __init__(self, value, uncertainty):
        self.value = value
        self.uncertainty = uncertainty

    def __add__(self, other):
        if type(self) == type(other):
            return self.add(other)
        else:
            other_value = Measurement(other, 0)
            return self.add(other_value)

    def __sub__(self, other):
        new_value = self.value - other.value
        new_uncert = self.add_uncertainty(other)
        return Measurement(new_value, new_uncert)

    def __mul__(self, other):
        new_value = self.value * other.value
        new_uncert = self.multiply_uncertainty(other, new_value)
        return Measurement(new_value, new_uncert)

    def __truediv__(self, other):
        if other.value == 0:
            print('_-------------------------')
            print('_-------------------------')
            print('_-------------------------')
            print('_-------------------------')
            print('_-------------------------')
            print('_-------------------------')
            print('_-------------------------')
            print('_-------------------------')
            print("ERRRRRROOOORRRR")

        new_value = self.value / other.value
        new_uncert = self.multiply_uncertainty(other, new_value)
        return Measurement(new_value, new_uncert)

    def add(self, other):
        new_value = self.value + other.value
        new_uncert = self.add_uncertainty(other)
        return Measurement(new_value, new_uncert)

    def divide_by_value(self, value):
        other_measurement = Measurement(value, 0)
        new_measurement = self / other_measurement
        return new_measurement

    def add_uncertainty(self, other):
        return pow((self.uncertainty * self.uncertainty) + (other.uncertainty * other.uncertainty), 0.5)

    def multiply_uncertainty(self, other, new_value):
        if other.value == 0:
            other.value = pow(10, -10)
        if new_value == 0:
            new_value = pow(10, -10)

        return pow(pow(self.uncertainty / self.value, 2) + pow(other.uncertainty / other.value, 2), 0.5) * abs(new_value)

    def __print__(self):
        return str(self.value) + "±" + str(self.uncertainty)

    def to_string(self):
        """
        Generates a string representing all the values and uncertainties in the column
        :return:
        """
        return "{:.3f} ± {:.3f}".format(self.value, self.uncertainty)

