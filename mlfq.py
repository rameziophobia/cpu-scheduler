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
            draw_rr_queue_header(i, quantum_list[i])

        self.queues.append(FCFSQueue(number_of_queues - 1))
        draw_fcfs_queue_header(number_of_queues - 1)

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
                draw_process_rect(highest_queue.queue_id, self.current_time, process_id)

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
        for i, job in enumerate(self.job_list):
            graph.draw_text(f"job arrival {job.arrival}, "
                            f"burst_time {job.burst_time}, "
                            f"turnaround_time: {job.statistics.turnaround}, "
                            f"wait: {job.statistics.wait}, "
                            f"response {job.statistics.response_time}",
                            (5, 10 + 25 * (number_of_queues + i)), text_location=sg.TEXT_LOCATION_TOP_LEFT)
            avg_response += job.statistics.response_time
            avg_turnaround_time += job.statistics.turnaround
            avg_wait += job.statistics.wait

        total_jobs = len(self.job_list)
        graph.draw_text(f"Global Statistics\n"
                        f"average turnaround_time: {avg_turnaround_time / total_jobs}\n"
                        f"average waiting_time: {avg_wait / total_jobs}\n"
                        f"average response_time: {avg_response / total_jobs}\n"
                        f"throughput: {total_jobs / self.current_time * 1000}",
                        (5, 10 + 25 * (number_of_queues + total_jobs)),
                        text_location=sg.TEXT_LOCATION_TOP_LEFT)


def parse_jobs(jobs):
    returned_jobs = list()
    for job in jobs:
        burst, arrival = job.split(":")

        returned_jobs.append(Process(int(burst), int(arrival)))
    return returned_jobs


def start_gui():
    global graph, window
    graph = sg.Graph(canvas_size=(1000, 500), graph_bottom_left=(0, 500), graph_top_right=(1000, 0), key='graph')

    layout = [[graph],
              [sg.Button('Exit')]]

    # Create the Window
    window = sg.Window('MultiLevelFeedbackQueue', layout, finalize=True)


def draw_rr_queue_header(queue_id, quantum):
    return graph.draw_text(f'Queue {queue_id} RR : {quantum}',
                           (5, 10 + 25 * queue_id), text_location=sg.TEXT_LOCATION_TOP_LEFT)


def draw_fcfs_queue_header(queue_id):
    return graph.draw_text(f'Queue {queue_id} FCFS', (5, 10 + 25 * queue_id),
                           text_location=sg.TEXT_LOCATION_TOP_LEFT)


x1 = 100
x2_off = 5
y1 = 10
y2_off = 15
COLORS = ["purple", "lightblue", "red", "green", "blue", "brown", "grey", "pink", "black", "yellow"]


def draw_process_rect(queue_num, queue_ticks, process_id):
    color = COLORS[process_id % len(COLORS)]
    y1_d = y1 + 25 * queue_num
    x1_d = x1 + queue_ticks * x2_off
    graph.draw_rectangle((x1_d, y1_d), (x1_d + x2_off, y1_d + y2_off), fill_color=color)


def parse_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-q", "--quantumList", default="2, 4, 7",
                    help="q1,q2,q3, ...", type=str)
    ap.add_argument("-l", "--jobList", default="19:0, 12:5, 13:50, 15:15, 17:15",
                    help="burst1:arrivalTime1,burst2:arrivalTime2, ...")
    ap.add_argument("-b", "--boost", default=71,
                    help="", type=int)
    return ap


if __name__ == '__main__':
    arg_parser = parse_arguments()

    args = vars(arg_parser.parse_args())
    boost = args["boost"]
    jobs = str(args["jobList"]).split(",")
    quantum_list = str(args["quantumList"]).split(",")
    quantum_list = [int(quantum) for quantum in quantum_list]
    number_of_queues = len(quantum_list) + 1

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
