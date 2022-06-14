import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class PointMoment:
    def __init__(self, pos, moment):
        self.x = pos[0]
        self.moment = moment

    @staticmethod
    def calc_shear(x):
        return 0

    def calc_moment(self, x):
        if x >= self.x:
            return self.moment
        else:
            return 0

    def plot(self):
        pass


class PointLoad:
    def __init__(self, pos, force):
        if isinstance(pos, int) or isinstance(pos, np.float64):
            self.x = pos
        elif isinstance(pos, np.ndarray):
            self.x = pos[0]
        else:
            raise TypeError(f"position should be either 'int' or 'np.ndarray', currently {type(pos)}")
        self.force = force

    def calc_moment(self, x):
        if x >= self.x:
            arm = self.x - x
            return arm * self.force
        else:
            return 0

    def calc_shear(self, x):
        if x >= self.x:
            return self.force
        else:
            return 0

    def plot(self):
        plt.arrow(self.x, 0, 0, self.force, color="tab:blue")


class DistributedLoad:
    def __init__(self, pos, force, width):
        self.x = pos[0]
        self.force = force
        self.width = width

        self.force_per_meter = self.force / self.width
        half_width = self.width / 2
        self.x_left = self.x - half_width
        self.x_right = self.x + half_width

    def calc_moment(self, x):
        if x <= self.x_left:
            return 0
        elif x >= self.x_right:
            point_load = PointLoad(self.x_left + self.width / 2, self.force)
            return point_load.calc_moment(x)
        else:
            width = x - self.x_left
            force = width * self.force_per_meter
            x_point_load = self.x_left + width / 2
            point_load = PointLoad(x_point_load, force)
            return point_load.calc_moment(x)

    def calc_shear(self, x):
        if x <= self.x_left:
            return 0
        elif x >= self.x_right:
            return self.force
        else:
            width = x - self.x_left
            force = width * self.force_per_meter
            return force

    def plot(self):
        plt.arrow(self.x_left, 0, 0, self.force_per_meter, color="tab:blue")
        plt.arrow(self.x_right, 0, 0, self.force_per_meter, color="tab:blue")
        plt.arrow(self.x, 0, 0, self.force_per_meter, color="tab:blue")
        plt.plot([self.x_left, self.x_right], [0, 0], color="tab:blue")
        plt.plot([self.x_left, self.x_right], [self.force_per_meter, self.force_per_meter], color="tab:blue")


class LinearLoad:
    def __init__(self, pos, force, width):
        self.x = pos[0]
        self.force = force
        self.width = width
        self.force_max = 2 * self.force / self.width
        self.force_gradient = self.force_max / self.width

        half_width = self.width / 2
        self.x_left = self.x - half_width
        self.x_right = self.x + half_width

    def calc_shear(self, x):
        if self.x_left > x:
            return 0
        elif self.x_right < x:
            return self.force
        else:
            force_left = self.force_max - x * self.force_gradient
            force_right_leftover = self.force_max - force_left

            w_current = x - self.x_left
            force_rect = force_left * w_current
            loads = [PointLoad(self.x_left + w_current / 2, force_rect)]

            force_tri = force_right_leftover * w_current / 2
            loads.append(PointLoad(self.x_left + w_current / 3, force_tri))
            return sum([y.calc_shear(x) for y in loads])

    def calc_moment(self, x):
        if self.x_left > x:
            return 0
        elif self.x_right < x:
            arm = self.x - x
            return arm * self.force
        else:
            force_left = self.force_max - x * self.force_gradient
            force_right_leftover = self.force_max - force_left

            w_current = x - self.x_left
            force_rect = force_left * w_current
            loads = [PointLoad(self.x_left + w_current / 2, force_rect)]

            force_tri = force_right_leftover * w_current / 2
            loads.append(PointLoad(self.x_left + w_current / 3, force_tri))
            return sum([y.calc_moment(x) for y in loads])

    def plot(self):
        pass


class LiftCurve:
    def __init__(self, df_location, lift):
        self.force = lift
        self.df = pd.read_csv(df_location)
        positive = self.df["y-span"] >= 0
        self.df = self.df[positive]

        # Factor to convert from cl to L
        self.force_factor = 1
        self.cl_sum = self.calc_shear(1000)
        self.force_factor = self.force / self.cl_sum

        print(self.cl_sum)
        print(self.df)

    def calc_shear(self, x):
        running = True
        i = 0
        data_y = np.array(self.df["y-span"])
        data_l = np.array(self.df["Cl"])
        force = 0
        while running:
            if i >= len(data_l):
                running = False
            elif data_y[i] > x:
                running = False
                y_left = data_y[i-1]
                y_right = data_y[i]
                cl_left = data_l[i-1]
                cl_right = data_l[i]
                dcldy = (cl_left - cl_right)/(y_left - y_right)
                w_middle = x - y_left
                cl_middle = cl_left + w_middle * dcldy
                force += (cl_left + cl_middle) / 2 * w_middle

            elif i == 0:
                pass
            elif data_y[i] < x:
                avg_height = (data_l[i] + data_l[i-1]) / 2
                width = abs(data_y[i] - data_y[i-1])
                force += width * avg_height

                print(data_y[i])
            i += 1

        return force * self.force_factor
