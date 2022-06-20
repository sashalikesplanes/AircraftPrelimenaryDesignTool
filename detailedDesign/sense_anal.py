import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from detailedDesign.classes.Aircraft import Aircraft
from detailedDesign.classes.State import State
from misc.openData import openData
from detailedDesign.getConstraints import get_constraints
from detailedDesign.historicalRelations import get_MTOM_from_historical_relations
from pathlib import Path
from detailedDesign.log import setup_custom_logger
from detailedDesign.analysis.marketEstimations import market_estimations, production_cost_estimation, operations_and_logistics
from dataclasses import dataclass

plt.rcParams.update({'font.size': 16})

# Key parameters:
    # oem
    # fuel_mass
    # DOC / ASK

# Key inputs
    # Velocity
    # Range
    # N pax
    # OEM Contingency
    # Cruise Drag contingency

# Get the default config

logger = setup_custom_logger("logger", False)

def run_one_param(param_values, param_updater, out_names):

    out_arr = np.empty((len(param_values), len(out_names)))

    for i, param_value in enumerate(param_values):
        states = {"cruise": State('cruise'), "take-off": State('take-off')}
        config = openData(Path('data', 'new_designs', 'config.yaml'))
        states, config = param_updater(param_value, states, config)
        
        outs = run_aircraft(config, states)
        out_arr[i] = [outs[name] for name in out_names]


    out_arr = np.apply_along_axis(lambda col: col / col[1], 0, out_arr)
    return (np.delete(out_arr, 1, 0) - 1), outs['C_m_alpha [-]']
        

    # normalize out array


    return out_arr


def param_updater_velocity(velocity, states, config):
    states['cruise'].velocity = velocity
    return states, config

def param_updater_range(range_, states, config):
    states['cruise'].range = range_
    return states, config

def param_updater_pax(pax, states, config):
    config["Aircraft"]['FuselageGroup']['Fuselage']['Cabin']['passenger_count'] = pax
    return states, config

def param_updater_oem(oem, states, config):
    config["Aircraft"]['oem_contingency'] = oem
    return states, config

def param_updater_drag(drag, states, config):
    config['Aircraft']['cruise_drag_contingency'] = drag
    return states, config

def param_updater_power(power, states, config):
    config['Aircraft']['WingGroup']['Engines']['engine_failure_contingency'] = power
    return states, config

def param_updater_fc_power(spec_power, states, config):
    config['Aircraft']['FuselageGroup']['Power']['FuelCells']['mass_power_density'] = spec_power
    return states, config

def param_updater_ar(ar, states, config):
    config['Aircraft']['WingGroup']['Wing']['aspect_ratio'] = ar
    return states, config

def param_updater_tr(tr, states, config):
    config['Aircraft']['WingGroup']['Wing']['taper_ratio'] = tr
    return states, config

def param_updater_volume_coef(vc, states, config):
    config['Aircraft']['FuselageGroup']['Tail']['HorizontalTail']['volume_coefficient'] = vc
    return states, config

def param_updater_tail_ar(tr, states, config):
    config['Aircraft']['FuselageGroup']['Tail']['HorizontalTail']['taper'] = tr
    return states, config

def param_updater_tail_length(tl, states, config):
    config['Aircraft']['FuselageGroup']['Fuselage']['tail_length_factor'] = tl
    return states, config

def param_updater_xlemac(xl, states, config):
    config['Aircraft']['x_lemac'] = xl
    return states, config

class Parameter:
    def __init__(self, name, values, updater):
        self.name = name
        self.values = values
        self.updater = staticmethod(updater)


param_velocity = Parameter('Velocity', [198, 200, 202], param_updater_velocity)
param_drag = Parameter('Drag Contingency', [0.99, 1.0, 1.01], param_updater_drag)
param_oem = Parameter('OEM Contingency', [1.0395, 1.05, 1.0605], param_updater_oem)

params_ac = [param_velocity, param_oem,
             Parameter('Range', [7920e3, 8000e3, 8080e3], param_updater_range),
             Parameter('N Pax', [1485, 1500, 1515], param_updater_pax),
             param_drag]


out_names_ac = ['OEM [kg]', 'Fuel Mass [kg]', 'DOC/ASK [$/pax/km]']

params_eng = [param_velocity, param_drag,
              Parameter('Fuel Cell Specific Power', [7920, 8000, 8080], param_updater_fc_power),
              Parameter('Power Contingency', [1.287, 1.3, 1.313], param_updater_power)]

