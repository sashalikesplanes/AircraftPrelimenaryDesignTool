from fileinput import filename
from tqdm import tqdm

import matplotlib.pyplot as plt
import matplotlib
from scipy.optimize import minimize, Bounds
from conceptualDesign.conceptualDesign import conceptualDesign
from misc.openData import openData
from misc.materials import load_materials
import numpy as np
plt.rcParams.update({'font.size': 2})


def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    row_labels
        A list or array of length N with the labels for the rows.
    col_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=["black", "white"],
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A list or array of two color specifications.  The first is used for
        values below a threshold, the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts


def func_to_optimize(params, iters, velocity, compressionRatio, range):
    altitude = params[0]
    material_data: dict = load_materials()

    parameters = openData("design1")

    parameters['altitude'] = altitude
    parameters['compressionRatio'] = compressionRatio
    parameters['velocity'] = velocity
    parameters["flightRange"] = range
    conceptualDesign(parameters, material_data, iters)
    return parameters['fuelMass']


def graph_stuff(compressionRatio, steps, speedStart, speedEnd, rangeStart, rangeEnd, figName):
    # altitude = 5000
    # X = np.array([[2], [1000]])  # compressionratio --> 50 steps
    # Y = np.array([[25], [200]])  # velocity --> 100 steps

    x = np.linspace(speedStart, speedEnd, num=steps)  # velocity
    y = np.linspace(rangeStart, rangeEnd, num=steps)  # range
    material_data: dict = load_materials()

    matrix = np.zeros((len(x), len(y)))

    for index_i, velocity in enumerate(x):
        for index_j, range in enumerate(y):
            bnds = [(1000, 10999)]  # height, CR, speed
            altitude = minimize(func_to_optimize, (1001,),
                                args=(10, velocity, compressionRatio, range), bounds=bnds, method="SLSQP").x[0]
            print(range, velocity, altitude)
            params = openData("design1")
            # print(f"Hello world! {i} {j}")
            params['compressionRatio'] = compressionRatio
            params['altitude'] = altitude
            params['velocity'] = velocity
            params["flightRange"] = range

            _, result = conceptualDesign(params, material_data, 1000)
            variable = result["fuelMass"]
            matrix[index_i, index_j] = variable.iloc[-1] / range
            # print(variable.iloc[-1])

    print(np.count_nonzero(np.isnan(matrix)))
    # x = np.linspace(speedStart, speedEnd, num=steps+1)  # compression ratio
    # y = np.linspace(1e6, 10e6, num=steps+1)  # velocity

    # matrix = np.log(matrix)

    fig, ax = plt.subplots()

    im, cbar = heatmap(matrix * 1000, x, y, ax=ax,
                       cmap="YlGn", cbarlabel="fuel consumption [g/m]")
    texts = annotate_heatmap(im, valfmt="{x:.1f} g/m")

    fig.tight_layout()
    plt.savefig(figName, dpi=1000)
    np.save(f"{figName}_data", matrix * 100)
    # plt.pcolormesh(y, x, matrix)
    # plt.show()


if __name__ == "__main__":

    # graph_stuff(altitude=10000, compressionRatio=5,
    #             steps=20, speedStart=50, speedEnd=200, rangeStart=5e6, rangeEnd=20e6, figName="FeasibilityCR5")
    # Constrained: Ballon Structure - 2x, Drag - 1.5x, Fuel - 1.2 x
    # Low Constrain: Balloon - 1.25x, Drag - 1.1x, Fuel - 1.05x
    graph_stuff(compressionRatio=8,
                steps=26, speedStart=50, speedEnd=200, rangeStart=1e6, rangeEnd=11e6, figName="FeasibilityCR8ConstrainAltitudeOptimized")
    graph_stuff(compressionRatio=9,
                steps=26, speedStart=50, speedEnd=200, rangeStart=1e6, rangeEnd=11e6,
                figName="FeasibilityCR9ConstrainAltitudeOptimized")
