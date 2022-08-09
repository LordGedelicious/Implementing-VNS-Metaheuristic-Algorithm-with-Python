from audioop import reverse
from itertools import count
from numpy import integer
import copy
from Tasks import *
from Models import *
from Reader import *
from System import *


def getTotalTimeCost(system, task_name):
    task = system.returnTask(task_name)
    task_models = task.returnAllModels()
    total_time_cost = 0.0
    for model in task_models:
        if task.returnInitialSolution() == 'H':
            total_time_cost += model.returnHumanCost()
        elif task.returnInitialSolution() == 'R':
            total_time_cost += model.returnMachineCost()
        elif task.returnInitialSolution() == 'HRC':
            total_time_cost += model.returnComboCost()
    return total_time_cost


def getValidTasks(system, uncompleted_task_list, task_list, operator, human_resource, robot_resource):
    if human_resource and robot_resource and operator == 'HRC' and len(task_list) != 0:
        can_modify_human = True
        can_modify_robot = True
    elif human_resource and operator == 'H' and len(task_list) != 0:
        can_modify_human = True
        can_modify_robot = False
    elif robot_resource and operator == 'R' and len(task_list) != 0:
        can_modify_robot = True
        can_modify_human = False
    else:
        return None, uncompleted_task_list, task_list, human_resource, robot_resource
    # To store all possible HRC tasks that can be completed in this iteration
    temp_chosen_tasks = None
    for task_name in task_list:
        task = system.returnTask(task_name)
        task_pred_count = task.returnNumOfPredecessors()
        # Only process HRC tasks that have all their predecessors completed
        for task_predecessor in task.returnPredecessors():
            if task_predecessor not in uncompleted_task_list:
                task_pred_count -= 1
        if task_pred_count == 0:
            if temp_chosen_tasks == None:
                temp_chosen_tasks = task_name
                human_resource = False if can_modify_human else human_resource
                robot_resource = False if can_modify_robot else robot_resource
                task_list.remove(task_name)
                uncompleted_task_list.remove(task_name)
            else:
                current_task = temp_chosen_tasks
                new_task = task_name
                current_task_cost = getTotalTimeCost(system, current_task)
                new_task_cost = getTotalTimeCost(system, new_task)
                if current_task_cost > new_task_cost:
                    temp_chosen_tasks = new_task
                    human_resource = False if can_modify_human else human_resource
                    robot_resource = False if can_modify_robot else robot_resource
                    uncompleted_task_list.remove(new_task)
                    uncompleted_task_list.append(current_task)
                else:
                    temp_chosen_tasks = current_task
                    human_resource = False if can_modify_human else human_resource
                    robot_resource = False if can_modify_robot else robot_resource
    return temp_chosen_tasks, uncompleted_task_list, task_list, human_resource, robot_resource


def getValidSubTasks(system, uncompleted_task_list, full_tasklist):
    temp_task_list = []
    for task_name in full_tasklist:
        task = system.returnTask(task_name)
        task_pred = task.returnPredecessors()
        isTaskValid = True
        for pred in task_pred:
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


def cycleTimeCounter(system, station):
    # The assumption is that precedence rule has already been applied for the station and the system as a whole
    max_system_cycle_time = system.returnCycleTime()
    task_list = system.returnTaskListByStation(station)
    task_list.sort()
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
    # Initialize the cycle time counter, human resource counter, robot resource counter
    cycle_time = 0.0
    can_process_hrc = True
    # Create temporary human time and robot time
    human_cycle_time = 0.0
    robot_cycle_time = 0.0
    # The loop will go on until every task in the station is completed
    while len(uncompleted_task_list) != 0:
        # Get only the tasks that are posssible to complete from each list
        hrc_subtasks = getValidSubTasks(
            system, uncompleted_task_list, hrc_tasks)
        # Prioritizes HRC tasks over R and H tasks. Only search for R and H tasks if there are no HRC tasks to complete
        if len(hrc_subtasks) != 0 and can_process_hrc:
            if human_cycle_time > 0.0 or robot_cycle_time > 0.0: # To prevent negative addition
                cycle_time += max(human_cycle_time, robot_cycle_time)
                human_cycle_time = 0.0
                robot_cycle_time = 0.0
            # Get the task that can be completed with the least cost
            hrc_task, hrc_task_cost = findMinimumCost(system, hrc_subtasks)
            cycle_time += hrc_task_cost
            uncompleted_task_list.remove(hrc_task)
            hrc_tasks.remove(hrc_task)
        else:
            # To process R tasks:
            r_subtasks = getValidSubTasks(system, uncompleted_task_list, r_tasks)
            r_task, r_task_cost = findMinimumCost(system, r_subtasks)
            robot_cycle_time += r_task_cost
            uncompleted_task_list.remove(r_task)
            r_tasks.remove(r_task)
            # To process H tasks:
            h_subtasks = getValidSubTasks(system, uncompleted_task_list, h_tasks)
            h_task, h_task_cost = findMinimumCost(system, h_subtasks)
            human_cycle_time += h_task_cost
            uncompleted_task_list.remove(h_task)
            h_tasks.remove(h_task)
        if human_cycle_time == robot_cycle_time:
            can_process_hrc = True
        else:
            can_process_hrc = False
    