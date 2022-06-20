from itertools import count
from numpy import integer
from Tasks import *
from Models import *
from Reader import *
from System import *
from StartImprovement import *
from Shaking import *

# def countTotalCost(system, partitions):
#     # TODO: Temporary fix for the total cost
#     total_cost = 0
#     alpha_value = 0
#     rho_value = 0
#     for i in partitions:
#         isThereHuman = 0
#         isThereRobot = 0
#         for j in i:
#             if system.returnTask(j).returnInitialSolution() in ["H", "HRC"] and isThereHuman == 0:
#                 isThereHuman = 1
#             if system.returnTask(j).returnInitialSolution() in ["R", "HRC"] and isThereRobot == 0:
#                 isThereRobot = 1
#             if isThereRobot == 1 and isThereHuman == 1:
#                 break
#         alpha_value += isThereHuman
#         rho_value += isThereRobot
#     cycle_time = getCycleTime(system, partitions)
#     total_cost += alpha_value * system.returnInvestmentCostHuman()
#     total_cost += rho_value * system.returnInvestmentCostRobot()
#     total_cost += (alpha_value * system.returnOperationCostHuman() + rho_value * system.returnOperationCostRobot()) * cycle_time * system.returnNumOfProducts()
#     for partition in partitions:
#         for task_name in partition:
#             current_task = system.returnTask(task_name)
#             if current_task.returnInitialSolution() == "R":
#                 total_cost -= current_task.returnBenefitR()
#             elif current_task.returnInitialSolution() == "HRC":
#                 total_cost -= current_task.returnBenefitHRC()
#     return total_cost

# def sortTaskNamesDecreasing(task_names):
#     task_names.sort(key=lambda x: int(x[1:]))
#     task_names.sort(key=lambda x: int(x[0]), reverse=True)
#     return task_names

# print(sortTaskNamesDecreasing([3,5,2,1,7,8,4,6]))