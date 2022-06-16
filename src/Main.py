from numpy import integer
from Tasks import *
from Models import *
from Reader import *
from System import *
from StartImprovement import *

import os
# other imports


def doesFilenameExist(filename):
    path_to_folder = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'testcase'))
    path_to_file = os.path.abspath(os.path.join(path_to_folder, filename))
    return os.path.isfile(path_to_file)


def main():
    main_system = System()
    bool_FilenameExist = False
    while not bool_FilenameExist:
        src_testcase_file = input(
            "Enter the name of the testcase file (include the .csv extension): ")
        bool_FilenameExist = doesFilenameExist(src_testcase_file)
    ReadFile(src_testcase_file, main_system)
    system_cycle_time = 0
    s_value = 0
    a_value = 0
    while system_cycle_time <= 0 or s_value <= 0 or a_value <= 0:
        system_cycle_time = int(input("Enter the system cycle time: "))
        s_value = int(input("Enter the system's s_value: "))
        a_value = int(input("Enter the system's a_value: "))
        if system_cycle_time <= 0 or s_value <= 0 or a_value <= 0:
            print("Invalid input. Please try again.")
    main_system.setCycleTime(system_cycle_time)
    main_system.setSValue(s_value)
    main_system.setAValue(a_value)
    main_system.printContents()
    StartImprovement(main_system)


main()
