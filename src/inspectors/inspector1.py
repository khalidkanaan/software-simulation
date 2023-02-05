from operator import attrgetter
from helper_functions import exponential_dist

class Inspector1(object):

    def __init__(self, env):
        self.env = env
        self.service_times = []
        
    def run(self, workstation_1, workstation_2, workstation_3):
        print('Inspector 1 starting')
        while True:
            service_time = exponential_dist(open('data/servinsp1.dat').read().splitlines())  # <--Generate duration here
            self.service_times.append(service_time)
            li = [workstation_1.c1_buffer, workstation_2.c1_buffer,
                  workstation_3.c1_buffer]
            # Finds the container with the least number of type 1 components
            container_to_use = min(li, key=attrgetter('level'))
            yield self.env.timeout(service_time)
            yield container_to_use.put(1)
            if container_to_use is workstation_1.c1_buffer:
                print('Added component 1 to workstation 1')
            elif container_to_use is workstation_2.c1_buffer:
                print('Added component 1 to workstation 2')
            elif container_to_use is workstation_3.c1_buffer:
                print('Added component 1 to workstation 3')

    def start_process(self, workstation_1, workstation_2, workstation_3):
        self.env.process(self.run(workstation_1, workstation_2, workstation_3))