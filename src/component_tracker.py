class ComponentTracker(object):

    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.total_time = 0
        self.isLatestComponent = True

    def add_time(self):
        self.total_time += (self.end_time - self.start_time)