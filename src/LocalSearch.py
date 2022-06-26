from Tasks import *
from Models import *
from Reader import *
from System import *
from StartImprovement import *
from Helper import *
from StationAllocation import *
from OperatorSwitch import *

# Needs copy module to deep copy the system
import copy
import random

def LocalSearch(system, first_point, second_point, initial_cost):
    # System, is the original system
    # First and second point is the two tasks that are switched successfully in the shaking process
    # Initial cost is the cost of the shaking process
    temp_storage = [first_point,second_point]
    reference_point = random.choice(temp_storage)
    reference_task = system.returnTask(reference_point)
    task_list = system.returnTaskNames()
    temp_storage.remove(reference_point)
    print("\nReference point: {}".format(reference_point))
    a_value = system.returnAValue()
    plus_one_task_name = copy.deepcopy(reference_point)
    minus_one_task_name = copy.deepcopy(reference_point)
    store_valid_moves = []
    while a_value > 0:
        plus_one_task_name += 1
        if plus_one_task_name in task_list:
            print("Attempt to swap task {} with task {}".format(reference_point, plus_one_task_name))
            plus_one_task = system.returnTask(plus_one_task_name)
            isSwitchPlusOnePossible = True
            if checkIfSameStationRule(system, plus_one_task_name, reference_point):
                print("Invalid. Task {} and {} are in the same station".format(plus_one_task_name, reference_point))
                isSwitchPlusOnePossible = False
            if plus_one_task_name == temp_storage[0]:
                print("Invalid. Task {} is the same as the other point".format(plus_one_task_name)) 
                isSwitchPlusOnePossible = False
            if isSwitchPlusOnePossible:
                system.switchStationsOfTwoTasks(plus_one_task, reference_task)
                isValidSwitch = True
                for station in system.returnStationList():
                    if not checkPrecedenceRule(system, station):
                        print("Invalid. Precedence Rule is violated when switching {} with {}.".format(plus_one_task_name, reference_point))
                        isValidSwitch = False
                        break
                    if not checkCycleTimeRule(system, station, True):
                        print("Invalid. Cycle Time Rule is violated when switching {} with {}.".format(plus_one_task_name, reference_point))
                        isValidSwitch = False
                        break
                if not isValidSwitch:
                    system.switchStationsOfTwoTasks(plus_one_task, reference_task)
                else:
                    new_cost = copy.deepcopy(system.countTotalCost())
                    temp_store_valid_moves = [plus_one_task_name, reference_point, new_cost]
                    print("Switch {} with {} is valid with new cost being {}.".format(plus_one_task_name, reference_point, new_cost))
                    store_valid_moves.append(temp_store_valid_moves)
                    system.switchStationsOfTwoTasks(plus_one_task, reference_task)
        else:
            print("Task {} does not exist".format(plus_one_task_name))
        minus_one_task_name -= 1
        if minus_one_task_name in task_list:
            print("Attempt to swap task {} with task {}".format(reference_point, minus_one_task_name))
            minus_one_task = system.returnTask(minus_one_task_name)
            isSwitchMinusOnePossible = True
            if checkIfSameStationRule(system, minus_one_task_name, reference_point):
                print("Invalid. Task {} and {} are in the same station".format(minus_one_task_name, reference_point))
                isSwitchMinusOnePossible = False
            if minus_one_task_name == temp_storage[0]:
                print("Invalid. Task {} is the same as the other point".format(minus_one_task_name)) 
                isSwitchMinusOnePossible = False
            if isSwitchMinusOnePossible:
                system.switchStationsOfTwoTasks(minus_one_task, reference_task)
                isValidSwitch = True
                for station in system.returnStationList():
                    if not checkPrecedenceRule(system, station):
                        print("Invalid. Precedence Rule is violated when switching {} with {}.".format(minus_one_task_name, reference_point))
                        isValidSwitch = False
                        break
                    if not checkCycleTimeRule(system, station, True):
                        print("Invalid. Cycle Time Rule is violated when switching {} with {}.".format(minus_one_task_name, reference_point))
                        isValidSwitch = False
                        break
                if not isValidSwitch:
                    system.switchStationsOfTwoTasks(minus_one_task, reference_task)
                else:
                    new_cost = copy.deepcopy(system.countTotalCost())
                    temp_store_valid_moves = [minus_one_task_name, reference_point, new_cost]
                    print("Switch {} with {} is valid with new cost being {}.".format(minus_one_task_name, reference_point, new_cost))
                    store_valid_moves.append(temp_store_valid_moves)
                    system.switchStationsOfTwoTasks(minus_one_task, reference_task)
        else:
            print("Task {} does not exist".format(minus_one_task_name))
        a_value -= 1
    # Find the best move
    store_valid_moves.sort(key=lambda row: row[2])
    best_move = store_valid_moves[0]
    shaking_first_point = first_point
    shaking_second_point = second_point
    shaking_initial_cost = initial_cost
    localSearch_first_point = best_move[0]
    localSearch_second_point = best_move[1]
    localSearch_initial_cost = best_move[2]
    if localSearch_initial_cost < shaking_initial_cost:
        first_point_task = system.returnTask(localSearch_first_point)
        second_point_task = system.returnTask(localSearch_second_point)
        system.switchStationsOfTwoTasks(first_point_task, second_point_task)
        print("\nLocal Search results will be used by switching {} with {} with final cost {}".format(localSearch_first_point, localSearch_second_point, localSearch_initial_cost))
    else:
        first_point_task = system.returnTask(shaking_first_point)
        second_point_task = system.returnTask(shaking_second_point)
        system.switchStationsOfTwoTasks(first_point_task, second_point_task)
        print("\nShaking results will be used by switching {} with {} with final cost {}".format(shaking_first_point, shaking_second_point, shaking_initial_cost))
    return system

