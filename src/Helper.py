from audioop import reverse
from itertools import count
from numpy import integer
import copy
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


def getTotalTimeCost(system, task_name):
    task = system.returnTask(task_name)
    task_models = task.returnAllModels()
    total_time_cost = [0.0 for idx in range(task.returnMaxModels())]
    curr_idx = 0
    for model in task_models:
        if task.returnInitialSolution() == 'H':
            total_time_cost[curr_idx] += model.returnHumanCost()
        elif task.returnInitialSolution() == 'R':
            total_time_cost[curr_idx] += model.returnMachineCost()
        elif task.returnInitialSolution() == 'HRC':
            total_time_cost[curr_idx] += model.returnComboCost()
        curr_idx += 1
    return total_time_cost


def getValidSubTasks(system, uncompleted_task_list, full_tasklist):
    temp_task_list = []
    for task_name in full_tasklist:
        task = system.returnTask(task_name)
        task_pred = task.returnPredecessors()
        isTaskValid = True
        print("Current task_name {} and current task's preds {}".format(
            task_name, task_pred))
        for pred_list in task_pred:
            for pred in pred_list:
                if pred in uncompleted_task_list:
                    isTaskValid = False
                    break
        if isTaskValid:
            temp_task_list.append(task_name)
    return temp_task_list


def findMinimumCost(system, subtask_list):
    temp_task_name = None
    temp_task_cost = None
    for task_name in subtask_list:
        if temp_task_name == None:
            temp_task_name = task_name
            temp_task_cost = getTotalTimeCost(system, task_name)
        else:
            if getTotalTimeCost(system, task_name) < temp_task_cost:
                temp_task_name = task_name
                temp_task_cost = getTotalTimeCost(system, task_name)
    return temp_task_name, temp_task_cost


def checkCycleTimeRule(system, station, forRule):
    # The assumption is that precedence rule has already been applied for the station and the system as a whole
    max_system_cycle_time = system.returnCycleTime()
    task_list = system.returnTaskListByStation(station)
    task_list.sort()
    # print("Currently checking station {}".format(station))
    # Create a list that keeps tracks of unfinished tasks
    uncompleted_task_list = copy.deepcopy(task_list)
    # Create three lists: to contain HRC tasks, R tasks and H tasks
    hrc_tasks = []
    r_tasks = []
    h_tasks = []
    # Fill the three lists with tasks from the task_list
    for task_name in task_list:
        task = system.returnTask(task_name)
        if task.returnInitialSolution() == 'HRC':
            hrc_tasks.append(task_name)
        elif task.returnInitialSolution() == 'R':
            r_tasks.append(task_name)
        elif task.returnInitialSolution() == 'H':
            h_tasks.append(task_name)
        else:
            print("ERROR: Initial solution is not H, R or HRC")
    # print("Contents of hrc tasks: {}".format(hrc_tasks))
    # print("Contents of r tasks: {}".format(r_tasks))
    # print("Contents of h tasks: {}".format(h_tasks))
    # Initialize the cycle time counter, human resource counter, robot resource counter
    cycle_time = [0.0 for idx in range(system.returnNumOfModels())]
    can_process_hrc = True
    # Create temporary human time and robot time
    human_cycle_time = [0.0 for idx in range(system.returnNumOfModels())]
    robot_cycle_time = [0.0 for idx in range(system.returnNumOfModels())]
    # The loop will go on until every task in the station is completed
    while len(uncompleted_task_list) != 0:
        # Get only the tasks that are posssible to complete from each list
        hrc_subtasks = getValidSubTasks(
            system, uncompleted_task_list, hrc_tasks)
        # Prioritizes HRC tasks over R and H tasks. Only search for R and H tasks if there are no HRC tasks to complete
        if len(hrc_subtasks) != 0 and can_process_hrc:
            # To prevent negative addition
            if human_cycle_time != [0.0 for idx in range(system.returnNumOfModels())] or robot_cycle_time != [0.0 for idx in range(system.returnNumOfModels())]:
                chosen_time = human_cycle_time if sum(human_cycle_time) > sum(
                    robot_cycle_time) else robot_cycle_time
                cycle_time = [x + y for x, y in zip(cycle_time, chosen_time)]
                human_cycle_time = [0.0 for idx in range(
                    system.returnNumOfModels())]
                robot_cycle_time = [0.0 for idx in range(
                    system.returnNumOfModels())]
            # Get the task that can be completed with the least cost
            hrc_task, hrc_task_cost = findMinimumCost(system, hrc_subtasks)
            cycle_time = [x + y for x, y in zip(cycle_time, hrc_task_cost)]
            uncompleted_task_list.remove(hrc_task)
            hrc_tasks.remove(hrc_task)
        else:
            # To process R tasks:
            if len(r_tasks) != 0:
                r_subtasks = getValidSubTasks(
                    system, uncompleted_task_list, r_tasks)
                r_task, r_task_cost = findMinimumCost(system, r_subtasks)
                robot_cycle_time = [x + y for x,
                                    y in zip(robot_cycle_time, r_task_cost)]
                uncompleted_task_list.remove(r_task)
                r_tasks.remove(r_task)
            # To process H tasks:
            if len(h_tasks) != 0:
                h_subtasks = getValidSubTasks(
                    system, uncompleted_task_list, h_tasks)
                h_task, h_task_cost = findMinimumCost(system, h_subtasks)
                human_cycle_time = [x + y for x,
                                    y in zip(human_cycle_time, h_task_cost)]
                uncompleted_task_list.remove(h_task)
                h_tasks.remove(h_task)
        if human_cycle_time == robot_cycle_time:
            can_process_hrc = True
        else:
            can_process_hrc = False
    cycle_time = [x + y + z for x, y,
                  z in zip(cycle_time, human_cycle_time, robot_cycle_time)]
    print("Resulting final cycle time for station {} is {}\n".format(
        station, cycle_time))
    if forRule:  # If forRule is True, returns true or false whether the station's cycle time is less than the system's cycle time
        if max(cycle_time) < max_system_cycle_time:
            return True
        return False
    else:
        return cycle_time