out_names_eng = ['Num of Fans [-]', 'P&P mass [kg]', 'Fuel Mass [kg]']

params_wing = [param_velocity, param_drag, param_oem, 
               Parameter('Aspect Ratio [-]', [7.92, 8.0, 8.08], param_updater_ar),
               Parameter('Taper Ratio [-]', [0.84348, 0.852, 0.86052], param_updater_tr)]

out_names_wing = ['Wing Area [m^2]', 'Wing Mass [kg]', 'Installation Angle [deg]']

# Tail mass, C_M_alpha, H_Tail area

# Volume volume coefficient, aspect ratio, tail_length_factor, x_lemac
params_tail = [param_velocity,  
               Parameter('H Tail Volume Coefficient [-]', [1.485, 1.5, 1.515], param_updater_volume_coef),
               Parameter('H Tail Aspect Ratio [-]', [3.96, 4, 4.04], param_updater_tail_ar),
               Parameter('Tailcone Length [m]', [2.2275, 2.25, 2.2725], param_updater_tail_length),
               Parameter('X position LEMAC [m]', [55.935, 56.5, 57.065], param_updater_xlemac)]

out_names_tail = ['Empennage Mass [kg]', 'H Tail Area [m^2]']

def main():
    plot_anal('aircraft', out_names_ac, params_ac)
    plot_anal('power_and_prop', out_names_eng, params_eng)
    plot_anal('wing', out_names_wing, params_wing)
    plot_anal_tail('tail', out_names_tail, params_tail)

def plot_anal_tail(sys_name, out_names, params):
    states = {"cruise": State('cruise'), "take-off": State('take-off')}
    config = openData(Path('data', 'new_designs', 'config.yaml'))
    clean_c_m_alpha = run_aircraft(config, states)['C_m_alpha [-]']
    c_m_alphas = []

    out_arrs = []
    for param in params:
        outs, c_m_alpha = run_one_param(param.values, param.updater, out_names)
        out_arrs.append(outs)
        c_m_alphas.append(c_m_alpha)

    out_arrs = np.stack(out_arrs, axis=2)

    fig, ax = plt.subplots()
    fig.set_size_inches(12, 8)
    plt.grid()

    x_locs = np.linspace(0, 10, len(params))
    width = 0.7
    ax.axhline(0, color='grey')
    hatch_list = ['//', 'oo', '\\\\']

    for i, _ in enumerate(out_names):
        outs_pos = out_arrs[1, i, :]

        up_bars = ax.bar(x_locs + (i - 1) * width,
                         outs_pos,
                         width - 0.05,
                         label=f"Change in {out_names[i]} due to +1% of parameter",
                         color='none',
                         hatch=hatch_list[i],
                         edgecolor=(0, 0, 0, 1.0),
                         zorder=10)

        ax.bar_label(up_bars, padding=3, labels=['{:,.2%}'.format(x) for x in outs_pos])

    ax2 = ax.twinx()
    x_locs = np.hstack([-x_locs[1], x_locs])
    ax2.set_ylabel(r"$C_{m_{\alpha}}$")
    up_bars = ax2.bar(x_locs + width,
                     [clean_c_m_alpha] + c_m_alphas,
                     width - 0.05,
                     label=r"$C_{m_{\alpha}}$",
                     color='none',
                     hatch=hatch_list[-1],
                     edgecolor=(0, 0, 0, 1.0),
                     zorder=10)

    ax2.bar_label(up_bars, padding=3, labels=['{:,.2f}'.format(x) for x in [clean_c_m_alpha] + c_m_alphas])
    ax2.set_ylim(bottom=-0.08)
    align_yaxis(ax, ax2)


    ax.set_yticklabels(['{:,.2%}'.format(x) for x in ax.get_yticks()])
    ax.set_ylabel(f"% Change in {', '.join(out_names)} relative to baseline")
    labels = ['Baseline'] + [param.name for param in params] 
    ax.set_xticks(x_locs, labels)
    ax.set_xlabel('Parameter varied')
    ax.legend()
    ax2.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig(Path('plots', f"sense_anal_{sys_name}.pdf"))

