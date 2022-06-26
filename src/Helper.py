from audioop import reverse
from itertools import count
from numpy import integer
from Tasks import *
from Models import *
from Reader import *
from System import *


def sortStationOrder(system):
    # Assumed that system's station is ordered alphabetically
    # Maximum station can be held is from A to ZZ.
    # Meaning there can be 26 * 27 stations (more than enough for the requirements)
    station_list = system.returnStationList()
    one_char_list = []
    two_char_list = []
    for i in station_list:
        if len(i) == 1:
            one_char_list.append(i)
        elif len(i) == 2:
            two_char_list.append(i)
    one_char_list.sort()
    two_char_list.sort()
    return one_char_list + two_char_list


def isStationAfter(station_1, station_2):
    # Returns boolean whether station_1 is after station_2 in alphabetical order
    # Used in checking precedence of stations (precedence rule)
    # station_1 and station_2 are strings (of length 1 or 2)
    if len(station_1) > len(station_2):
        return True
    elif len(station_1) < len(station_2):
        return False
    else:
        return station_1 > station_2
    
# For rules' implementations
def checkIfSameStationRule(system, task_name_a, task_name_b):
    # Return True if the two tasks are from the same station
    if system.returnStationFromTask(task_name_a) == system.returnStationFromTask(task_name_b):
        return True
    return False

def checkIfSameStation(system, task_name_a, station_name):
    if system.returnStationFromTask(task_name_a) == station_name:
        return True
    return False

def singularStationRule(system, task_name_a, task_name_b):
    # Check whether task_a and task_b both are from stations that has length of one
    # Returns False if both task are from individual stations
    # Returns True if valid switch between two stations
    station_a = system.returnStationFromTask(task_name_a)
    station_b = system.returnStationFromTask(task_name_b)
    len_station_a = system.returnLenStation(station_a)
    len_station_b = system.returnLenStation(station_b)
    if len_station_a == 1 and len_station_b == 1:
        return False
    return True

def checkPrecedenceRule(system, station_name):
    task_list = system.returnTaskListByStation(station_name)
    task_list.sort(reverse=True)
    for idx in range(len(task_list)):
        ref_task_name = task_list[idx]
        ref_task = system.returnTask(ref_task_name)
        ref_task_pred = ref_task.returnDirectPredecessors()
        for pred in ref_task_pred:
            pred_task = system.returnTask(pred)
            pred_station = pred_task.returnOriginStation()
            if pred in task_list or isStationAfter(station_name, pred_station):
                continue
            return False
    return True

def checkCycleTimeRule(system, station, forRule):
    # If forRule is True, check whether the station's cycle time is less than the task's cycle time
    # If forRule is False, returns max time for models in all task in the station
    # Check whether the cycle time of the tasks in the station is less than the cycle time of the system
    max_system_cycle_time = system.returnCycleTime()
    task_list = system.returnTaskListByStation(station)
    task_list.sort()
    temp_storage = [] 
    # Temp storage is a list of [A,B,C,D,...] with A being the source task 
    # and B,C,D,... respectively being the H/R/HRC cost for each model in the task
    for task_name in task_list:
        task = system.returnTask(task_name)
        direct_pred = task.returnDirectPredecessors()
        # print("Task {} has direct predecessors {}".format(task_name, direct_pred))
        if len(direct_pred) in [0,1]:
            pred_task, temp_storage = whereIsPredInTempStorage(temp_storage, direct_pred)
        else:
            pred_task = None
        # If the task is starting task OR (the task has only one predecessor and it's not in the station)
        if len(direct_pred) == 0 or (len(direct_pred) == 1 and pred_task is None):
            temp_new_list = [task_name]
            task = system.returnTask(task_name)
            task_solution = task.returnInitialSolution()
            temp_new_list += task.isolateModelCosts(task_solution)
            # print("The added list is {}".format(temp_new_list))
            temp_storage.append(temp_new_list)
            continue
        # If the task has only one predecessor and it's on the station (consecutive tasks)
        elif len(direct_pred) == 1 and pred_task is not None:
            temp_new_list = pred_task
            temp_new_list[0] = task_name
            task = system.returnTask(task_name)
            task_solution = task.returnInitialSolution()
            isolated_model_costs = task.isolateModelCosts(task_solution)
            for idx in range(0, len(isolated_model_costs)):
                temp_new_list[idx + 1] += isolated_model_costs[idx]
            # print("The added list is {}".format(temp_new_list))
            temp_storage.append(temp_new_list)
            continue
        # Multiple predecessors for the reference task
        elif len(direct_pred) > 1:
            count_existing_pred_in_station = 0
            store_pred_task = []
            for pred in direct_pred:
                pred_task, temp_storage = whereIsPredInTempStorage(temp_storage, pred)
                if pred_task is not None:
                    count_existing_pred_in_station += 1
                    store_pred_task.append(pred_task)
            # If the task has multiple predecessors and all of them are NOT in the station
            if count_existing_pred_in_station == 0:
                temp_new_list = [task_name]
                task = system.returnTask(task_name)
                task_solution = task.returnInitialSolution()
                temp_new_list += task.isolateModelCosts(task_solution)
                # print("The added list is {}".format(temp_new_list))
                temp_storage.append(temp_new_list)
                continue
            # If the task has multiple predecessors and ONLY ONE of them is in the station
            elif count_existing_pred_in_station == 1:
                temp_new_list = store_pred_task[0]
                temp_new_list[0] = task_name
                task = system.returnTask(task_name)
                task_solution = task.returnInitialSolution()
                isolated_model_costs = task.isolateModelCosts(task_solution)
                for idx in range(0, len(isolated_model_costs)):
                    temp_new_list[idx + 1] += isolated_model_costs[idx]
                # print("The added list is {}".format(temp_new_list))
                temp_storage.append(temp_new_list)
                continue
            # If the task has multiple predecessors and AT LEAST TWO of them are in the station
            else:
                max_cost_models = filterMaxCost(system, store_pred_task)
                temp_new_list = [task_name]
                temp_new_list += max_cost_models
                task = system.returnTask(task_name)
                task_solution = task.returnInitialSolution()
                isolated_model_costs = task.isolateModelCosts(task_solution)
                for idx in range(0, len(max_cost_models)):
                    temp_new_list[idx + 1] += isolated_model_costs[idx]
                # print("The added list is {}".format(temp_new_list))
                temp_storage.append(temp_new_list)
                continue
    # Calculate the total cycle time for the station
    final_cost = [0 for i in range(system.returnNumOfModels())]
    # print("For station {}, the temp_storage is {}".format(station, temp_storage))
    final_cost = filterMaxCost(system, temp_storage)
    if forRule:
        for cost in final_cost:
            if cost > max_system_cycle_time:
                return False
        return True
    else:
        return final_cost

