"""
Python Module containing code to manage functions for analysis of acid viscosity

CopyRight @2023 Brian Obot
https://brianobot.github.io/
"""

# import required modules and functions
import numpy as np
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d

# Program Flow 
# plot original data on graph
# - figure title ✅
# - label x coordinate ✅
# - label y coordinate ✅
# - provide legend for the different conc chart lines ✅

# obtain regression equation for the x,y set
#  - produce regression for each given conc provided

# use the regression equation to produce a updated graph
# receive temp and produce corresponding acid viscosity for the stated conc

DATA_POINT = 100 

filename = "data/acid_viscosity.csv"

data = pd.read_csv(filename, delimiter=",")

# obtain values for the named columns
temp_range = data['Temp (oF)']
water_visc = data['Water']
acid_at_5p = data['5% HCL']
acid_at_10 = data['10% HCL']
acid_at_15 = data['15% HCL']
acid_at_31 = data['31.45% HCL']


def plot_original_data():
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


def obtain_interpolated_functions():
    # interpolate for the different equations
    interp_water = interp1d(temp_range, water_visc, kind='quadratic', fill_value='extrapolate')
    interp_acid5 = interp1d(temp_range, acid_at_5p, kind='quadratic', fill_value='extrapolate')
    interp_acid10 = interp1d(temp_range, acid_at_10, kind='quadratic', fill_value='extrapolate')
    interp_acid15 = interp1d(temp_range, acid_at_15, kind='quadratic', fill_value='extrapolate')
    interp_acid31 = interp1d(temp_range, acid_at_31, kind='quadratic', fill_value='extrapolate')

    return [
        interp_water,
        interp_acid5,
        interp_acid10,
        interp_acid15,
        interp_acid31,
    ]

def generate_regression_values_for_conc(all=False):
    trial = 0
    index = None
    if all:
        pass
    else:
        options = [5, 10, 15, 31.5]
        while trial < 3:
            conc = float(input(f"Please specify a value for the acid concentration: {options=}: "))
            if conc not in options:
                trial += 1
                print("Invalid Value for Concentration! Must be between 0 and 35.\n")
            else:
                break
        else:
            raise Exception("Too Many Failed Inputs for Conc! Restart Program")
        
        print(f"Acid Concentration to be used = {conc}")
        index = options.index(conc)

    # obtain new values from interpolated functions for the variables from 0 to 300
    new_x = np.linspace(0, 300, DATA_POINT)
    
    interp_water, interp_acid5, interp_acid10, interp_acid15, interp_acid31 = obtain_interpolated_functions()

    new_water = interp_water(new_x)
    new_acid_5 = interp_acid5(new_x)
    new_acid_10 = interp_acid10(new_x)
    new_acid_15 = interp_acid15(new_x)
    new_acid_31 = interp_acid31(new_x)

    return [new_water, new_acid_5, new_acid_10, new_acid_15, new_acid_31], index


def plot_new_regression_graph(all=True):
    if all:
        data, _ = generate_regression_values_for_conc(all=True)
    else:
        data, data_index = generate_regression_values_for_conc(all=False)
        data = [data[data_index], ]

    temp_range = np.linspace(0, 300, DATA_POINT)

    # plot new values
    for index, datum in enumerate(data):
        plt.plot(temp_range, datum, marker=",")
    # prepare graph metadata for original data chart
    plt.title("New Acid Viscosity with Temperature Chart")
    plt.xlabel("Temperature (oF)")
    plt.ylabel("New Acid Viscosity (cp)")
    plt.grid(which='both')
    plt.legend()
    # plot the graph here
    plt.show()


def generate_regression_equation(y, degree=3):
    # need a range for x
    # need a range for y
    # specify a degree for the regression equation
    x = np.linspace(0, 300, DATA_POINT)

    # get regression
    y_est = np.polyfit(x, y, degree)
    return y_est

def main():
    """Main entry point to module execution"""
    intro = f"""
    TITLE: ACID VISCOSITY-TEMPERATURE ANALYSIS PROGRAM
    ###################################################################
    Program Started Successfully!.              Timestamp:{datetime.now().date()}
    ###################################################################
    Program to analyze Acid Viscosity for different concentration of 
    Acid over a temperature temperture Range. Follow the prompt to use
    the program correctly, 
    
    # _____________________________________________
    NOTE: confirm your inputs before pressing Enter.

    Options (Commands):
        Type 1: To Plot Original Viscosity-Temperature data for All specified Concentration.
        Type 2: To Plot the Regression Value for the Viscosity-Temp Data for all the Specified Concentration
        Type 3: To Plot the Regression Value for the Viscosity-Temp Data for a Specific Concentration
        Type 4: To Generate a regression equation for a specific concenration.
        Type 5: To Interatively Obtain a Viscosity Value for a Given Temperature Value
    
    _____________________________________________
    """
    print(intro)
    command = None
    while command != "q":
        command = input("Enter Command >>>")
        match command:
            case "1":
                plot_original_data()
            case "2":
                plot_new_regression_graph()
            case "3":
                plot_new_regression_graph(all=False)
            case "4":
                data, data_index = generate_regression_values_for_conc()
                y = data[data_index]
                reg_var = generate_regression_equation(y)
                print("Regression eqn = ", reg_var)
            case "5":
                option = ["5", "10", "15", "31.5"]
                select = input(f"Select a Concentration. Options => {option}: ")
                select_index = option.index(select) + 1
                func = obtain_interpolated_functions()[select_index]
                value = float(input("Enter a Temperature value: "))
                print(f"You Entered {value}")
                result = func(value)
                print(f"Viscosity Value = {result}")
            case _:
                print("Invalid Option! Try Again")
    
    print("\nProgram CLOSED Successfully!")


if __name__ == "__main__":
    main()