import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-q", "--numberOfQueues", default=3,
                help="number of queues", type=int)

ap.add_argument("-l", "--jobList",
                help="burst1:arrivalTime1:IOFreq1,burst2:arrivalTime2:IOFreq2")

ap.add_argument("-b", "--boost", default=True,
                help="", type=bool)

args = vars(ap.parse_args())

boost = args["boost"]
number_of_queues = args["numberOfQueues"]
jobs = str(args["jobList"]).split(",")

for job in jobs:
    job = 

class Player:
    def __init__(self):
        self.turn
    def mudsd(self):
