from statistics import Statistics
from queue import Queue


class Process:
    def __init__(self, burst_time, arrival_time, io_freq, queue: Queue):
        self.arrival = arrival_time
        self.burst_time = burst_time
        self.io_freq = io_freq
        self.priority = 0
        self.time_left = burst_time
        self.statistics = Statistics()
        self.doing_io = False
        self.finish_time = -1
        self.current_run = 0
        self.queue = queue

    def is_finished(self):
        return True if self.finish_time != -1 else False

    def finish(self, time):
        self.time_left = 0
        self.finish_time = time
        self.queue
        queues[self.priority].queue.remove(self)
        finished_jobs.append(self)
        self.statistics.calculate_turnaround(self.finish_time, self.arrival)

    # todo rename
    def downgrade_queue(self):
        queues[self.priority].queue.pop(0)
        self.priority += 1
        queues[self.priority].queue.append(self)
        self.current_run = 0

    def increment_wait_time(self):
        self.statistics.wait += 1

    def decrement_wait_time(self):
        self.statistics.wait -= 1

    def run(self, current_time):
        self.time_left -= 1
        if self.time_left == 0:
            self.finish(current_time)
        self.current_run += 1

        if self.current_run == queues[self.priority].quantum:
            self.downgrade_queue()