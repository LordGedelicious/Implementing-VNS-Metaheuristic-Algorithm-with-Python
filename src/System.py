from numpy import integer
from Tasks import *
from Models import *
from Reader import *


class System:
    # Constructor function
    def __init__(self):
        self.list_tasks = []
        self.list_stations = []
        self.num_of_stations = 0
        self.cycle_time = 0

    def addTask(self, task):
        temp_predecessors = task.returnPredecessors()
        for i in temp_predecessors:
            if i in self.list_tasks:
                prev_predecessors = self.returnTask(i).returnPredecessors()
                if (len(prev_predecessors) != 0):
                    for j in prev_predecessors:
                        if j not in temp_predecessors:
                            temp_predecessors.insert(0, j)
        task.setPredecessors(temp_predecessors)
        self.list_tasks.append(task)
        temp_station = task.returnOriginStation()
        if temp_station not in self.list_stations:
            self.list_stations.append(temp_station)
            self.num_of_stations += 1

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

    def printContents(self):
        for i in self.list_tasks:
            print("Task name is {}".format(i.returnTaskName()))
            print("Number of model in task is {}".format(i.returnMaxModels()))
            print("List of models in task:")
            i.returnModels()
            print("Predecessors of this task: {}".format(i.returnPredecessors()))
            print("From early solution, the task's initial solution is {}".format(
                i.returnInitialSolution()))
            print("This task belongs to the {} station".format(
                i.returnOriginStation()))
            print()
        print("The system's cycle time is {} unit of time.".format(
            self.returnCycleTime()))
