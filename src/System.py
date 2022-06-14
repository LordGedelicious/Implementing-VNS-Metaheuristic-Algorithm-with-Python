from numpy import integer
from Tasks import *
from Models import *
from Reader import *


class System:
    # Constructor function
    def __init__(self):
        self.list_tasks = []
        self.list_task_names = []
        self.list_stations = []
        self.list_starting_tasks = []
        self.num_of_stations = 0
        self.cycle_time = 0
        self.s_value = 0
        self.a_value = 0

    def addTask(self, task):
        print("Adding task {}".format(task.returnTaskName()))
        temp_predecessors = task.returnPredecessors()
        for i in temp_predecessors:
            print("Predecessor of {} is {}".format(task.returnTaskName(), i))
            if i in self.list_task_names:
                prev_predecessors = self.returnTask(i).returnPredecessors()
                print("Previous predecessors of {} is {}".format(
                    i, prev_predecessors))
                if (len(prev_predecessors) != 0):
                    for j in prev_predecessors:
                        print("Adding predecessor {} to {}".format(j, i))
                        if j not in temp_predecessors:
                            temp_predecessors.insert(0, j)
        task.setPredecessors(temp_predecessors)
        self.list_task_names.append(task.returnTaskName())
        self.list_tasks.append(task)
        temp_station = task.returnOriginStation()
        if temp_station not in self.list_stations:
            self.list_stations.append(temp_station)
            self.num_of_stations += 1
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
            i.returnModels()
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