def align_yaxis(ax1, ax2):
    """Align zeros of the two axes, zooming them out by same ratio"""
    axes = (ax1, ax2)
    extrema = [ax.get_ylim() for ax in axes]
    tops = [extr[1] / (extr[1] - extr[0]) for extr in extrema]
    # Ensure that plots (intervals) are ordered bottom to top:
    if tops[0] > tops[1]:
        axes, extrema, tops = [list(reversed(l)) for l in (axes, extrema, tops)]

    # How much would the plot overflow if we kept current zoom levels?
    tot_span = tops[1] + 1 - tops[0]

    b_new_t = extrema[0][0] + tot_span * (extrema[0][1] - extrema[0][0])
    t_new_b = extrema[1][1] - tot_span * (extrema[1][1] - extrema[1][0])
    axes[0].set_ylim(extrema[0][0], b_new_t)
    axes[1].set_ylim(t_new_b, extrema[1][1])

def plot_anal(sys_name, out_names, params):

    out_arrs = []
    for param in params:
        outs, _ = run_one_param(param.values, param.updater, out_names)
        out_arrs.append(outs)

    out_arrs = np.stack(out_arrs, axis=2)

    fig, ax = plt.subplots()
    fig.set_size_inches(12, 8)
    plt.grid()

    x_locs = np.linspace(0, 10, len(params))
    width = 0.7
    ax.axhline(0, color='grey')
    hatch_list = ['//', 'oo', '\\\\']

    for i, _ in enumerate(out_names):
        outs_pos = out_arrs[1, i, :]

        up_bars = ax.bar(x_locs + (i - 1) * width,
                         outs_pos,
                         width - 0.05,
                         label=f"Change in {out_names[i]} due to +1% of parameter",
                         color='none',
                         hatch=hatch_list[i],
                         edgecolor=(0, 0, 0, 1.0),
                         zorder=10)

        ax.bar_label(up_bars, padding=3, labels=['{:,.2%}'.format(x) for x in outs_pos])

    ax.set_yticklabels(['{:,.2%}'.format(x) for x in ax.get_yticks()])
    ax.set_ylabel(f"% Change in {', '.join(out_names)} relative to baseline")
    ax.set_xticks(x_locs, [param.name for param in params])
    ax.set_xlabel('Parameter varied')
    ax.legend()
    plt.tight_layout()
    plt.savefig(Path('plots', f"sense_anal_{sys_name}.pdf"))



# Plot them

def run_aircraft(config, states, debug=False):

    aircraft = Aircraft(config, states, debug=False)

    aircraft.mtom = get_MTOM_from_historical_relations(aircraft)
    previous_mtom = 0

    # Size the cabin and cargo bay as it is constant and is a dependency for other components
    pre_run = aircraft.FuselageGroup.Fuselage
    pre_run.Cabin.size_self()
    pre_run.CargoBay.size_self()

    for i in range(1000):
        get_constraints(aircraft)

        aircraft.get_sized()

        # Check divergence
        if np.isnan(aircraft.mtom):
            logger.warn("DIVERGED :(")
            break
        # Check convergence
        if abs(aircraft.mtom - previous_mtom) < 0.01:
            logger.warn("CONVERGED :)")
            logger.debug(f"Took {i} iterations")
            break
        previous_mtom = aircraft.mtom

    ground_time = operations_and_logistics(aircraft)
    competitive_price_ac, total_program_cost, program_roi, average_price, total_nrc, breakeven_point = production_cost_estimation(aircraft)
    price_ac, cost_per_passenger_km, cost_breakdown, breakdown_summary, roi, revenue_per_flight, cost_per_flight = market_estimations(aircraft, average_price, total_nrc, ground_time)

    power_prop_mass = aircraft.WingGroup.Engines.own_mass + aircraft.FuselageGroup.Power.FuelCells.own_mass 

    tail = aircraft.FuselageGroup.Tail
    return {
            'OEM [kg]': aircraft.oem,
            'Fuel Mass [kg]': aircraft.fuel_mass,
            'DOC/ASK [$/pax/km]': cost_per_passenger_km,
            'Num of Fans [-]': aircraft.WingGroup.Engines.own_amount_fans,
            'P&P mass [kg]': power_prop_mass,
            'Wing Area [m^2]': aircraft.WingGroup.Wing.wing_area,
            'Wing Mass [kg]': aircraft.WingGroup.Wing.own_mass,
            'Installation Angle [deg]': aircraft.WingGroup.Wing.get_installation_angle(),
            'C_m_alpha [-]': aircraft.C_m_alpha_no_fuel,
            'Empennage Mass [kg]': tail.HorizontalTail.own_mass + tail.VerticalTail.own_mass,
            'H Tail Area [m^2]': tail.HorizontalTail.surface_area,
            }


if __name__ == "__main__":
    main()
