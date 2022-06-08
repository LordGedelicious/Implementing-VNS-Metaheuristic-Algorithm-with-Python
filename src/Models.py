# for imports

class Model:
    # Constructor function
    # TODO: Tambahin Total Cost berdasarkan metode yang dipilih
    def __init__(self, origin_task, model_name, human, machine, combo):
        self.origin_task = origin_task  # the task that this model belongs to
        self.model_name = model_name  # the model name i.e. X, Y, Z etc.
        self.human_cost = human  # the human cost to do the model
        self.machine_cost = machine  # the machine cost to do the model
        self.combo_cost = combo  # the combo cost to do the model

    # Getter functions
    def returnName(self):
        return self.model_name

    def returnHumanCost(self):
        return self.human_cost

    def returnMachineCost(self):
        return self.machine_cost

    def returnComboCost(self):
        return self.combo_cost

    # Setter functions
    def setName(self, new_name):
        self.model_name = new_name

    def setHumanCost(self, new_human_cost):
        self.human_cost = new_human_cost

    def setMachineCost(self, new_machine_cost):
        self.machine_cost = new_machine_cost

    def setComboCost(self, new_combo_cost):
        self.combo_cost = new_combo_cost
