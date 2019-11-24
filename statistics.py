class Statistics:
    def __init__(self):
        self.turnaround = 0
        self.response_time = -1
        self.wait = 0
    #     todo throughput

    def calculate_turnaround(self, final, arrival):
        self.turnaround = final - arrival - self.wait

    def increment_wait(self):
        self.wait += 1
