import numpy as np 
import matplotlib.pyplot as plt
from pathlib import Path

def make_drag_polar(aircraft):
    alphas = np.linspace(-15,10, 100)
    C_L_s = aircraft.WingGroup.Wing.get_C_L(alphas)
    C_D_s = aircraft.C_D_min + C_L_s ** 2 / (np.pi * aircraft.WingGroup.Wing.aspect_ratio * aircraft.WingGroup.Wing.oswald)


    fig, ax = plt.subplots()
    ax.plot(C_D_s, C_L_s, color='k')
    ax.plot([min(C_D_s)-0.012, max(C_D_s)] ,[0,0], alpha=0)

    ax.spines['left'].set_position('zero')

    ax.spines['right'].set_color('none')
    ax.yaxis.tick_left()

    ax.spines['bottom'].set_position('zero')

    ax.spines['top'].set_color('none')
    ax.xaxis.tick_bottom()

    ax.set_xlabel(r'$C_D$', fontsize=20)
    ax.set_ylabel(r'$C_L$', fontsize=20)
    save_path = Path("plots", "drag_polar")
    plt.savefig(save_path, dpi=600)
    # plt.show()
    plt.close()








