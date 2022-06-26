from itertools import count
from random import random
from numpy import integer
from Tasks import *
from Models import *
from Reader import *
from System import *
from StartImprovement import *
from Helper import *
from LocalSearch import *

import copy
import random
import time

def getStationListFromPartitions(system, partitions):
    station_list = []
    for task_name in partitions:
        task = system.returnTask(task_name)
        task_station = task.returnOriginStation()
        if task_station not in station_list:
            station_list.append(task_station)
    return station_list

def startShaking(system, partitions):
    start_time = time.time()
    s_value = system.returnSValue()
    station_list = system.returnStationList()
    initial_system_cost = copy.deepcopy(system.countTotalCost())
    tested_tasks = []
    shakingSuccess = False
    final_first_point = None
    final_second_point = None
    while s_value > 0:
        first_point = random.choice(partitions)
        while first_point in tested_tasks:
            first_point = random.choice(partitions)
        tested_tasks.append(first_point)
        print("Current attempted first point: {}".format(first_point))
        for possible_task in partitions:
            print("Current attempted second point: {}".format(possible_task))
            if possible_task == first_point:
                print("First point and second point is the same. Invalid.")
                continue
            first_point_task = system.returnTask(first_point)
            second_point_task = system.returnTask(possible_task)
            system.switchStationsOfTwoTasks(first_point_task, second_point_task)
            passAllRule = True
            for station in station_list:
                if not checkPrecedenceRule(system, station):
                    print("Switch between first_point and possible_task failed because violation of Precedence Rule.")
                    passAllRule = False
                    break
                if not checkCycleTimeRule(system, station, True):
                    # print(checkCycleTimeRule(system, station, False))
                    print("Switch between first_point and possible_task failed because violation of Cycle Time Rule.")
                    passAllRule = False
                    break
            if not singularStationRule(system, first_point, possible_task):
                print("Switch between first_point and possible_task failed because violation of Singular Station Rule.")
                passAllRule = False
            if checkIfSameStationRule(system, first_point, possible_task):
                print("Switch between first_point and possible_task failed because both tasks are from the same station.")
                passAllRule = False
            if not passAllRule:
                system.switchStationsOfTwoTasks(first_point_task, second_point_task)
                continue
            else:
                # Set s_value to 0 to stop the loop
                s_value = 0
                shakingSuccess = True
                final_first_point = first_point
                final_second_point = possible_task
                new_system_cost = copy.deepcopy(system.countTotalCost())
                system.switchStationsOfTwoTasks(first_point_task, second_point_task)
                break
        if shakingSuccess:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print("Successful shaking by switching {} and {} with cost being {}!".format(final_first_point, final_second_point, new_system_cost))
            print("Elapsed time for shaking process: {0:.3f} seconds".format(elapsed_time))
            print("Next, attempts to perform local search.")
            haltProgress()
            system, local_search_time = LocalSearch(system, final_first_point, final_second_point, new_system_cost)
            total_time = local_search_time + elapsed_time
            return system, local_search_time
        else:
            print("Shaking failed.\n")
            s_value -= 1
    end_time = time.time()
    total_time = end_time - start_time
    print("Elapsed time for shaking process: {0:.3f} seconds".format(total_time))
    return system, total_time
    
                
                
                
                
        
