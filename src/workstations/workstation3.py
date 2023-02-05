from simpy.resources import container
from helper_functions import exponential_dist

class Workstation3(object):

    def __init__(self, env):
        self.env = env
        self.p3 = 0
        self.service_times = []
        self.c1_buffer = container.Container(self.env, 2)
        self.c3_buffer = container.Container(self.env, 2)

    def run(self):
        print('Workstation 3 starting')
        while True:
            # Waits until there are components available to use
            yield self.c1_buffer.get(1) & self.c3_buffer.get(1)
            service_time = exponential_dist(open('data/ws3.dat').read().splitlines())  # <--Generate duration here
            self.service_times.append(service_time)
            yield self.env.timeout(service_time)
            self.p3 += 1
            print('Product 3 assembled')
    
    def start_process(self):
        self.env.process(self.run())