from numpy import integer
from Tasks import *
from Models import *
from Reader import *

import sys

class System:
    # Constructor function
    def __init__(self):
        self.list_tasks = [] # List of Task objects
        self.list_task_names = [] # List of Task objects' names
        self.list_stations = [] # List of station names in the system
        self.list_starting_tasks = [] # List of starting tasks (Tasks that have no predecessors)
        self.cycle_time = 0 # Integer, the cycle time of the system
        self.s_value = 0 # Integer, the s value of the system (shaking 1st point maximum attempts)
        self.a_value = 0 # Integer, the a value of the system (localsearch maximum attempts increment/decrement)

    def addTask(self, task):
        task_predecessors = task.returnPredecessors()
        if not task_predecessors: # Check empty list
            print("Task {} is a starting task. No predecessors available".format(task.returnTaskName()))
            new_predecessors = []
        else:
            new_predecessors_length = 0
            for i in task_predecessors:
                direct_predecessor = self.returnTask(i)
                if direct_predecessor is None:
                    sys.exit("Error: Task {} is not in the system. \nPlease fix the csv file".format(task_predecessors[i]))
                new_predecessors_length += direct_predecessor.returnNumOfPredecessors()
            new_predecessors = [[] for i in range(0, new_predecessors_length)]
            print("Predecessors of task {} are {}".format(task.returnTaskName(), task_predecessors))
            print("Length of new predecessors is {}\n".format(new_predecessors_length))
            current_position = 0
            while current_position < new_predecessors_length:
                for i in task_predecessors:
                    direct_predecessor = self.returnTask(i)
                    print("Number of predecessors of {} is {}".format(i, direct_predecessor.returnNumOfPredecessors()))
                    for j in range(0, direct_predecessor.returnNumOfPredecessors()):
                        new_predecessors[current_position] = direct_predecessor.returnPredecessors()[j]
                        current_position += 1
        # temp_predecessors = task.returnPredecessors()
        # max_length = len(temp_predecessors) if len(temp_predecessors) > len
        # new_predecessors = [[] for i in range(0, len(temp_predecessors))]
        # for i in range (0, len(temp_predecessors)):
        #     direct_predecessor = self.returnTask(temp_predecessors[i])
        #     if direct_predecessor is None:
        #         sys.exit("Error: Task {} is not in the system. \nPlease fix the csv file".format(temp_predecessors[i]))
        #     old_predecessors = direct_predecessor.returnPredecessors()
        #     for j in range(0, len(old_predecessors)):
        #         new_predecessors[j] = old_predecessors[j]
        #     new_predecessors[i].append(temp_predecessors[i])
        task.setPredecessors(new_predecessors)
        self.list_task_names.append(task.returnTaskName())
        self.list_tasks.append(task)
        temp_station = task.returnOriginStation()
        if temp_station not in self.list_stations:
            self.list_stations.append(temp_station)
        if task.returnPredecessors() == []:
            self.list_starting_tasks.append(task.returnTaskName())

    def setCycleTime(self, cycle_time):
        self.cycle_time = cycle_time

    def returnCycleTime(self):
        return self.cycle_time

    def returnTaskNames(self):
        list_of_task_names = []
        for i in self.list_tasks:
            list_of_task_names.append(i.returnTaskName())
        return list_of_task_names

    def returnTask(self, task_name):
        for i in self.list_tasks:
            if i.returnTaskName() == task_name:
                return i
        return None

    def returnStationFromTask(self, task_name):
        task = self.returnTask(task_name)
        return task.returnOriginStation()

    def returnPredecessors(self, task_name):
        task = self.returnTask(task_name)
        return task.returnPredecessors()

    def returnStartingTasks(self):
        return self.list_starting_tasks

    def printContents(self):
        for i in self.list_tasks:
            print("Task name is {}".format(i.returnTaskName()))
            print("Number of model in task is {}".format(i.returnMaxModels()))
            print("List of models in task:")
            i.printModels()
            print("Predecessors of this task: {}".format(i.returnPredecessors()))
            print("From early solution, the task's initial solution is {}".format(
                i.returnInitialSolution()))
            print("This task belongs to the {} station".format(
                i.returnOriginStation()))
            print()
        print("The system's starting tasks are {}".format(
            self.returnStartingTasks()))
        print("The system's cycle time is {} unit of time.".format(
            self.returnCycleTime()))
