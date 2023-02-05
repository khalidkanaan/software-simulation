import random
from helper_functions import exponential_dist

class Inspector2(object):

    def __init__(self, env):
        self.env = env
        self.service_times22 = []
        self.service_times23 = []
        
    def run(self, workstation_2, workstation_3):
        print('Inspector 2 starting')
        while True:
            if bool(random.getrandbits(1)):  # Randomly decides which component to make
                service_time = exponential_dist(open('data/servinsp22.dat').read().splitlines())  # <--Generate duration here
                self.service_times22.append(service_time)
                yield self.env.timeout(service_time)
                yield workstation_2.c2_buffer.put(1)
                print('Added component 2 to workstation 2')
            else:
                service_time = exponential_dist(open('data/servinsp23.dat').read().splitlines())  # <--Generate duration here
                self.service_times23.append(service_time)
                yield self.env.timeout(service_time)
                yield workstation_3.c3_buffer.put(1)
                print('Added component 3 to workstation 3')

    def start_process(self, workstation_2, workstation_3):
        self.env.process(self.run(workstation_2, workstation_3))