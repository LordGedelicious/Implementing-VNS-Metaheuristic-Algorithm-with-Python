from itertools import count
from numpy import integer
from Tasks import *
from Models import *
from Reader import *
from System import *
from StartImprovement import *

import copy


def sortPredecessorsListBasedOnPredecessorsLength(system, partition):
    # Using bubble sort to sort the predecessors list based on the length of the predecessors list descendingly
    new_list = copy.deepcopy(partition)
    while True:
        count_swaps = 0
        for i in range(len(new_list) - 1):
            if len(system.returnPredecessors(new_list[i])) < len(system.returnPredecessors(new_list[i + 1])):
                new_list[i], new_list[i + 1] = new_list[i + 1], new_list[i]
                count_swaps += 1
        if count_swaps == 0:
            break
    return new_list


def checkIfSameStationRule(system, task_a, task_b):
    # Return True if the two tasks are from the same station
    if system.returnStationFromTask(task_a) == system.returnStationFromTask(task_b):
        return True
    return False


def checkIfPrecedenceRule(system, partition):
    starting_tasks = system.returnStartingTasks()
    bool_first_checking = True
    for i in partition:
        if system.returnStationFromTask(i) == []:
            continue
        elif len(system.returnPredecessors(i)) == 1 and system.returnPredecessors(i)[0] in starting_tasks:
            continue
        else:
            bool_first_checking = False
            break
    if not bool_first_checking:
        bool_second_checking = True
        # Sort is based on the length of the predecessors list
        sorted_partition = sortPredecessorsListBasedOnPredecessorsLength(
            system, partition)
        for i in range(0, len(sorted_partition)):
            for j in range(len(sorted_partition) - 1, j, -1):
                if j in system.returnPredecessors(i):
                    continue
                else:
                    bool_second_checking = False
                    break
        if not bool_second_checking:
            bool_third_checking = True
            for i in partition:
                for j in system.returnPredecessors(i):
                    if j in starting_tasks:
                        bool_third_checking = True
                        break
                    else:
                        bool_third_checking = False
                        continue
            if not bool_third_checking:
                # TODO: Cek kalau gabungan aturan aturan di atas
                pass
    return True


def startShaking(system, partitions):
    for i in partitions:
        print(i)
