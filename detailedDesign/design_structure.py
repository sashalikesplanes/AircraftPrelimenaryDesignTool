import numpy as np

from detailedDesign.bending_shear import find_bending_shear


def design_structure(aircraft):
    design_fuselage(aircraft)


def design_fuselage(aircraft):
    find_bending_shear(aircraft)
