"""
Python Module containing code to manage functions for analysis of acid hydrostatic grad

CopyRight @2023 Brian Obot
https://brianobot.github.io/
"""

# import required modules and functions
import numpy as np
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d

DATA_POINT = 100

filename = "data/acid_hydrostatic_gradient.csv"

data = pd.read_csv(filename, delimiter=",")

acid_strength = data['Acid Strength (% wt)']
hydrostatic_grad = data['Hydrostatic Gradient (psi/ft)']


def plot_original_data():
    plt.plot(acid_strength ,hydrostatic_grad, marker="*")
    # prepare graph metadata for original data chart
    plt.title("Acid Hydrostatic Gradient with Acid Strength Chart")
    plt.xlabel("Acid Strength (% wt)")
    plt.ylabel("Acid Hydrostatic Gradient (psi/ft)")
    plt.grid(which='both')
    # plt.legend()
    # start the plot here
    plt.show()


def get_interpolation_func_for_acid_gradient():
    func = interp1d(acid_strength, hydrostatic_grad, kind='quadratic', fill_value='extrapolate')
    return func


def generate_regression_values_for_gradient():
    new_x = np.linspace(0, 50, DATA_POINT)
    new_acid_gradient = get_interpolation_func_for_acid_gradient()(new_x)
    return new_acid_gradient


def plot_new_regression_graph():
    x_axis = np.linspace(0, 50 ,DATA_POINT)
    values = generate_regression_values_for_gradient()

    plt.plot(x_axis ,values, marker=",")
    # prepare graph metadata for original data chart
    plt.title("Regression Value for Acid Hydrostatic Gradient with Acid Strength Chart")
    plt.xlabel("Acid Strength (% wt)")
    plt.ylabel("Acid Hydrostatic Gradient (psi/ft)")
    plt.grid(which='both')
    # plt.legend()
    # start the plot here
    plt.show()


def generate_regression_equation(y, degree=3):
    # need a range for x
    # need a range for y
    # specify a degree for the regression equation
    x = np.linspace(0, 50, DATA_POINT)

    # get regression
    y_est = np.polyfit(x, y, degree)
    return y_est



def main():
    """Main entry point to module execution"""
    intro = f"""
    TITLE: ACID HYDROSTATIC GRADIENT-ACID STRENGTH ANALYSIS PROGRAM
    ###################################################################
    Program Started Successfully!.              Timestamp:{datetime.now().date()}
    ###################################################################
    Program to analyze Acid Hydrostatic Gradient for Over a range of Acid Strength.
    Follow the prompt to use the program correctly, 
    
    # _____________________________________________
    NOTE: confirm your inputs before pressing Enter.

    Options (Commands):
        Type 1: To Plot Original Acid-Gradient/Acid Strength Data.
        Type 2: To Plot Regression Values for Acid-Gradient/Acid Strength Data.
        Type 3: To Get Regression Values for Acid-Gradient/Acid Strength Data.
        Type 4: To Get Regression Equation for Acid-Gradient/Acid Strength.
        Type 5: To Get Acid-Gradient Value for specific Acid Strenth value.


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
                values = generate_regression_values_for_gradient()
                print("Regression Values = \n")
                print(values)
            case "4":
                x = np.linspace(0, 50, DATA_POINT)
                y = generate_regression_values_for_gradient()
                reg_eqn = generate_regression_equation(y)
                print("Regresion Equation for Acid Hydrostatic Gradient-Acid Strength is")
                print("________________________________________________________")
                print(reg_eqn)
                print("________________________________________________________")
            case "5":
                value = float(input("Please specify the Acid Strength: "))
                print(f"You inputed Acid Strength = {value}")
                result = get_interpolation_func_for_acid_gradient()(value)
                print(f"Acid Hydrostatic Gradient for {value} is         {result}")
            case _:
                pass


if __name__ == "__main__":
    main()