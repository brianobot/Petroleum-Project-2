"""
Python Module containing code to manage functions for analysis of acid injection rate

CopyRight @2023 Brian Obot

https://brianobot.github.io/
"""

# import required modules and functions
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


filename = "data/acid_mud_injection_rate.csv"


data = pd.read_csv(filename, delimiter=",")

def main():
    """Main entry point to module execution"""
    print("Data = ", data)


if __name__ == "__main__":
    main()