from NasaCollageGUI.model.statusmonitor import StatusMonitor


class Task(object):

    def __init__(self):
        self.status_mon = StatusMonitor()
        self.result = None
        self.running = True

    def run(self):
        self.running = True
        self._run()
        self.running = False
        return self.result

    def _run(self):
        print("Base task object run called")

    def get_status(self) -> StatusMonitor:
        return self.status_mon

    def get_result(self):
        return None