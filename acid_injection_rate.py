"""
Python Module containing code to manage functions for analysis of acid injection rate

CopyRight @2023 Brian Obot
https://brianobot.github.io/
"""

# import required modules and functions
import numpy as np
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d

filename = "data/acid_mud_injection_rate.csv"
data = pd.read_csv(filename, delimiter=",")

UNIT_OPTIONS = ["0.001", "0.005", "0.01", "0.025", "0.05", "0.1", "0.2"]
DATA_POINT = 100
INDEX = None

depth = data["Depth of K (inches)"]
depth_0001 = data["0.001"]
depth_0005 = data["0.005"]
depth_0010 = data["0.01"]
depth_0025 = data["0.025"]
depth_0050 = data["0.05"]
depth_0100 = data["0.1"]
depth_0200 = data["0.2"]

X_AXIS = [
    depth_0001,
    depth_0005,
    depth_0010,
    depth_0025,
    depth_0050,
    depth_0100,
    depth_0200
]


def plot_original_data():
    plt.plot(depth[:-2], depth_0001[:-2], label="0.001bbl/min/ft", marker="*")
    plt.plot(depth[:-1], depth_0005[:-1], label="0.005bbl/min/ft", marker="*")
    plt.plot(depth[:-1], depth_0010[:-1], label="0.010bbl/min/ft", marker="*")
    plt.plot(depth, depth_0025, label="0.025bbl/min/ft", marker="*")
    plt.plot(depth, depth_0050, label="0.050bbl/min/ft", marker="*")
    plt.plot(depth, depth_0100, label="0.100bbl/min/ft", marker="*")
    plt.plot(depth, depth_0200, label="0.200bbl/min/ft", marker="*")
    # prepare graph metadata for original data chart
    plt.title("Volume of mud acid with injection rates chart @ 150 oF")
    plt.xlabel("Depth of K (inches)")
    plt.ylabel("Volume of mud acid (gal/ft)")
    plt.grid(which='both')
    plt.legend()
    # start the plot here
    plt.show()


def obtain_interpolated_functions():
    # interpolate for the different equations
    interp_depth_0001 = interp1d(depth[:-2], depth_0001[:-2], kind='quadratic', fill_value='extrapolate')
    interp_depth_0005 = interp1d(depth[:-1], depth_0005[:-1], kind='quadratic', fill_value='extrapolate')
    interp_depth_0010 = interp1d(depth[:-1], depth_0010[:-1], kind='quadratic', fill_value='extrapolate')
    interp_depth_0025 = interp1d(depth, depth_0025, kind='quadratic', fill_value='extrapolate')
    interp_depth_0050 = interp1d(depth, depth_0050, kind='quadratic', fill_value='extrapolate')
    interp_depth_0100 = interp1d(depth, depth_0100, kind='quadratic', fill_value='extrapolate')
    interp_depth_0200 = interp1d(depth, depth_0200, kind='quadratic', fill_value='extrapolate')

    return [
        interp_depth_0001,
        interp_depth_0005,
        interp_depth_0010,
        interp_depth_0025,
        interp_depth_0050,
        interp_depth_0100,
        interp_depth_0200,
    ]


def generate_regression_values_for_acid_unit(all=True, index=INDEX):
    new_x = np.linspace(0, 30 ,DATA_POINT)
    if all:
        values = []
        for func in obtain_interpolated_functions():
            result = func(new_x)
            values.append(result)
        return values
    else:
        func = obtain_interpolated_functions()[index]
        option = input("Enter a value for the Depth Value: ")
        result = func(option)
        return result


def plot_regression_graph(all=True, index=INDEX):
    new_x = np.linspace(0, 10, DATA_POINT)
    if all:
        for index, func in enumerate(obtain_interpolated_functions()):
            y_axis = func(new_x)
            label_text = UNIT_OPTIONS[index]
            plt.plot(new_x, y_axis, label=label_text+"/min/ft", marker=",")
    else:
        func = obtain_interpolated_functions()[index]
        y_axis = func(new_x)
        label_text = UNIT_OPTIONS[index]
        plt.plot(new_x, y_axis, label=label_text+"/min/ft", marker=",")


    # prepare graph metadata for original data chart
    plt.title("Volume of mud acid with injection rates chart @ 150 oF")
    plt.xlabel("Depth of K (inches)")
    plt.ylabel("Volume of mud acid (gal/ft)")
    plt.grid(which='both')
    plt.legend()
    # start the plot here
    plt.show()


def generate_regression_equation(y, degree=3):
    # need a range for x
    # need a range for y
    # specify a degree for the regression equation
    x = np.linspace(0, 10, DATA_POINT)

    # get regression
    y_est = np.polyfit(x, y, degree)
    return y_est


def main():
    """Main entry point to module execution"""
    intro = f"""
    Title: ACID MUD INJECTION RATE ANALYSIS PROGRAM
    ###################################################################
    Program Started Successfully!.              Timestamp:{datetime.now().date()}
    ###################################################################
    Program to analyze Acid Injection Rate for different depth of 
    penetratino. 
    Follow the prompt to use the program correctly, 
    
    # _____________________________________________
    NOTE: confirm your inputs before pressing Enter.
    NOTE: Each Acid VOlume last for a whole program session, to change acid volume restart the program

    """

    intro_2 = """

    Options (Commands):
        Type 1: To Plot Original Volume of Mud Acid-Depth of Penetration data for All Unit of Acid Provided.
        Type 2: To Plot Regression Volume of Mud Acid-Depth of Penetration data for All Unit of Acid Provided.
        Type 3: To Plot Regression Volume of Mud Acid-Depth of Penetration data for Specific Unit of Acid Provided.
        Type 4: To Generate Regression Values for Specific Acid Unit.
        Type 5: To Get Regression Equation for a Specific Acid Unit.
        Type 6: To Get Acid Mud Volume for a Specific Acid Unit.
    
    _____________________________________________
    """
    print(intro)
    
    global INDEX
    select_acid_volume = input(f"Please Select a Acid VOlume for this session! OPTIONS = {UNIT_OPTIONS}:  ")
    INDEX = UNIT_OPTIONS.index(select_acid_volume)
    print("Index = ", INDEX)

    print(intro_2)
    command = None
    while command != "q":
        command = input("Enter Command >>>")
        match command:
            case "1":
                plot_original_data()
            case "2":
                plot_regression_graph()
            case "3":
                plot_regression_graph(all=False, index=INDEX)
            case "4":
                values = generate_regression_values_for_acid_unit(all=True)
                print("Values = ", values)
            case "5":
                y = generate_regression_values_for_acid_unit(all=True)[INDEX]
                eqn = generate_regression_equation(y)
                print(f"Equations = {eqn}")
            case "6":
                value = generate_regression_values_for_acid_unit(all=False, index=INDEX)
                print("Acid Mud Volume = ", value)
            case _:
                pass


if __name__ == "__main__":
    main()