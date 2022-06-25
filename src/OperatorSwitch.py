from Tasks import *
from Models import *
from Reader import *
from System import *
from StartImprovement import *
from Helper import *
from LocalSearch import *
from StationAllocation import *

import copy
import random

def startOperatorSwitch(system, partitions):
    solution_list = ['HRC','R','H']
    for task_name in partitions:
        attempted_solutions = []
        task = system.returnTask(task_name)
        task_station = task.returnOriginStation()
        task_solution = copy.deepcopy(task.returnInitialSolution())
        attempted_solutions.append(task_solution)
        for possible_solution in solution_list:
            if possible_solution == task_solution:
                continue
            task.setInitialSolution(possible_solution)
            print("Attempt to switch solution of task {} from {} to {}".format(task_name, task_solution, possible_solution))
            if checkCycleTimeRule(system, task_station, True):
                print("OperatorSwitch: Task {} is now using {} solution.\n".format(task_name, possible_solution))
                break
            else:
                task.setInitialSolution(task_solution)
                print("Operator Switch failed because violation of Cycle Time Rule.\n")
    print("OperatorSwitch: Done")
    print("System's total cost: {}".format(str(system.countTotalCost())))
    return system