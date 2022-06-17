from itertools import count
from numpy import integer
from Tasks import *
from Models import *
from Reader import *
from System import *
from StartImprovement import *
from Shaking import *

def countTotalCost(system, partitions):
    # TODO: Temporary fix for the total cost
    total_cost = 0
    for i in partitions:
        total_cost += system.returnCost(i)
    return total_cost