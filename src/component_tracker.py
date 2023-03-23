class ComponentTracker(object):

    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.total_times = []
        self.isLatestComponent = True

    def add_time_spent_in_buffer(self):
        self.total_times.append(self.end_time - self.start_time)