from Models import Model


class Task:
    # Constructor function
    def __init__(self, task_name, max_models):
        self.task_name = task_name  # Name of the task, numerical identifier
        self.max_models = max_models  # Maximum number of models that can be added to the task
        self.models = []  # Contain models of a single task
        self.num_of_predecessors = 0  # Number of predecessors of the task (before converted to full list)
        self.direct_predecessors = []  # List of direct predecessors of the task
        self.num_of_successors = 0  # Number of successors of the task (before converted to full list)
        self.direct_successors = []  # List of direct successors of the task
        self.predecessors = []  # Predecessors is a list type (full list from starting tasks)
        # Initial Solution is a string type, either use "H" for human or "R" for robot or "HRC" for human and robot
        self.initial_solution = None
        # Origin Station is a char (string) type, of a single alphabet. Since the limitations are from 25 to 40 tasks and a single station must contain more than one task, 26 letters of the alphabet is sufficient
        self.originStation = None
        self.benefit_R = 0  # benefit of the task for robot
        self.benefit_HRC = 0  # benefit of the task for human and robot combo

    # Add a model to the task
    # Model will be only added if the maximum number of models is not reached
    def addModel(self, model):
        if (self.models.__len__() < self.max_models):
            self.models.append(model)
        else:
            print("Error: Task " + self.task_name + " is full.")

    # Set successor tasks, initial solution, and origin station to Task object
    # Predecessors are tasks that must be completed before this task can be completed
    def setPredecessors(self, predecessor):
        self.predecessors = predecessor
        
    def setDirectPredecessors(self, direct_predecessors):
        self.direct_predecessors = direct_predecessors
    
    def setDirectSuccessors(self, direct_successors):
        self.direct_successors = direct_successors

    # Initial Solution is a selected method to do all the work in every model for a given task
    def setInitialSolution(self, initial_solution):
        self.initial_solution = initial_solution

    # Origin Station is the station that the task is grouped in, determined from the input
    def setOriginStation(self, originStation):
        self.originStation = originStation

    # Number of predecessors is the number of direct tasks that is a predecessors of the reference task
    def setNumOfPredecessors(self, num_of_predecessors):
        self.num_of_predecessors = num_of_predecessors
        
    def setNumOfSuccessors(self, num_of_successors):
        # Set the number of successors of the task
        self.num_of_successors = num_of_successors
    
    # Benefit_R is the benefit cost for using robot to perform the task
    def setBenefitR(self, benefit_R):
        # Set the benefit of the task for robot
        self.benefit_R = benefit_R
    
    # Benefit_HRC is the benefit cost for using human and robot to perform the task
    def setBenefitHRC(self, benefit_HRC):
        # Set the benefit of the task for human and robot combo
        self.benefit_HRC = benefit_HRC
    
    # Getter functions
    def returnTaskName(self):
        # Returns integer as the task's name
        return self.task_name
    
    def returnNumOfPredecessors(self):
        # Returns integer as the number of direct predecessors
        return self.num_of_predecessors
    
    def returnDirectPredecessors(self):
        # Returns list of integer as the list of direct predecessor tasks' names
        return self.direct_predecessors
    
    def returnDirectSuccessors(self):
        # Returns list of integer as the list of direct successor tasks' names
        return self.direct_successors

    def returnNumOfSuccessors(self):
        # Returns integer as the number of direct successors
        return self.num_of_successors

    def returnMaxModels(self):
        # Returns integer as the maximum number of models that can be added to the task
        return self.max_models

    def returnModel(self, model_name):
        # Return Model object with the given model name
        try:
            for i in self.models:
                if i.returnModelName() == model_name:
                    return i
        except:
            print("Error: Model " + model_name + " does not exist.")
    
    def returnAllModels(self):
        return self.models

    def returnPredecessors(self):
        # Returns list of integer as the list of predecessor tasks' names
        return self.predecessors

    def returnInitialSolution(self):
        # Returns char (string) type as the initial solution
        return self.initial_solution

    def returnOriginStation(self):
        # Returns char (string) type as the origin station
        return self.originStation
    
    def returnBenefitR(self):
        # Returns integer as the benefit cost for using robot to perform the task
        return self.benefit_R
    
    def returnBenefitHRC(self):
        # Returns integer as the benefit cost for using human and robot to perform the task
        return self.benefit_HRC

    def switchStations(self, task_name):
        # Switch station for two tasks
        temp_station_a, temp_station_b = self.returnOriginStation(), task_name.returnOriginStation()
        self.setOriginStation(temp_station_b)
        task_name.setOriginStation(temp_station_a)

    def printModels(self):
        # Prints the task's models' info
        for i in self.models:
            print("Model name is {}".format(i.returnModelName()))
            print("Model's human cost is {}".format(i.returnHumanCost()))
            print("Model's machine cost is {}".format(i.returnMachineCost()))
            print("Model's hrc cost is {}".format(i.returnComboCost()))
    
    def isolateModelCosts(self, initial_solution):
        # Isolate the model costs from the task's models
        model_costs = []
        for model in self.returnAllModels():
            model_costs.append(model.returnHumanCost()) if initial_solution == 'H' else None
            model_costs.append(model.returnMachineCost()) if initial_solution == 'R' else None
            model_costs.append(model.returnComboCost()) if initial_solution == 'HRC' else None
        return model_costs
