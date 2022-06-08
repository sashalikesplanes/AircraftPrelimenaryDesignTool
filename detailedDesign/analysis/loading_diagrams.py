import numpy as np
import matplotlib.pyplot as plt

from misc.constants import g


def make_loading_diagrams(aircraft):
    fuselage_group = aircraft.FuselageGroup
    components = get_sizes_and_loads(fuselage_group)
    forces = []

    for component in components:
        if component[2] is None:
            forces.append(PointLoad(component[3], -component[1] * g))
        else:
            forces.append(DistributedLoad(component[3], -component[1] * g, component[2]))

    total_length = aircraft.FuselageGroup.Tail.transformed_pos[0]
    # Lift force
    x_lift = 30
    lift = PointLoad(aircraft.WingGroup.Wing.transformed_cg[0], aircraft.FuselageGroup.get_mass() * g)
    forces.append(lift)

    X = np.arange(0, total_length, 0.1)
    shear = [sum([i.calc_shear(y) for i in forces]) for y in X]
    moment = [sum([i.calc_moment(y) for i in forces]) for y in X]
    print("Making loading diagram...")
    print(X)

    plt.title("Fuselage Loading Diagram")
    plt.plot(X, shear)


def get_sizes_and_loads(head_component):
    if hasattr(head_component, "length"):
        l = head_component.length
    else:
        l = None

    lst = [(str(head_component), head_component.own_mass, l, head_component.transformed_cg)]
    for component in head_component.components:
        lst += get_sizes_and_loads(component)
    return lst


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
