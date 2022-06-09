from numpy import integer
from Tasks import *
from Models import *
from Reader import *
from System import *
from StartImprovement import *

import copy


def checkIfSameStationRule(system, task_a, task_b):
    # Return True if the two tasks are from the same station
    if system.returnStationFromTask(task_a) == system.returnStationFromTask(task_b):
        return True
    return False


def checkIfPrecedenceRule(system, partition):
    pass


def startShaking(system, partitions):
    for i in partitions:
        print(i)
