from collections import deque
from process import Process


class Queue:
    highest_priority = 0

    def __init__(self, priority):
        self.__deque = deque()
        self.priority = priority
        Queue.highest_priority += 1

    def pop_first(self):
        return self.__deque.popleft()

    def add_process(self, process: Process):
        self.__deque.append(process)
        process.current_run = 0

    def empty(self):
        self.__deque.clear()

    def is_empty(self):
        return True if len(self.__deque) == 0 else False

    def get_highest_priority_job(self):
        # if
        return self.__deque[0]

    def run_process(self, current_time):
        process = self.get_highest_priority_job()
        process.run(current_time)

        if process.is_finished():
            self.pop_first()
            return


class FCFSQueue(Queue):
    def __init__(self, priority):
        Queue.__init__(self, priority)

    def run_process(self, current_time):
        Queue.run_process(self, current_time)


class RRQueue(Queue):
    def __init__(self, priority, quantum):
        Queue.__init__(self, priority)
        self.quantum = quantum
        self.next_queue = None

    def set_next_queue(self, queue: Queue):
        self.next_queue = queue

    def run_process(self, current_time):
        process = self.get_highest_priority_job()
        Queue.run_process(self, current_time)

        if process.current_run == self.quantum:
            self.pop_first()
            self.next_queue.add_process(process)
