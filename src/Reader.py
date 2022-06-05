from msilib.schema import Error
from traceback import print_tb

from numpy import integer
from Tasks import *
from Models import *

import os
import pandas as pd


def createListOfPredecessors(predecessors):
    # If "predecessors" is a single integer, return a list of integer of 1 length
    # If "predecessors" is a string containing integers separated by commas, return a list of integers
    if (type(predecessors) == integer):
        if predecessors != -1:
            return [predecessors]
        else:
            return []
    else:
        temp_list = predecessors.split(",")
        map_integers = map(int, temp_list)
        return list(map_integers)

# File must be located in the "testcase" directory and have the "txt" extension


def ReadFile(filename, MainSystem):
    try:
        path_to_folder = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', 'testcase'))
        path_to_file = os.path.abspath(os.path.join(path_to_folder, filename))
        df = pd.read_csv(path_to_file)
        for i in range(0, df.__len__()):
            current_row = df.iloc[i]
            task_name = current_row['task']
            num_of_models = current_row['num_models']
            temp_task = Task(task_name, num_of_models)
            for i in range(0, num_of_models):
                current_count = i + 1
                model_name = current_row['model' +
                                         str(current_count) + "_name"]
                human_cost = current_row['model' + str(current_count) + "_h"]
                machine_cost = current_row['model' + str(current_count) + "_r"]
                combo_cost = current_row['model' + str(current_count) + "_hrc"]
                new_model = Model(task_name, model_name,
                                  human_cost, machine_cost, combo_cost)
                temp_task.addModel(new_model)
            predecessor_list = createListOfPredecessors(
                current_row['predecessor'])
            initial_solution = current_row['initial_solution']
            originStation = current_row['belongsToStation']
            temp_task.setPredecessors(predecessor_list)
            temp_task.setInitialSolution(initial_solution)
            temp_task.setOriginStation(originStation)
            MainSystem.addTask(temp_task)
    except Error as err:
        print(err)
