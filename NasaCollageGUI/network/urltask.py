import time
from threading import Thread
import json
from uuid import uuid1
from threading import Thread


class BaseUrlTask(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.running = False
        self.progress = ProgressObject()
        self.time_started = time.time()
        self.id = str(uuid1())
        self.type = "base"
        self.failed = False
        self.todo_urls = []
        self.done_urls = []
        self.results = {}
        self.other_notes = {}

    def serialize(self):
        return {
            "time_started": self.time_started,
            "id": self.id,
            "type": self.type,
            "failed": self.failed,
            "todo_urls": self.todo_urls,
            "done_urls": self.done_urls,
            "results": self.results,
            "other": self.other_notes
        }

    def run(self):
        pass


class ProgressObject(object):

    def __init__(self):
        self.todo_total = 0
        self.start_time = time.time()
        self.todo_done = 0
        self.avg_timedone = 0
        self.timeleft = 0

    def add_total(self, total_req):
        self.todo_total = total_req

    def increment(self):
        if self.todo_done != 0:
            self.avg_timedone = (time.time()-self.start_time)/self.todo_done
            self.timeleft = self.avg_timedone * (self.todo_total-self.todo_done)
        self.todo_done += 1
