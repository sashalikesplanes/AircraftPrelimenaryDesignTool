# Physical Constants
g = 9.80665  # m/s^2
R_air = 287  # air gas constant [m^2/s^2/K]
R_h2 = 4157.2  # h2 gas constant
R = 8.31446261815324  # ideal gas constant [J/k/mol]
testMargin = 0.03  # [-] fraction of the margin that a unit_test can be wrong without being wrong
# https://rmi.org/run-on-less-with-hydrogen-fuel-cells/#:~:text=In%20electrical%20terms%2C%20the%20energy,as%20a%20gallon%20of%20diesel.
energyDensityHydrogen = 33.6e3 * 60 * 60  # [J/kg]
Xtrovercfus = 0.0   #transition location
Xtrovercwing = 0.35 #transition location

# Yes I know this shouldn't be here, but it is.
mass_per_passenger = 120  # [kg]
# Percentage of the passenger mass which shall be stored in the cargo bay
cargo_cabin_fraction = 0.75  # [kg]

# Safety margin for potato plot
safety_margin = 0.02
