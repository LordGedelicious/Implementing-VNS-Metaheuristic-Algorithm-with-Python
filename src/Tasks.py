from Models import Model


class Task:
    # Constructor function
    def __init__(self, task_name, max_models):
        self.task_name = task_name
        self.max_models = max_models
        self.models = []
        self.predecessors = []

    # Add a model to the task
    def addModel(self, model):
        if (self.models.__len__() < self.max_models):
            self.models.append(model)
        else:
            print("Error: Task " + self.task_name + " is full.")

    # Add successor tasks to Task
    def addSuccessors(self, successor):
        self.successors.append(successor)
