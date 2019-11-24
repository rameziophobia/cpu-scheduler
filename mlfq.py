import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--numberOfQueues", default=3,
                help="number of queues", type=int)

ap.add_argument("-q", "--quantumList", default="5,10",
                help="q1,q2,q3, ...", type=str)

ap.add_argument("-l", "--jobList", default="10:0:10,10:1:10",
                help="burst1:arrivalTime1:IOFreq1,burst2:arrivalTime2:IOFreq2, ...")

ap.add_argument("-b", "--boost", default=0,
                help="", type=int)

args = vars(ap.parse_args())

boost = args["boost"]
number_of_queues = args["numberOfQueues"]
jobs = str(args["jobList"]).split(",")
quantum_list = str(args["quantumList"]).split(",")
quantum_list = [int(quantum) for quantum in quantum_list]


def find_highest_priority_job(queues):
    for i in range(len(queues)):
        if len(queues[i].queue) == 0:
            continue
        return queues[i].queue[0]


class Mlfq:
    def __init__(self, number_of_queues, quantum_list):
        self.init_queues(number_of_queues, quantum_list)

    def init_queues(self, number_of_queues, quantum_list):
        pass


job_list = list()
finished_jobs = list()

queues = list()
for i in range(number_of_queues - 1):
    queues.append(Queue(i, quantum_list[i]))
queues.append(Queue(number_of_queues, -1))


def add_to_queue(current_time, priority):
    if process.arrival == current_time:
        queues[priority].queue.append(process)
    else:
        print(f"arrival is {process.arrival}, current time is {current_time}")


for job in jobs:
    burst, arrival, io_freq = job.split(":")

    process = Process(int(burst), int(arrival), int(io_freq))
    job_list.append(process)

    current_time = 0
    priority = 0
    add_to_queue(priority, current_time)

print(f"dsdsdsdsds {str(len(queues[0].queue))}")

print(queues[0].queue[0])
total_jobs = len(job_list)

# job_list.sort()

current_time = 0


def boost_available():
    if boost <= 0 or current_time == 0:
        return False
    return True


def boost_jobs():
    if current_time % boost == 0:
        for queue in queues:
            queue.queue.clear()
        for job in job_list:
            if not job.is_finished():
                queues[0].queue.append(job)


print(len(finished_jobs))
print(total_jobs)
while len(finished_jobs) < total_jobs:
    for process in job_list:
        if process.is_finished():
            add_to_queue(current_time, priority=0)

    if boost_available():
        boost_jobs()

    # todo io done?
    job = find_highest_priority_job(queues)
    job.decrement_wait_time()
    # todo run it
    # todo response time
    # todo FCFS queue
    if job.priority == number_of_queues - 1:
        job.finish(current_time)
    else:
        # normal queue
        job.run(current_time)

        # todo increment wait_time
        for job in job_list:
            if not job.is_finished():
                job.increment_wait_time()
    current_time += 1


for job in job_list:
    print(f"job turn: {job.statistics.turnaround}")
    print(f"job wait: {job.statistics.wait}")
