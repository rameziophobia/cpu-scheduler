from collections import deque
from process import Process


class Queue:
    highest_priority = 0

    def __init__(self, priority):
        self._deque = deque()
        self.priority = priority
        Queue.highest_priority += 1

    def pop_first(self):
        return self._deque.popleft()

    def add_process(self, process: Process):
        self._deque.append(process)

    def empty(self):
        self._deque.clear()

    def run_process(self):
        pass


class FCFS_queue(Queue):
    def __init__(self, priority):
        Queue.__init__(self, priority)

    def run_process(self):
        pass


class RR_queue(Queue):
    def __init__(self, priority, quantum):
        Queue.__init__(self, priority)
        self.quantum = quantum

    def run_process(self):
        pass