# For Total Cost's Cycle Time calculation


def countTotalCostCycleTime(system):
    max_cycle_time = 0
    station_list = system.returnStationList()
    for station in station_list:
        final_cost = checkCycleTimeRule(system, station, False)
        # print("For station {} the final cycle time list is {}".format(station, final_cost))
        max_cycle_time = max(max_cycle_time, max(final_cost))
    # print("The max cycle time is {}".format(max_cycle_time))
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
    robot_pred_task_list = nonparallelCostCountPerSolution(robot_pred_task_list) if len(
        robot_pred_task_list) > 0 else [0 for i in range(system.returnNumOfModels())]
    human_pred_task_list = nonparallelCostCountPerSolution(human_pred_task_list) if len(
        human_pred_task_list) > 0 else [0 for i in range(system.returnNumOfModels())]
    hrc_pred_task_list = nonparallelCostCountPerSolution(hrc_pred_task_list) if len(
        hrc_pred_task_list) > 0 else [0 for i in range(system.returnNumOfModels())]
    # print("The robot_pred_task_list is {}".format(robot_pred_task_list))
    # print("The human_pred_task_list is {}".format(human_pred_task_list))
    # print("The hrc_pred_task_list is {}".format(hrc_pred_task_list))
    # print("Can it parallel? {}".format(can_parallel))
    if can_parallel:
        robot_compare_human = []
        robot_compare_human.append(robot_pred_task_list)
        robot_compare_human.append(human_pred_task_list)
        robot_compare_human = filterMaxCostPerSolution(robot_compare_human)
        return [x + y for x, y in zip(robot_compare_human, hrc_pred_task_list)]
    else:
        return [x + y + z for x, y, z in zip(robot_pred_task_list, human_pred_task_list, hrc_pred_task_list)]


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
