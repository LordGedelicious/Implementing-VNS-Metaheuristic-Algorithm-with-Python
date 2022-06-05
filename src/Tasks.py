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


class MainSystem:
    # Constructor function
    def __init__(self):
        self.list_tasks = []

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

    def returnTask(self, task_name):
        try:
            index = self.list_tasks.index(task_name)
            return self.list_tasks[index]
        except ValueError:
            print("index not found!")
            return -1

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
