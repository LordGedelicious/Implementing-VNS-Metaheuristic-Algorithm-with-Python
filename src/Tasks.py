from Models import Model


class Task:
    def __init__(self, task_name, max_models):
        self.task_name = task_name
        self.max_models = max_models
        self.models = []
        # self.predecessors = []
        self.successors = []

    def addModel(self, model):
        if (self.models.__len__() < self.max_models):
            self.models.append(model)
        else:
            print("Error: Task " + self.task_name + " is full.")

    def addSuccessors(self, successor):
        self.successors.append(successor)
