import numpy as np
import matplotlib.pyplot as plt

from misc.constants import g
from detailedDesign.board_passengers import board_passengers


def make_loading_diagrams(aircraft):
    fuselage_group = aircraft.FuselageGroup
    components = get_sizes_and_loads(fuselage_group)

    board_passengers(aircraft)
    # Initialize the bending moment due to the wing
    C_m = 0.199
    state = aircraft.states["cruise"]
    wing_area = aircraft.WingGroup.Wing.wing_area
    normalized_chord = aircraft.WingGroup.Wing.mean_geometric_chord
    moment = 0.5 * state.density * state.velocity ** 2 * wing_area * C_m * normalized_chord
    forces = [PointMoment(aircraft.WingGroup.Wing.transformed_cg, moment)]

    # Transform the components into the correct loads
    for component in components:
        if not component[0] == "Cabin":
            if component[2] is None:
                forces.append(PointLoad(component[3], -component[1] * g))
            else:
                forces.append(DistributedLoad(component[3], -component[1] * g, component[2]))
        else:
            m_pax = sum([x.mass for x in aircraft.FuselageGroup.Fuselage.Cabin.passengers])
            if component[2] is None:
                forces.append(PointLoad(component[3], -(component[1] + m_pax) * g))
            else:
                forces.append(DistributedLoad(component[3], -(component[1] + m_pax) * g, component[2]))

    # Get the maximum length to plot to
    total_length = aircraft.FuselageGroup.Tail.transformed_pos[0]

    # Lift force
    lift = PointLoad(aircraft.WingGroup.Wing.transformed_cg[0], aircraft.FuselageGroup.get_mass() * g)
    forces.append(lift)

    # Plot the forces for debugging
    plt.figure()
    [x.plot() for x in forces]
    plt.title("Forces Drawing")

    # Initialize a new figure
    plt.figure()
    fig, (ax1, ax2) = plt.subplots(2)

    # Calculate shear and bending over the longitudinal plane length
    X = np.arange(0, total_length, 0.1)
    shear = np.array([sum([i.calc_shear(y) for i in forces]) for y in X])
    moment = -np.array([sum([i.calc_moment(y) for i in forces]) for y in X])

    # Plot the bending and shear diagram
    ax1.set_title("Fuselage Shear Loading Diagram")
    ax1.set(xlabel="Longitudinal Position [m]", ylabel="Shear Force [kN]")
    ax1.plot(X, shear * 10 ** -3, color="tab:red")
    ax1.grid()
    ax2.set_title("Fuselage Bending Diagram")
    ax2.set(xlabel="Longitudinal Position [m]", ylabel="Bending Moment [kNm]")
    ax2.plot(X, moment * 10 ** -3, color="tab:green")
    ax2.grid()


def get_sizes_and_loads(head_component):
    if hasattr(head_component, "length"):
        l = head_component.length
    else:
        l = None

    if str(head_component) == "Miscellaneous":
        lst = head_component.forces_lst
        total_accounted_mass = sum([x[1] for x in lst])
        lst.append(("RemainingMisc", head_component.own_mass - total_accounted_mass, l, head_component.FuselageGroup.Fuselage.transformed_cg))
        return lst

    lst = [(str(head_component), head_component.own_mass, l, head_component.transformed_cg)]
    for component in head_component.components:
        lst += get_sizes_and_loads(component)
    return lst


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
