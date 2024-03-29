from Tasks import *
from Models import *
from Reader import *
from System import *
from Helper import *
from OperatorSwitch import *

import copy
import time

def startStationAllocation(system, partition):
    # This function will attempt to allocate all tasks in the partition to stations
    # Station will first be ordered ascendingly from the least remaining cycle time to the most remaining cycle time
    # Tasks from stations with lower priority can be moved to stations with higher priority but not the other way around.
    start_time = time.time()
    task_list_in_partition = copy.deepcopy(partition)
    station_list_in_partition = []
    station_list_in_system = system.returnStationList()
    for task_name in task_list_in_partition:
        task = system.returnTask(task_name)
        task_station = task.returnOriginStation()
        if task_station not in station_list_in_partition:
            station_list_in_partition.append(task_station)
    station_list_ordered = sortStationList(system, station_list_in_partition)
    cant_be_moved_tasks = []
    checked_station_list = []
    for station_list_idx in range(len(station_list_ordered)):
        ref_station = station_list_ordered[station_list_idx][0]
        tasks_in_ref_station = system.returnTaskListByStation(ref_station)
        for task_name in tasks_in_ref_station:
            cant_be_moved_tasks.append(task_name)
        for task_name in task_list_in_partition:
            ref_task = system.returnTask(task_name)
            ref_task_station = copy.deepcopy(ref_task.returnOriginStation())
            if checkIfSameStation(system, task_name, ref_station):
                print("Task {} can't be inserted into station {} because task {} is already there.".format(task_name, ref_station, task_name))
                continue
            if task_name in cant_be_moved_tasks or ref_task_station in checked_station_list:
                print("Task {} can't be inserted into station {} because task {} has higher r_value of priority.".format(task_name, ref_station, task_name))
            ref_task.setOriginStation(ref_station)
            isFailPrecedenceCheck = True
            isFailCycleTimeCheck = True
            for station in station_list_in_system:
                if not isFailPrecedenceCheck and not isFailCycleTimeCheck:
                    break
                if not checkPrecedenceRule(system, station):
                    isFailPrecedenceCheck = False
                if not checkCycleTimeRule(system, station, True):
                    isFailCycleTimeCheck = False
            if not isFailPrecedenceCheck:
                ref_task.setOriginStation(ref_task_station)
                print("Task {} can't be inserted into station {} because of precedence rule violation.".format(task_name, ref_station))
                continue
            if not isFailCycleTimeCheck:
                ref_task.setOriginStation(ref_task_station)
                print("Task {} can't be inserted into station {} because of Cycle Time rule violation.".format(task_name, ref_station))
                continue
            print("Task {} is now inserted into station {}.".format(task_name, ref_station))
        checked_station_list.append(ref_station)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Elapsed time for station allocation: {0:.3f} seconds".format(elapsed_time))
    print("Total cost of the system now is: {}".format(system.countTotalCost()))
    return system, elapsed_time

def sortStationList(system, station_list):
    temp_storage = [] # Fill this with lists of [A,B] with A being the station name and B being the station's remainder cycle time
    max_time = system.returnCycleTime() * system.returnNumOfModels()
    for station in station_list:
        new_list = [station]
        station_cycle_time = checkCycleTimeRule(system, station, False)
        total_time = 0
        for time in station_cycle_time:
            total_time += time
        new_list.append(max_time - total_time)
        temp_storage.append(new_list)
    temp_storage.sort(key=lambda x: x[1])
    print(temp_storage)
    return temp_storage