from numpy import integer
from Tasks import *
from Models import *
from Reader import *
from Helper import *

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
        self.num_of_products = 0 # Integer, the number of products want to be produced by the system
        self.investment_cost_human = 0 # Integer, the investment cost of the human resources
        self.investment_cost_robot = 0 # Integer, the investment cost of the robot resources
        self.operational_cost_human = 0 # Integer, the operational cost of the human resources
        self.operational_cost_robot = 0 # Integer, the operational cost of the robot resources

    def addTask(self, task):
        starting_tasks = self.returnStartingTasks()
        task_predecessors = task.returnPredecessors()
        if not task_predecessors: # Check empty list
            new_predecessors = []
            new_predecessors_length = 0
        else:
            new_predecessors = []
            new_predecessors_length = 0
            for i in task_predecessors:
                direct_predecessor = self.returnTask(i)
                if direct_predecessor is None:
                    sys.exit("Error: Task {} is not in the system. \nPlease fix the csv file".format(task_predecessors[i]))
                if direct_predecessor.returnTaskName() in starting_tasks:
                    new_predecessors_length += 1
                    new_predecessors.append([direct_predecessor.returnTaskName()])
                else:
                    for j in direct_predecessor.returnPredecessors():
                        temp_pred_list = []
                        if j not in new_predecessors:
                            for k in j:
                                temp_pred_list.append(k)
                            temp_pred_list.append(direct_predecessor.returnTaskName())
                            new_predecessors.append(temp_pred_list)
                    new_predecessors_length += len(direct_predecessor.returnPredecessors())
            new_predecessors_length = max(new_predecessors_length, 1)
        task.setPredecessors(new_predecessors)
        self.list_task_names.append(task.returnTaskName())
        self.list_tasks.append(task)
        temp_station = task.returnOriginStation()
        if temp_station not in self.list_stations:
            self.list_stations.append(temp_station)
        if task.returnPredecessors() == []:
            self.list_starting_tasks.append(task.returnTaskName())

    def setInvestmentCostHuman(self, investment_cost_human):
        self.investment_cost_human = investment_cost_human
        
    def setInvestmentCostRobot(self, investment_cost_robot):
        self.investment_cost_robot = investment_cost_robot
        
    def setOperationalCostHuman(self, operational_cost_human):
        self.operational_cost_human = operational_cost_human
    
    def setOperationalCostRobot(self, operational_cost_robot):
        self.operational_cost_robot = operational_cost_robot
    
    def setNumOfProducts(self, num_of_products):
        self.num_of_products = num_of_products
    
    def setCycleTime(self, cycle_time):
        self.cycle_time = cycle_time
    
    def setSValue(self, s_value):
        self.s_value = s_value
    
    def setAValue(self, a_value):
        self.a_value = a_value

    def returnInvestmentCostHuman(self):
        return self.investment_cost_human

    def returnInvestmentCostRobot(self):
        return self.investment_cost_robot
    
    def returnOperationalCostHuman(self):
        return self.operational_cost_human
    
    def returnOperationalCostRobot(self):
        return self.operational_cost_robot
    
    def returnNumOfProducts(self):
        return self.num_of_products

    def returnCycleTime(self):
        return self.cycle_time
    
    def returnSValue(self):
        return self.s_value
    
    def returnAValue(self):
        return self.a_value

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
            print("R-Benefit of this task is {}".format(i.returnBenefitR()))
            print("HRC-Benefit of this task is {}".format(i.returnBenefitHRC()))
            print()
        print("The system's starting tasks are {}".format(
            self.returnStartingTasks()))
        print("All tasks that are in the system are {}".format(self.returnTaskNames()))
        print("The system's cycle time is {} unit of time.".format(
            self.returnCycleTime()))
        print("The system's s value is {}".format(self.returnSValue()))
        print("The system's a value is {}".format(self.returnAValue()))
        
