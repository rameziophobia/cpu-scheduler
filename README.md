# CPU MLFQ Scheduler
CPU scheduler simulator written in python, utilizing PySimpleGUI framework, simulates a MLFQ MultiLevel Feedback Queue with configurable scheduling algorithms for each level.
## Prerequisites
install Pysimplegui via pip
* pip install PySimpleGUI
## Built with
* Python
* PySimpleGUI - gui framework
* Pycharm - IDE
## Usage
the simulator accepts input via the command line then displays the gui output
### Parameters
* "-q" or "--quantumList" followed by a comma separated list of quantums for each Round roben level "q1,q2,q3, ..."
  * ex: "-q 8, 16, 24"
* "-l" or "--jobList" followed by a comma seperated list of jobs to be scheduled in the format "burstTime:arrivalTime"
  * ex: "-l 24:3, 26:17, 42:7"
* write "-b" or "--boost" followed by one integer, default 0 (no boost) the algorithm boosts all jobs in all queues each period b as a form of aging to avoid process starvation
### Examples
#### Example 1
python main.py  -q 5,10,15 -l 10:24, 16:4, 17:19, 23:18, 32:3, 16:16, 4:55

![Example1](/docImages/example1.png)

#### Example 2 - using default queues
python main.py -l 10:24, 29:4, 37:19, 23:18, 32:3

![Example2](/docImages/example2.png)

#### Example 3 - with boosting
python main.py -b 100 -q 3,7,10 -l 10:24, 29:4, 37:19, 23:18, 32:3 

![Example3](/docImages/example3.png)

## License
this project  is licensed under the MIT license
