import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from detailedDesign.carrotPlot import make_carrot_plot
from detailedDesign.stability import get_xplot
from detailedDesign.log import setup_custom_logger


def find_stability(aircraft):
    logger = setup_custom_logger('logger', True)
    df = make_carrot_plot(force_run=False)
    f_stab, f_cont, Xcg = get_xplot(aircraft)

    plt.plot(Xcg, f_stab(Xcg), '-k')
    plt.plot(Xcg, f_cont(Xcg), '-k')
    plt.xlabel("xcg/c")
    plt.ylabel("Sh/S")
    plt.ylim(ymin=0)
    plt.grid()
    plt.title("X-plot")

    y_min = 1e6
    z_min = None
    # For every row in the dataframe we try to find the Sh/S value, we then find the minimum Sh/S
    for row in np.array(df):
        logger.debug(row)
        
        # Get x_lemac/l_fus
        z = row[1]
        # Get the position as %mac
        x1 = row[2]
        x2 = row[3]
        # Find the Sh/S
        y1 = f_cont(row[2])
        y2 = f_stab(row[3])

        # Find the highest point as it otherwise crosses the scissor plot
        if y1 > y2:
            y = y1
        else:
            y = y2

        # Find the minimum value for Sh/S and Xlemac/Lfus
        if y < y_min:
            y_min = y
            z_min = z

        # Plot the different lines from the carrot plot inside the scissor plot
        plt.plot([x1, x2], [y, y], "--", label=f'LE pos at MAC: {row[4]}, MTOM = {row[5]/1e3:.2f} [ton], Drag: {row[5]/1e6} [kN]')
        print(y)

    plt.savefig(Path('plots', 'scissor'))
    plt.legend()
    plt.show()
    print(f"Best Sh/S: {y_min}, best Xlemac/Lfus: {z_min}")
    print(f"Horizontal tail area should be {y_min * aircraft.WingGroup.Wing.wing_area} [m2].")
    print(f"Xlemac should be placed at {z_min * aircraft.FuselageGroup.Fuselage.length} [m].")
