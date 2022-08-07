from msilib.schema import Error
from traceback import print_tb

from numpy import integer
from Tasks import *
from Models import *

import os
import pandas as pd


def createListOfPredOrSucc(pred_or_succ):
    # If "predecessors"/"successors" is a single integer, return a list of integer of 1 length
    # If "predecessors"/"successors" is a string containing integers separated by commas, return a list of integers
    temp_list = pred_or_succ.split(",")
    map_integers = map(int, temp_list)
    list_integers = list(map_integers)
    if len(list_integers) == 1 and list_integers[0] == -1:
        return [], 0
    else:
        return list_integers, len(list_integers)


# File must be located in the "testcase" directory and have the "csv" extension
def ReadFile(filename, MainSystem):
    try:
        path_to_folder = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', 'testcase'))
        path_to_file = os.path.abspath(os.path.join(path_to_folder, filename))
        df = pd.read_csv(path_to_file)
        for i in range(0, df.__len__()):
            current_row = df.iloc[i]
            task_name = current_row['task']
            num_of_models = MainSystem.returnNumOfModels()
            temp_task = Task(task_name, num_of_models)
            for i in range(0, num_of_models):
                current_count = i + 1
                model_name = current_row['model' + str(current_count) + "_name"]
                human_cost = current_row['model' + str(current_count) + "_h"]
                machine_cost = current_row['model' + str(current_count) + "_r"]
                combo_cost = current_row['model' + str(current_count) + "_hrc"]
                new_model = Model(task_name, model_name, human_cost, machine_cost, combo_cost)
                temp_task.addModel(new_model)
            predecessor_list, num_of_pred = createListOfPredOrSucc(str(current_row['predecessor']))
            successor_list, num_of_succ = createListOfPredOrSucc(current_row['successor'])
            initial_solution = current_row['initial_solution']
            originStation = current_row['belongsToStation']
            benefit_R = current_row['benefit_r']
            benefit_HRC = current_row['benefit_hrc']
            temp_task.setDirectPredecessors(predecessor_list)
            temp_task.setPredecessors(predecessor_list)
            temp_task.setNumOfPredecessors(num_of_pred)
            temp_task.setDirectSuccessors(successor_list)
            temp_task.setNumOfSuccessors(num_of_succ)
            temp_task.setInitialSolution(initial_solution)
            temp_task.setOriginStation(originStation)
            temp_task.setBenefitR(benefit_R)
            temp_task.setBenefitHRC(benefit_HRC)
            MainSystem.addTask(temp_task)
    except Error as err:
        print(err)
