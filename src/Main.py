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
    main_system.printContents()
    StartImprovement(main_system)


main()
