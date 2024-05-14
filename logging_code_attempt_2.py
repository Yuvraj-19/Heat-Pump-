import matplotlib.pyplot as plt
import CoolProp.CoolProp as cp
import numpy as np 

tim = []   # Initiate lists for time and inlet water temperature
T1w = []

file_name = "HP_May10_05"
try:
    with open(file_name, "r") as data_file:  # Open file using "with" statement for automatic closure
        title = data_file.readline()  # Read first header line
        props = data_file.readline()  # Read second header line

        # Now read in data line by line
        for line in data_file:
            vals = line.split()  # Split each line into "words"
            if len(vals) >= 2:  # Ensure at least two values are present
                tim.append(float(vals[0]))  # Convert the first value to floating point and append to tim[]
                T1w.append(float(vals[1]))  # Convert the second value to floating point and append to T1w[]
            else:
                print("Skipping line with insufficient data:", line)
except FileNotFoundError:
    print("File not found:", file_name)
except Exception as e:
    print("An error occurred:", e)
