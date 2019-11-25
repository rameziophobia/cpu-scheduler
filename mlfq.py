import argparse
from scheduling_queue import RRQueue
from scheduling_queue import FCFSQueue
from process import Process


class Mlfq:
    def __init__(self, number_of_queues, quantum_list, job_list, boost):
        self.current_time = 0
        self.queues = list()
        self.init_queues(number_of_queues, quantum_list)
        self.job_list = job_list
        self.boost = boost

    def init_queues(self, number_of_queues, quantum_list):
        for i in range(number_of_queues - 1):
            self.queues.append(RRQueue(i, quantum_list[i]))

        self.queues.append(FCFSQueue(number_of_queues - 1))

        for i in range(number_of_queues - 1):
            self.queues[i].set_next_queue(self.queues[i + 1])

    def add_arrival_to_first_queue(self, process, priority):
        if process.arrival == self.current_time:
            self.queues[priority].add_process(process)

    def loop(self):
        while True:
            pending_jobs = [job for job in self.job_list if not job.is_finished()]
            if len(pending_jobs) == 0:
                break

            for process in pending_jobs:
                self.add_arrival_to_first_queue(process, priority=0)

            if self.is_boost_available():
                self.boost_jobs()

            highest_queue = self.get_highest_non_empty_queue()
            if highest_queue is not None:
                highest_queue.run_process(self.current_time)

            self.current_time += 1

    def is_boost_available(self):
        if self.boost <= 0 or self.current_time == 0:
            return False
        return True

    def boost_jobs(self):
        if self.current_time % self.boost == 0:
            for queue in self.queues:
                queue.empty()
            for job in self.job_list:
                if not job.is_finished():
                    self.queues[0].add_process(job)

    def get_highest_non_empty_queue(self):
        for queue in self.queues:
            if queue.is_empty():
                continue
            return queue

    def print_statistics(self):
        for job in self.job_list:
            print(f"job arrival {job.arrival}, turn: {job.statistics.turnaround}, wait: {job.statistics.wait}, "
                  f"response {job.statistics.response_time}")

        print(f"throughput: {len(self.job_list) / self.current_time * 1000}")


def parse_jobs(jobs):
    returned_jobs = list()
    for job in jobs:
        burst, arrival = job.split(":")

        returned_jobs.append(Process(int(burst), int(arrival)))
    return returned_jobs


if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--numberOfQueues", default=3,
                    help="number of queues", type=int)

    ap.add_argument("-q", "--quantumList", default="5,10",
                    help="q1,q2,q3, ...", type=str)

    ap.add_argument("-l", "--jobList", default="15:1,20:0",
                    help="burst1:arrivalTime1,burst2:arrivalTime2, ...")

    ap.add_argument("-b", "--boost", default=0,
                    help="", type=int)

    args = vars(ap.parse_args())

    boost = args["boost"]
    number_of_queues = args["numberOfQueues"]
    jobs = str(args["jobList"]).split(",")
    quantum_list = str(args["quantumList"]).split(",")
    quantum_list = [int(quantum) for quantum in quantum_list]

    processes = parse_jobs(jobs)
    mlfq = Mlfq(number_of_queues, quantum_list, processes, boost)
    mlfq.loop()
    mlfq.print_statistics()