# For Total Cost's Cycle Time calculation
def countTotalCostCycleTime(system):
    max_cycle_time = 0
    station_list = system.returnStationList()
    for station in station_list:
        final_cost = checkCycleTimeRule(system, station, False)
        print("For station {} the final cycle time list is {}".format(station, final_cost))
        max_cycle_time = max(max_cycle_time, max(final_cost))
    print("The max cycle time is {}".format(max_cycle_time))
    return max_cycle_time
            
            
def whereIsPredInTempStorage(temp_storage, pred):
    # Returns the index of the predecessor in the temp_storage with the costs
    for lists in temp_storage:
        # print(lists)
        # print(pred)
        if lists[0] == pred:
            idx = temp_storage.index(lists)
            return temp_storage.pop(idx), temp_storage
    return None, temp_storage

def filterMaxCost(system, pred_task_list):
    # Find maximum time for each model in the pred_task_list
    # Computes parallelism in case different tasks use different resource
    can_parallel = True
    robot_pred_task_list = []
    human_pred_task_list = []
    hrc_pred_task_list = []
    for pred_task in pred_task_list:
        task = system.returnTask(pred_task[0])
        if task.returnInitialSolution() == "HRC":
            can_parallel = False
            hrc_pred_task_list.append(pred_task[1:])
        elif task.returnInitialSolution() == "H":
            human_pred_task_list.append(pred_task[1:])
        elif task.returnInitialSolution() == "R":
            robot_pred_task_list.append(pred_task[1:])
    robot_pred_task_list = nonparallelCostCountPerSolution(robot_pred_task_list) if len(robot_pred_task_list) > 0 else [0 for i in range(system.returnNumOfModels())]
    human_pred_task_list = nonparallelCostCountPerSolution(human_pred_task_list) if len(human_pred_task_list) > 0 else [0 for i in range(system.returnNumOfModels())]
    hrc_pred_task_list = nonparallelCostCountPerSolution(hrc_pred_task_list) if len(hrc_pred_task_list) > 0 else [0 for i in range(system.returnNumOfModels())]
    # print("The robot_pred_task_list is {}".format(robot_pred_task_list))
    # print("The human_pred_task_list is {}".format(human_pred_task_list))
    # print("The hrc_pred_task_list is {}".format(hrc_pred_task_list))
    # print("Can it parallel? {}".format(can_parallel))
    if can_parallel:
        robot_compare_human = []
        robot_compare_human.append(robot_pred_task_list)
        robot_compare_human.append(human_pred_task_list)
        robot_compare_human = filterMaxCostPerSolution(robot_compare_human)
        return [x + y for x,y in zip(robot_compare_human, hrc_pred_task_list)]
    else:
        return [x + y + z for x,y,z in zip(robot_pred_task_list, human_pred_task_list, hrc_pred_task_list)]
        
    
def filterMaxCostPerSolution(pred_task_list):
    temp_store_all_costs = [[0] for i in range(len(pred_task_list[0]))]
    for pred_task in pred_task_list:
        for idx in range(len(pred_task)):
            temp_store_all_costs[idx].append(pred_task[idx])
    max_cost_models = []
    for model in temp_store_all_costs:
        max_cost_models.append(max(model))
    return max_cost_models

def nonparallelCostCountPerSolution(pred_task_list):
    temp_store_all_costs = [0 for i in range(len(pred_task_list[0]))]
    for pred_task in pred_task_list:
        for idx in range(len(pred_task)):
            temp_store_all_costs[idx] += pred_task[idx]
    return temp_store_all_costs

def haltProgress():
    delayProgram = input("Enter anything to continue...")