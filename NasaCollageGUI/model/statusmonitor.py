import time


class StatusMonitor(object):

    def __init__(self):
        self.total_tasks = 0
        self.done_tasks = 0
        self.average_time_between_task_done = 0
        self.start_time = time.time()
        self.time_elapsed = 0

    def set_total_tasks(self, total_amt: int) -> None:
        self.total_tasks = total_amt

    def clear(self):
        self.total_tasks = 0
        self.done_task = 0
        self.average_time_between_task_done = 0
        self.start_time = time.time()
        self.time_elapsed = 0

    def get_tasks_left(self) -> int:
        return self.total_tasks - self.done_tasks

    def get_time_left(self) -> float:
        tasks_left = self.total_tasks - self.done_tasks
        time_left = self.average_time_between_task_done * tasks_left
        return time_left

    def do_task(self) -> None:
        self.done_tasks += 1
        current_time = time.time()
        self.time_elapsed = current_time - self.start_time
        self.average_time_between_task_done = self.time_elapsed/self.done_tasks
