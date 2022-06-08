from Models import Model


class Task:
    # Constructor function
    def __init__(self, task_name, max_models):
        self.task_name = task_name
        self.max_models = max_models
        self.models = []
        self.predecessors = []
        self.initial_solution = None
        self.originStation = None

    # Add a model to the task
    def addModel(self, model):
        if (self.models.__len__() < self.max_models):
            self.models.append(model)
        else:
            print("Error: Task " + self.task_name + " is full.")

    # Set successor tasks, initial solution, and origin station to Task
    def setPredecessors(self, predecessor):
        self.predecessors = predecessor

    def setInitialSolution(self, initial_solution):
        self.initial_solution = initial_solution

    def setOriginStation(self, originStation):
        self.originStation = originStation

    def returnTaskName(self):
        return self.task_name

    def returnMaxModels(self):
        return self.max_models

    def returnModels(self):
        for i in self.models:
            print("Model name is {}".format(i.returnName()))
            print("Model's human cost is {}".format(i.returnHumanCost()))
            print("Model's machine cost is {}".format(i.returnMachineCost()))
            print("Model's hrc cost is {}".format(i.returnComboCost()))

    def returnPredecessors(self):
        return self.predecessors

    def returnInitialSolution(self):
        return self.initial_solution

    def returnOriginStation(self):
        return self.originStation
