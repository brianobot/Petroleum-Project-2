"""
Python Module containing code to manage functions for analysis of acid viscosity

CopyRight @2023 Brian Obot

https://brianobot.github.io/
"""

# import required modules and functions
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt


# plot original data on graph
# - figure title
# - label x coordinate
# - label y coordinate
# - provide legend for the different conc chart lines

# obtain regression equation for the x,y set
#  - produce regression for each given conc provided

# use the regression equation to produce a updated graph

# receive temp and produce corresponding acid viscosity for the stated conc


filename = "data/acid_viscosity.csv"

data = pd.read_csv(filename, delimiter=",")


def main():
    """Main entry point to module execution"""
    print("Data = ", data)

    # obtain values for the named columns
    temp_range = data['Temp (oF)']
    water_visc = data['Water']
    acid_at_5p = data['5% HCL']
    acid_at_10 = data['10% HCL']
    acid_at_15 = data['15% HCL']
    acid_at_31 = data['31.45% HCL']

    # prepare plot data for original data
    plt.plot(temp_range, water_visc, label='water', marker='o')
    plt.plot(temp_range, acid_at_5p, label='5% Hcl', marker='o')
    plt.plot(temp_range, acid_at_10, label='10% Hcl', marker='o')
    plt.plot(temp_range, acid_at_15, label='15% Hcl', marker='o')
    plt.plot(temp_range, acid_at_31, label='31.45% Hcl', marker='o')

    # prepare graph metadata for original data chart
    plt.title("Acid Viscosity with Temperature Chart")
    plt.xlabel("Temperature (oF)")
    plt.ylabel("Acid Viscosity (cp)")
    plt.grid(which='both')
    plt.legend()

    # start the plot here
    plt.show()

    # interpolate for the different equations
    interp_water = interp1d(temp_range, water_visc, kind='quadratic', fill_value='extrapolate')
    interp_acid5 = interp1d(temp_range, acid_at_5p, kind='quadratic', fill_value='extrapolate')
    interp_acid10 = interp1d(temp_range, acid_at_10, kind='quadratic', fill_value='extrapolate')
    interp_acid15 = interp1d(temp_range, acid_at_15, kind='quadratic', fill_value='extrapolate')
    interp_acid31 = interp1d(temp_range, acid_at_31, kind='quadratic', fill_value='extrapolate')

    # obtain new values from interpolated functions for the variables from 0 to 300
    new_x = np.linspace(0, 300, 100)
    
    new_water = interp_water(new_x)
    new_acid_5 = interp_acid5(new_x)
    new_acid_10 = interp_acid10(new_x)
    new_acid_15 = interp_acid15(new_x)
    new_acid_31 = interp_acid31(new_x)

    temp_range = new_x

    # plot new values
    plt.plot(temp_range, new_water, marker=",")
    plt.plot(temp_range, new_acid_5, marker=",")
    plt.plot(temp_range, new_acid_10, marker=",")
    plt.plot(temp_range, new_acid_15, marker=",")
    plt.plot(temp_range, new_acid_31, marker=",")
    
    plt.show()

    # get regression from interpolated variables
    degree = 2 # set the degree to be used for the regression equation
    y_estimates = {
        "Water": np.polyfit(temp_range, new_water, degree),
        "Acid 5%": np.polyfit(temp_range, new_acid_5, degree),
        "Acid 10%": np.polyfit(temp_range, new_acid_10, degree),
        "Acid 15%": np.polyfit(temp_range, new_acid_15, degree),
        "Acid 31%": np.polyfit(temp_range, new_acid_31, degree),
    }
     
    f_regression_equations = {}
    
    #get formatted regression equation
    for variable, y_estimate in y_estimates.items():
        regression_eqn_str = ""
        index = len(y_estimate)
        for value in y_estimate:
            index -= 1
            if index == 0:
                regression_eqn_str += f"({value:.2f})X^{index}"
                continue
            regression_eqn_str += f" + ({value:.2f})X^{index}"
    
            print(f"Regression Equation = {regression_eqn_str}")
            f_regression_equations[variable] = regression_eqn_str

    print("##########################################################################################")
    for element, eqn in f_regression_equations.items():
        print(f"{element:<10} : {eqn}")


if __name__ == "__main__":
    main()