from datetime import datetime

class Heuristics(object):

    def __init__(self):
        self.simulation_start_time
        self.simulation_end_time
    
    def store_start_time(self, start_time):
        self.simulation_start_time = start_time

    def store_end_time(self, end_time):
        self.simulation_end_time = end_time

    def find_sim_time_in_seconds(self) :
        return (self.simulation_end_time - self.simulation_start_time).total_seconds()

        
    