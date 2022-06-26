# Implementing-VNS-Metaheuristic-Algorithm-with-Python-Program

## Daftar Isi
- [Description](#description)
- [How to Use](#howtouse)
- [Programmer Identity](#programmer)

## Deskripsi
The program contains within is part of a HMIF ITB's IT Incubator's project.

The program implements the Variable Neighborhood Search (VNS) Metaheuristic Program as given by the flowchart in the `project_info` folder.The program accepts a csv file contains all tasks with all models, each with a list of direct predecessor and successors. The benefit for each task for using R or HRC resource must be listed in the csv file as well. 

The program outputs the final state of the system, complete with the final cost.

The directory contain the following files and folders:
```
├── project_info   [contains information about the project]
├── src            [contains source code to the project]
    ├── __pycache__            [contains python prerequisites for the project]
    ├── Helper.py              [contains helper functions and rules to implement]
    ├── LocalSearch.py         [contains functions to perform Local Search process]
    ├── Main.py                [contains main function to perform all functions in the VNS algorithm program]
    ├── Models.py              [contains class template to create models for tasks]
    ├── OperatorSwitch.py      [contains functions to perform Operator Switch process]
    ├── Reader.py              [contains functions to read csv file and parse data]
    ├── Shaking.py             [contains functions to perform Shaking process]
    ├── StartImprovement.py    [contains functions to perform Start Improvement process]
    ├── StationAllocation.py   [contains functions to Station Allocation process]
    ├── System.py              [contains class template to create system that can contain tasks and models]
    ├── Tasks.py               [contains class template to create tasks that can store models]
├── testcase       [contains correct and incorrect testcases]
    ├── testcase1.csv
    ├── testcase2_false.csv
    ├── testcase2.csv
    ├── testcase3_false.csv
    ├── testcase3.csv
```

## How To Use
**[IMPORTANT]** Make sure Python 3.9 or above is installed in your system. Clone the repository into your computer system.

Two ways to run the program:
1. Using Batch File
+ Edit the run.bat file.
+ The run.bat file has the following structure:
```
@echo off
<path to the python.exe> <path to the Main.py file in the src folder>
pause
```
+ Change the path to the python.exe and Main.py to the path of the files in your system
+ Double click the run.bat file in the file explorer
+ Input necessary information about the system
+ Run the program as the prompt says

2. Using Manual Python Script Manually
+ Open the src folder inside the main folder
+ Open Terminal on that directory
+ Type and run `py Main.py`
+ Input necessary information about the system
+ Run the program as the prompt says

## Programmer
- <a href = "https://github.com/LordGedelicious">Gede Prasidha Bhawarnawa (13520004)</a>
