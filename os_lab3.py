from random import randint
from itertools import accumulate
from collections import deque, defaultdict, Counter
from matplotlib import pyplot


class Job:
    def __init__(self, arrival, processing):
        self.arrival = arrival
        self.fixed_processing = self.left = processing
        self.starts = []
        self.ends = []

    @property
    def existence_time(self):
        return self.ends[-1] - self.arrival

    @property
    def idle_time(self):
        return self.existence_time - sum(e - s for s, e in zip(self.starts, self.ends))

    def __str__(self):
        ranges = [f"{x}-{y}" for x, y in zip(self.starts, self.ends)]

        arrival = self.arrival
        processing = self.fixed_processing
        total = self.existence_time
        idle = self.idle_time

        return "{}, {}, {}, {}, {}".format(arrival, processing, total, idle, "|".join(ranges))


class MFQS:
    def __init__(self, jobs_num, min_time, max_time, min_pause, max_pause, queues_num, quantum_length, stable=False):
        self.queues_num = queues_num
        self.quantum_length = quantum_length

        if stable:
            f = lambda: min_pause
        else:
            f = lambda: randint(min_pause, max_pause)

        arrivals = accumulate(f() for i in range(jobs_num))

        self.jobs = deque(
            Job(j, t) for j, t in zip(
                arrivals,
                (randint(min_time, max_time) for _ in range(jobs_num))
            )
        )
        self.finished_jobs = []
        self.queues = [deque() for _ in range(self.queues_num)]
        self.current_time = self.system_idle_time = 0

    @property
    def total_jobs_in_time(self):
        jobs, cur = [], 0
        differences = defaultdict(int)
        for j in self.finished_jobs:
            differences[j.arrival] += 1
            differences[j.ends[-1]] -= 1
        for i in range(self.current_time):
            cur += differences[i]
            jobs.append(cur)
        return jobs

    @property
    def differences(self):
        differences = defaultdict(int)
        for j in self.finished_jobs:
            differences[(j.arrival, "+")] += 1
            differences[(j.ends[-1], "-")] -= 1
        return differences

    def get_non_empty_queue(self):
        for i in range(self.queues_num):
            if self.queues[i]:
                return i

    def get_next_job(self):
        if self.jobs:
            return self.jobs[0]

    def process_next_job(self, cur_index):
        next_index = cur_index + 1
        cur_queue = self.queues[cur_index]
        current_job = cur_queue.popleft()
        next_job = self.get_next_job()
        time_until_arrival = next_job and next_job.arrival - self.current_time
        current_job.starts.append(self.current_time)

        end_flag = 0
        if next_index == self.queues_num:
            max_process_time = current_job.left
        else:
            max_process_time = self.quantum_length * next_index

        if cur_index and next_job and time_until_arrival < min(current_job.left, max_process_time):
            current_job.left -= time_until_arrival
            cur_queue.append(current_job)
            self.current_time = next_job.arrival
        elif current_job.left > max_process_time:
            current_job.left -= max_process_time
            self.queues[next_index].append(current_job)
            self.current_time += max_process_time
        else:
            self.current_time += current_job.left
            end_flag = 1
        current_job.ends.append(self.current_time)
        if end_flag:
            self.finished_jobs.append(current_job)

    def wait_for_job(self):
        if self.jobs:
            self.system_idle_time += self.jobs[0].arrival - self.current_time
            self.current_time = self.jobs[0].arrival
            return 1
        return 0

    def schedule_jobs(self):
        while self.jobs and self.jobs[0].arrival <= self.current_time:
            self.queues[0].append(self.jobs[0])
            self.jobs.popleft()

    def run(self):
        while 1:
            self.schedule_jobs()
            next_queue_index = self.get_non_empty_queue()
            if next_queue_index is None:
                if not self.wait_for_job():
                    break
                continue
            self.process_next_job(next_queue_index)


"""
jobs_num = 10
min_time, max_time = 1, 3
min_pause, max_pause = 0, 5
queues_num = 3
quantum_length = 8
mfqs = MFQS(jobs_num, min_time, max_time, min_pause, max_pause, queues_num, quantum_length)
mfqs.run()
"""

if __name__ == "__main__":
    pauses = []
    waiting_times = []
    idle_times = []

    for pause in range(1, 51):
        w = i = 0
        LOOPS = 1
        for _ in range(LOOPS):
            mfqs = MFQS(
                jobs_num=100,
                min_time=1,
                max_time=20,
                min_pause=0,
                max_pause=pause,
                queues_num=3,
                quantum_length=8
            )
            mfqs.run()
            i += mfqs.system_idle_time
            total_waiting = sum(j.idle_time for j in mfqs.finished_jobs)
            w += total_waiting / len(mfqs.finished_jobs)

        idle_times.append(i / LOOPS)
        waiting_times.append(w / LOOPS)
        pauses.append(pause)
    intensities = pauses[::-1]

    pyplot.subplot(2, 1, 1)
    pyplot.plot(intensities, waiting_times, "b", label="Waiting")
    pyplot.plot(intensities, idle_times, "r", label="Idling")
    pyplot.xlabel("Intensity")
    pyplot.legend()

    mfqs = MFQS(
        jobs_num=1000,
        min_time=150,
        max_time=200,
        min_pause=100,
        max_pause=8,
        queues_num=3,
        quantum_length=8,
        stable=True
    )
    mfqs.run()
    X = 8000
    d = Counter(round(j.idle_time / X) * X for j in mfqs.finished_jobs)

    a = sorted((x, y) for x, y in d.items())

    pyplot.subplot(2, 1, 2)
    pyplot.plot([x[0] for x in a], [x[1] for x in a], label="Total jobs")
    pyplot.xlabel("Jobs")
    pyplot.legend()

    pyplot.savefig("plot.png")