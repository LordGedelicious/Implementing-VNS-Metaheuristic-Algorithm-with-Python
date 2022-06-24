from numpy import integer
from Tasks import *
from Models import *
from Reader import *
from System import *
from Shaking import *


def checkKValueContents(system, partitions, k_value):
    # Check if every partition of the system has tasks from at least two different stations
    # Assumed that the user understands the graph structure of the system
    for i in range(0, k_value + 1):
        current_partition = partitions[i]
        list_stations = []
        for j in current_partition:
            station_of_j = system.returnStationFromTask(j)
            if station_of_j not in list_stations:
                list_stations.append(station_of_j)
        if len(list_stations) < 2:
            print("Partition {} has less than 2 stations".format(i))
            return False
    return True


def StartImprovement(system):
    # main_system.printContents()
    k_value = 0
    while k_value <= 0:
        k_value = int(input("Enter the value of k (must be greater than 0): "))
    print("You may insert elements for the partitions.\nPlease note that 1 task may only exist at 1 given partition at any given time.")
    print("Example input for partition X: 'task1 task2 task3' (space-separated)")
    isPartitionComplete = False
    while not isPartitionComplete:
        try:
            list_of_partitionable_tasks = copy.deepcopy(system.returnTaskNames())
            print(list_of_partitionable_tasks)
            partitions = [[] for i in range(0, k_value + 1)]
            for i in range(0, k_value):
                partition_contents = input("Insert contents for partition {} :".format(i+1))
                for j in partition_contents.split():
                    val_j = int(j)
                    list_of_partitionable_tasks.remove(val_j)
                    partitions[i].append(val_j)
            partitions[k_value] = list_of_partitionable_tasks
            if checkKValueContents(system, partitions, k_value):
                isPartitionComplete = True
        except ValueError as error:
            print(error)
            print("You inserted a task more than once, try again")
            isPartitionComplete = False
    # Check if every partition of the system has tasks from at least two different stations
    print("Current State of Partitions:")
    for i in range(0, k_value + 1):
        print(partitions[i])
    for partition in partitions:
        print("Current partition: {}".format(partition))
        print("Current tasks in system: {}".format(system.returnTaskNames()))
        startShaking(system, partition)
