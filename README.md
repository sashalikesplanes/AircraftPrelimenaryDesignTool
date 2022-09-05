# AE3200DSE - Aircraft Prelimenary Design Tool

This tool is designed to allow the team to quickly iterate on the chosen design of the Aircraft.

The tool works by specifying all of the systems of the Aircraft as individual classes. These classes have design constraints specified in code. The constraints may be interrelated to the other systems. The tool iteratively updates the design parameters of each system, so that all constraints would be satisfied. The iteration is checked for convergence and halted if it converges or diverges, producing the final outputs. From the final outputs additional outputs, which would not affect the iteration process, are calculated.

Tools used:
- Numpy
- Scipy
- Pandas
- Matplotlib
- PyTest
