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
import time

def LocalSearch(system, first_point, second_point, initial_cost):
    # System, is the original system
    # First and second point is the two tasks that are switched successfully in the shaking process
    # Initial cost is the cost of the shaking process
    start_time = time.time()
    shaking_first_point = copy.deepcopy(first_point)
    shaking_second_point = copy.deepcopy(second_point)
    shaking_initial_cost = copy.deepcopy(initial_cost)
    temp_storage = [first_point,second_point]
    # Reference point is the shaking point that is used to compare with the other possible shaking points
    # Second point is the point that will be incremented and decremented in the local search process
    # Reference point and second point are picked randomly
    reference_point = random.choice(temp_storage)
    reference_task = system.returnTask(reference_point)
    task_list = system.returnTaskNames()
    temp_storage.remove(reference_point)
    second_point = temp_storage[0]
    print("\nReference point (to be switched): {}".format(reference_point))
    print("Second point (for plus/minus one): {}".format(second_point))
    a_value = system.returnAValue()
    # plus_one_task_name and minus_one_task_name are the tasks that are incremented and decremented in the local search process
    plus_one_task_name = copy.deepcopy(second_point)
    minus_one_task_name = copy.deepcopy(second_point)
    # Store valid moves in the local search process
    # Store as list of [A,B,C] with A being the first point, B being the second point, and C being the cost of the move
    store_valid_moves = []
    # Conditions for a valid move:
    # 1. Precedence rule is still valid after the move
    # 2. Cycle time rule is still valid after the move
    # 3. Both tasks are not from the same station
    # 4. Both tasks are not the same task
    # 5. Both tasks are not from two singular stations
    # 6. Move is not the same as the shaking move
    while a_value > 0:
        plus_one_task_name += 1
        if plus_one_task_name in task_list:
            print("Attempt to swap task {} with task {}".format(reference_point, plus_one_task_name))
            plus_one_task = system.returnTask(plus_one_task_name)
            isSwitchPlusOnePossible = True
            if checkIfSameStationRule(system, plus_one_task_name, reference_point):
                print("Invalid. Task {} and {} are in the same station".format(plus_one_task_name, reference_point))
                isSwitchPlusOnePossible = False
            if plus_one_task_name == reference_point:
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
    # If there are multiple best moves, pick the best one (with the minimum cost)
    # IF there are no best moves, use the shaking results
    if len(store_valid_moves) == 0:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("No valid moves found")
        first_point_task = system.returnTask(shaking_first_point)
        second_point_task = system.returnTask(shaking_second_point)
        system.switchStationsOfTwoTasks(first_point_task, second_point_task)
        print("Elapsed time for local search process: {0:.3f} seconds".format(elapsed_time))
        print("\nShaking results will be used by switching {} with {} with final cost {}".format(shaking_first_point, shaking_second_point, shaking_initial_cost))
        return system
    store_valid_moves.sort(key=lambda row: row[2])
    best_move = store_valid_moves[0]
    localSearch_first_point = best_move[0]
    localSearch_second_point = best_move[1]
    localSearch_initial_cost = best_move[2]
    print("Local search minimum cost is {} by switching task {} and {}.".format(localSearch_initial_cost, localSearch_first_point, localSearch_second_point))
    print("Shaking cost is {} by switching task {} and {}.".format(shaking_initial_cost, shaking_first_point, shaking_second_point))
    # If the local search cost is less than the shaking cost, use the local search results
    # If not, use the shaking results
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
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Time for local search process: {0:.3f} seconds".format(elapsed_time))
    return system, elapsed_time

