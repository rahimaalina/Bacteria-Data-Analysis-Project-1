#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 15:19:23 2022

@author: linarahima
"""

#importing needed packages
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Defining variables
# Actions
ACTIONS = [
    "Load data",
    "Filter data",
    "Display statistic",
    "Generate plots",
    "Quit",
]

# Statistics
STATISTICS = [
    "Mean Temperature",
    "Mean Growth rate",
    "Std Temperature",
    "Std Growth rate",
    "Rows",
    "Mean Cold Growth rate",
    "Mean Hot Growth rate",
]


# Filters
FILTERS = [
    "Enable/Disable filters",
    "Bacteria type",
    "Growth rate range",
    "Temperature range",
]


# Bacteria Names
BACTERIAS = [
    "Salmonella enterica",
    "Bacillus cereus",
    "Listeria",
    "Brochothrix thermosphacta",
]


# Data Headers
DATA_HEADER = {
    "Temperature": 0,
    "Growth rate": 1,
    "Bacteria": 2,
}


# The function for loading data
def dataLoad(filename):
    table = pd.read_table(filename, delimiter=" ", header=None)
    data = []
    for i, line in enumerate(np.array(table)):
        if line[DATA_HEADER["Temperature"]] < 10 or line[DATA_HEADER["Temperature"]] > 60:
            print(f"Error: Temperature out of range in line {i + 1}!, Please try again in the range 10<Temperature<60.")
            continue
        if line[DATA_HEADER["Growth rate"]] <= 0:
            print(f"Error: Growth rate out of range in line {i + 1}, Growth Rate cannot be defined as a negative number. Please try again in Growth Rate > 0")
            continue
        if line[DATA_HEADER["Bacteria"]] not in [1, 2, 3, 4]:
            print(f"ERROR: Wrong Bacteria type in line {i + 1}, Please pick a bacteria type 1-4.")
            continue
        data.append(line)
    return np.array(data)


# Function for statistics definition
def dataStatistics(data, statistic):
    result = None
    #Calculating the average temperature
    if statistic == "Mean Temperature":
        result = np.mean(data, axis=0)[DATA_HEADER["Temperature"]]
    #Calculating the average growth rate
    elif statistic == "Mean Growth rate":
        result = np.mean(data, axis=0)[DATA_HEADER["Growth rate"]]
    #Calculating the standard deviation of temperature
    elif statistic == "Std Temperature":
        result = np.std(data, axis=0)[DATA_HEADER["Temperature"]]
    #Calculating the standard deviation of growth rate
    elif statistic == "Std Growth rate":
        result = np.std(data, axis=0)[DATA_HEADER["Growth rate"]]
    #The total number of rows in the data
    elif statistic == "Rows":
        result = len(data)
    #Average Growth rate when Temperature is less than 20 degrees
    elif statistic == "Mean Cold Growth rate":
        cold_data = data[data[:, DATA_HEADER["Temperature"]] < 20]
        result = np.mean(cold_data, axis=0)[DATA_HEADER["Growth rate"]]
    #Average Growth rate when Temperature is greater than 50 degrees
    elif statistic == "Mean Hot Growth rate":
        hot_data = data[data[:, DATA_HEADER["Temperature"]] > 50]
        result = np.mean(hot_data, axis=0)[DATA_HEADER["Growth rate"]]
    return result


# Plotting data
def dataPlot(data):
    bacteriaPlot(data)
    growthRateByTemperaturePlot(data)
    plt.show()


# Defining the type of the plotting graph 1
def bacteriaPlot(data):
    plt.figure()
    bacteria = data[:, DATA_HEADER["Bacteria"]]
    bacteria_num = np.bincount(bacteria.astype(int), minlength=len(BACTERIAS) + 1)[1:]
    plt.bar(BACTERIAS, bacteria_num)
    plt.title(f"Number of bacteria")
    plt.xlabel("Bacteria")
    plt.ylabel("Number")

# Defining the type of the plotting graph 2
def growthRateByTemperaturePlot(data):
    plt.figure()
    markers = ["o", "*", "^", "+"]
    for id, bacteria in enumerate(BACTERIAS):
        data_per_bacteria = data[data[:, DATA_HEADER["Bacteria"]] == (id + 1)]
        temperature = data_per_bacteria[:, DATA_HEADER["Temperature"]]
        growth_rate = data_per_bacteria[:, DATA_HEADER["Growth rate"]]
        plt.scatter(temperature, growth_rate, label=bacteria, marker=markers[id])
    plt.title(f"Growth rate by temperature")
    plt.xlabel("Temperature")
    plt.ylabel("Growth rate")
    plt.xlim([10, 60])
    plt.ylim(bottom=0)
    plt.grid(linestyle="--")
    plt.legend()


# Filtering function
def dataFilter(data, filter, condition):
    result = data
    if filter == "Bacteria type":
        result = data[data[:, DATA_HEADER["Bacteria"]] == condition]
    elif filter == "Growth rate range":
        result = data[(data[:, DATA_HEADER["Growth rate"]] >= condition[0]) & (data[:, DATA_HEADER["Growth rate"]] <= condition[1])]
    elif filter == "Temperature range":
        result = data[(data[:, DATA_HEADER["Temperature"]] >= condition[0]) & (data[:, DATA_HEADER["Temperature"]] <= condition[1])]
    return result


# Applying filters
def applyFilters(data, filters):
    filtered_data = data
    print(filters)
    for key, value in filters.items():
        filtered_data = dataFilter(filtered_data, key, value)
    return filtered_data


# User input functions
def getInputNumber(prompt):
    while True:
        try:
            print()
            print("-" * 40)
            num = int(input(prompt))
            break
        except ValueError:
            print("Error: Sorry, Cannot be accepted. Please enter numbers ONLY")
    return num


def getLimitedInputNumber(prompt, limit):
    prompt = prompt + f" (1 - {limit}) "
    while True:
        num = getInputNumber(prompt)
        if num > 0 and num <= limit:
            break
        else:
            print("Error: Sorry, Wrong number. Please try again in the defined range limit.")
    return num


def getInputRange(prompt):
    prompt = prompt + f" (min, max) "
    while True:
        try:
            print()
            print("-" * 40)
            min, max = input(prompt).split(",")
            min = float(min)
            max = float(max)
            break
        except ValueError:
            print("Error: Wrong range. Please try again!")
    if max > min:
        return (min, max)
    else:
        return (max, min)


# Menu
def getInputString(prompt):
    print()
    print("-" * 40)
    return input(prompt)


def getInputFile(prompt):
    while True:
        print()
        print("-" * 40)
        file = input(prompt)
        if os.path.isfile(file):
            break
        else:
            print("Error: Wrong file path! Please choose the file from your directory.")
    return file


# Menu setting
def printMenu(header, elements):
    separator_len = 40
    print()
    print("=" * separator_len)
    print(f"= {header}")
    print("=" * separator_len)
    for i, item in enumerate(elements):
        print(f"{i + 1}. {item}")


# Filering menu
def getFilter():
    printMenu("Select Filter:", FILTERS)
    return getLimitedInputNumber(f"Which filter would you like to apply?", len(FILTERS))


def getStatistic():
    printMenu("Select Statistic:", STATISTICS)
    return getLimitedInputNumber(f"Which statistic would you like to display", len(STATISTICS))


def getUserAction():
    printMenu("Select Action:", ACTIONS)
    return getLimitedInputNumber(f"Which Action would you like to choose?", len(ACTIONS))


def getBacteria():
    printMenu("Select Bacteria:", BACTERIAS)
    return getLimitedInputNumber(f"Which bacteria would you like to work with?", len(BACTERIAS))


def getFilterConditions(filter):
    if filter == "Bacteria type":
        return getBacteria()
    elif filter == "Growth rate range":
        return getInputRange("Please provide a range for Growth rate")
    elif filter == "Temperature range":
        return getInputRange("Please provide a range for Temperature")


def printStatistic(statistic, value):
    descriptions = {
        "Mean Temperature": "Mean (average) Temperature.",
        "Mean Growth rate": "Mean (average) Growth rate.",
        "Std Temperature": "Standard deviation of Temperature.",
        "Std Growth rate": "Standard deviation of Growth rate.",
        "Rows": "The total number of rows in the data.",
        "Mean Cold Growth rate": "Mean (average) Growth rate when Temperature is less than 20 degrees.",
        "Mean Hot Growth rate": "Mean (average) Growth rate when Temperature is greater than 50 degrees.",
    }
    separator_len = 40
    print()
    print("#" * separator_len)
    print(f"# {statistic}")
    print(f"# {descriptions[statistic]}")
    print("#" * separator_len)
    print(f"# {value}")


def updateStatus():
    separator_len = 40
    print()
    print("*" * separator_len)
    print("* Status")
    print("*" * separator_len)
    print(f"Filename: {LOADED_DATA_FILE}")
    print(f"Data loaded: {False if LOADED_DATA is None else True}")
    print(f"Filter enabled: {FILTER_ENABLE}")
    print(f"Selected filters: {SELECTED_FILTERS}")


LOADED_DATA_FILE = None
LOADED_DATA = None
FILTER_ENABLE = False
SELECTED_FILTERS = {}


#Updating Status
while True:
    updateStatus()

    action = getUserAction()
    print(f"Selected Action: {ACTIONS[action - 1]}\n")

    if action == 1:
        LOADED_DATA_FILE = getInputFile("Give me a filename with data!: ")
        LOADED_DATA = dataLoad(LOADED_DATA_FILE)
    elif action == 2:
        filter = getFilter()
        if filter == 1:
            FILTER_ENABLE = not FILTER_ENABLE
        else:
            SELECTED_FILTERS[FILTERS[filter - 1]] = getFilterConditions(FILTERS[filter - 1])
    elif action == 3:
        if LOADED_DATA is None:
            print("Error: Load data first!")
            continue
        selected_statistic = getStatistic()
        if FILTER_ENABLE:
            input_data = applyFilters(LOADED_DATA, SELECTED_FILTERS)
        else:
            input_data = LOADED_DATA
        statistic = dataStatistics(input_data, STATISTICS[selected_statistic - 1])
        printStatistic(STATISTICS[selected_statistic - 1], statistic)
    elif action == 4:
        if LOADED_DATA is None:
            print("Error: Load data first!")
            continue
        if FILTER_ENABLE:
            input_data = applyFilters(LOADED_DATA, SELECTED_FILTERS)
        else:
            input_data = LOADED_DATA
        dataPlot(input_data)
    elif action == 5:
        break
    else:
        print("Error: Sorry. Wrong Action. Please Try again!")
        



