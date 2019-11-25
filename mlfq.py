import argparse
from scheduling_queue import RRQueue
from scheduling_queue import FCFSQueue
from process import Process
import PySimpleGUI as sg
import random

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
                process_id = highest_queue.run_process(self.current_time)
                draw_process_rect(highest_queue.queue_id, highest_queue.ticks - 1, process_id)
            else:
                for queue in self.queues:
                    queue.ticks += 1
            for queue in self.queues:
                queue.ticks += 1
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
        avg_turnaround_time = avg_wait = avg_response = 0
        for job in self.job_list:
            print(f"job arrival {job.arrival}, "
                  f"turnaround_time: {job.statistics.turnaround}, "
                  f"wait: {job.statistics.wait}, "
                  f"response {job.statistics.response_time}")
            avg_response += job.statistics.response_time
            avg_turnaround_time += job.statistics.turnaround
            avg_wait += job.statistics.wait

        total_jobs = len(self.job_list)
        print("\nGlobal Statistics")
        print(f"average turnaround_time: {avg_turnaround_time / total_jobs}\n"
              f"average waiting_time: {avg_wait / total_jobs}\n"
              f"average response_time: {avg_response / total_jobs}\n"
              f"throughput: {total_jobs / self.current_time * 1000}")


def parse_jobs(jobs):
    returned_jobs = list()
    for job in jobs:
        burst, arrival = job.split(":")

        returned_jobs.append(Process(int(burst), int(arrival)))
    return returned_jobs


def start_gui():
    global graph, window
    graph = sg.Graph(canvas_size=(1000, 300), graph_bottom_left=(0, 300), graph_top_right=(1000, 0), key='graph')

    layout = [[graph],
              [sg.Button('Exit')]]

    # Create the Window
    window = sg.Window('MultiLevelFeedbackQueue', layout, finalize=True)
    text1 = graph.draw_text('Queue 0 RR : 5', (5, 10), text_location=sg.TEXT_LOCATION_TOP_LEFT)
    text2 = graph.draw_text('Queue 1 RR : 10', (5, 35), text_location=sg.TEXT_LOCATION_TOP_LEFT)
    text3 = graph.draw_text('Queue 2 FCFS', (5, 60), text_location=sg.TEXT_LOCATION_TOP_LEFT)


x1 = 100
x2_off = 10
y1 = 10
y2_off = 15
COLORS = ["purple", "lightblue", "red", "green", "blue", "brown", "red", "black"]


def draw_process_rect(queue_num, queue_ticks, process_id):
    color = COLORS[process_id]
    # color = (sg.YELLOWS[process_id], sg.BLUES[process_id])
    # color = sg.BLUES[process_id]
    # color = str('#' + str(int(random.random() * process_id * 1000000)))
    # print(float(hash(process_id) % 256) / 256)
    y1_d = y1 + 25 * queue_num
    x1_d = x1 + queue_ticks * x2_off
    graph.draw_rectangle((x1_d, y1_d), (x1_d + x2_off, y1_d + y2_off), fill_color=color)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--numberOfQueues", default=3,
                    help="number of queues", type=int)

    ap.add_argument("-q", "--quantumList", default="5,10",
                    help="q1,q2,q3, ...", type=str)

    ap.add_argument("-l", "--jobList", default="15:1,20:0,17:14,25:20",
                    help="burst1:arrivalTime1,burst2:arrivalTime2, ...")

    ap.add_argument("-b", "--boost", default=0,
                    help="", type=int)

    args = vars(ap.parse_args())

    boost = args["boost"]
    number_of_queues = args["numberOfQueues"]
    jobs = str(args["jobList"]).split(",")
    quantum_list = str(args["quantumList"]).split(",")
    quantum_list = [int(quantum) for quantum in quantum_list]

    start_gui()
    processes = parse_jobs(jobs)
    mlfq = Mlfq(number_of_queues, quantum_list, processes, boost)
    mlfq.loop()
    mlfq.print_statistics()
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):  # if user closes window or clicks cancel
            break
    window.close()
