import numpy as np
from detailedDesign.classes.Component import Component
from misc.ISA import getPressure


class SAD(Component):
    def __init__(self, FuselageGroup, design_config):
        super().__init__(design_config)
        self.FuselageGroup = FuselageGroup
        self.parent = self.FuselageGroup


    def bending_shear(self):
        # if (self.FuselageGroup.Fuselage.outer_height == self.FuselageGroup.Fuselage.outer_width):
        #     I_zz = np.pi/64*(self.FuselageGroup.Fuselage.outer_width**4-self.FuselageGroup.Fuselage.inner_width**4)
        #     I_yy = I_zz
        # else:

        #Initialisation
        # z = np.linspace(0, z_max, 100)
        # y = np.linspace(0, y_max, 100)
        t = np.linspace(0, 0.5, 100)
        # t = max(self.FuselageGroup.Fuselage.outer_height/2 - self.FuselageGroup.Fuselage.inner_height/2, self.FuselageGroup.Fuselage.outer_width/2 - self.FuselageGroup.Fuselage.inner_width/2)


        z_max = self.FuselageGroup.Fuselage.outer_height / 2
        z_inner = self.FuselageGroup.Fuselage.inner_height / 2
        y_max = self.FuselageGroup.Fuselage.outer_width / 2
        y_inner = self.FuselageGroup.Fuselage.inner_width / 2
        R = max(z_max, y_max)  # not really sure since it's a cylinder, maybe just take it as a contingency
        # R_inner = max(self.FuselageGroup.Fuselage.inner_width / 2, self.FuselageGroup.Fuselage.inner_height / 2)



        #inertia thin walled oval
        area = 0.25*np.pi*(self.FuselageGroup.Fuselage.outer_height*self.FuselageGroup.Fuselage.outer_width-self.FuselageGroup.Fuselage.inner_height*self.FuselageGroup.Fuselage.inner_width)
        I_zz = (np.pi*(self.FuselageGroup.Fuselage.outer_height*self.FuselageGroup.Fuselage.outer_width**3 - self.FuselageGroup.Fuselage.inner_height*self.FuselageGroup.Fuselage.inner_width**3))/64
        I_yy = (np.pi*(self.FuselageGroup.Fuselage.outer_height**3*self.FuselageGroup.Fuselage.outer_width - self.FuselageGroup.Fuselage.inner_height**3*self.FuselageGroup.Fuselage.inner_width))/64
        J_0 = I_zz+I_yy

        #first moment of area <-hopefully correct
        Q_outer_z = 0.25*np.pi*z_max*y_max**3
        Q_outer_y = 0.25 * np.pi * z_max**3 * y_max
        Q_inner_z = 0.25 * np.pi * z_inner * y_inner ** 3
        Q_inner_y = 0.25 * np.pi * z_inner ** 3 * y_inner
        Q_z = Q_outer_z - Q_inner_z
        Q_y = Q_outer_y - Q_inner_y


        delta_P = np.abs(getPressure(aircraft.states[test_state].altitude)-getPressure(0))

        M_z = 0
        M_y = 0
        #loading in y-/z-axis
        S_y = 0
        S_z = 0
        T = 0


        #Stress calculations
        sigma_x = []
        sigma_y = []
        tau = []
        tau_max =[]
        sigma_1 = []
        sigma_2 = []

        for i in range(len(t)):
            sigma_x.append(M_z*y/I_zz + M_y*z/I_yy + 2*delta_P*R/(2*t[i]))
            sigma_y.append(2*delta_P*R/t[i])

            # sigma_x = M_z*y/I_zz + M_y*z/I_yy + 2*delta_P*R/(2*t)
            # sigma_y = 2*delta_P*R/t

            tau.append(-(S_y*Q_z)/(I_zz*t[i])-(S_z*Q_y)/(I_yy*t[i])+T*R/J_0)


            tau_max.append(np.sqrt(((sigma_z-sigma_y)/2)**2+tau**2))

            sigma_1.append((sigma_z[i]+sigma_y[i])/2+tau_max[i])
            sigma_2.append((sigma_z[i]+sigma_y[i])/2-tau_max[i])

        print(sigma_y)






