from main_conceptual import run_concept
from conceptualDesign.dragModel import dragModel as model_drag
from conceptualDesign.dragModel import get_drag as get_cd
from misc.openData import openData
from misc.ISA import getDensity
import numpy as np


if __name__ == "__main__":
    parameters = openData("design1")

 #   run_concept(parameters)
    # A380 with Hindenberg
    print(' --- --- A380 --- ---')
    print('plane: actual C_D = 0.0265')
    rho = getDensity(parameters['altitude'])
    rho = 0.66
    temp = 249.15
    parameters['velocity'] = 200
    parameters['balloonLength'] = 0
    parameters['balloonVolume'] = 0 
    parameters['wingArea'] = 843
    parameters['wingQuarterChordSweep'] = np.deg2rad(33.5)
    parameters['fuselageLength'] = 73
    parameters['fuselageRadius'] = 12/2
    parameters['wingAspectRatio'] = 7.5
    parameters['wingC_L_design'] = 0.5
    parameters['designConcept'] = 4
    AR = 7.5 
    span = np.sqrt(parameters["wingArea"] * AR)
    rootChord = 2 * parameters["wingArea"] / ( span * (1 + parameters["wingTaperRatio"]))
    MAC = 2 / 3 * rootChord * (1 + parameters["wingTaperRatio"] + \
            parameters["wingTaperRatio"] ** 2)/(1 + parameters["wingTaperRatio"])
    parameters['meanAerodynamicChord'] = MAC
    parameters['balloonRadius'] = 35/2
    drag = model_drag(parameters, rho, temp)
    cd = get_cd(parameters, rho, temp)
    print(cd, parameters['fuelMass'], parameters["balloonVolume"],
          parameters["balloonRadius"], parameters["balloonLength"], parameters['totalDrag'])

    # print('blimp')
    # drag = model_drag(parameters, rho, temp, designConcept=3)
    # print(parameters['fuelMass'], parameters["balloonVolume"],
    #       parameters["balloonRadius"], parameters["balloonLength"], parameters['totalDrag'])
    


 
