from itertools import count
from numpy import integer
from Tasks import *
from Models import *
from Reader import *
from System import *
from StartImprovement import *
from Helper import *
from LocalSearch import *
from StationAllocation import *
from OperatorSwitch import *

import os
# other imports


def doesFilenameExist(filename):
    path_to_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'testcase'))
    path_to_file = os.path.abspath(os.path.join(path_to_folder, filename))
    return os.path.isfile(path_to_file)

def main():
    main_system = System()
    bool_FilenameExist = False
    while not bool_FilenameExist:
        src_testcase_file = input(
            "Enter the name of the testcase file (include the .csv extension): ")
        bool_FilenameExist = doesFilenameExist(src_testcase_file)
    num_of_models = 0
    while num_of_models <= 0:
        num_of_models = int(input("Input the number of models for each task in the system: "))
    main_system.setNumOfModels(num_of_models)
    ReadFile(src_testcase_file, main_system)
    system_cycle_time = 0
    s_value = 0
    a_value = 0
    while system_cycle_time <= 0 or s_value <= 0 or a_value <= 0:
        system_cycle_time = int(input("Enter the system cycle time: "))
        s_value = int(input("Enter the system's s_value: "))
        a_value = int(input("Enter the system's a_value: "))
        if system_cycle_time <= 0 or s_value <= 0 or a_value <= 0:
            print("Invalid input (time and value must be larger than 0 and whole number). Please try again.")
    main_system.setInvestmentCostHuman(int(input("Enter the investment cost of the human resource: ")))
    main_system.setInvestmentCostRobot(int(input("Enter the investment cost of the robot resource: ")))
    main_system.setOperationalCostHuman(int(input("Enter the operational cost of the human resource: ")))
    main_system.setOperationalCostRobot(int(input("Enter the operational cost of the robot resource: ")))
    main_system.setNumOfProducts(int(input("Enter the number of products to be produced: ")))
    print()
    main_system.setCycleTime(system_cycle_time)
    main_system.setSValue(s_value)
    main_system.setAValue(a_value)
    main_system.printContents()
    print("The initial total cost of the system is {}".format(main_system.countTotalCost()))
    haltProgress()
    partitions = StartImprovement(main_system)
    ref_system = copy.deepcopy(main_system)
    for partition in partitions:
        isOldSystemBetter = False
        print("Partition: {}".format(partition))
        while not isOldSystemBetter:
            changed_system = copy.deepcopy(ref_system)
            print("Attempting Shaking process...")
            haltProgress()
            changed_system = startShaking(changed_system, partition)
            print("Next, attempting operator switch...")
            haltProgress()
            changed_system = startOperatorSwitch(changed_system, partition)
            print("\nOperator Switching process complete.")
            print("Next, attempting station allocation...")
            haltProgress()
            changed_system = startStationAllocation(changed_system, partition)
            print("\nStation Allocation process complete.")
            print("Comparing original system's cost with the changed system's cost...")
            haltProgress()
            old_system_cost = ref_system.countTotalCost()
            changed_system_cost = changed_system.countTotalCost()
            if old_system_cost < changed_system_cost:
                print("The changed system is better than the original system.")
                print("Attempting to repeat the entire process from start...")
                isOldSystemBetter = False
                ref_system = copy.deepcopy(changed_system)
                haltProgress()
            else:
                print("The original system is better than the changed system.")
                isOldSystemBetter = True
                print("Moving on to the next partition...")
                haltProgress()
    print("The final total cost of the system is {}".format(ref_system.countTotalCost()))
    print("Final composition of the system:")
    ref_system.printContents()
main()
