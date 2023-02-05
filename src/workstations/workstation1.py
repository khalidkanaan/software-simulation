from simpy.resources import container
from helper_functions import exponential_dist

class Workstation1(object):

    def __init__(self, env):
        self.env = env
        self.p1 = 0
        self.service_times = []
        self.c1_buffer = container.Container(self.env, 2)
        
    def run(self):
        print('Workstation 1 starting')
        while True:
            # Waits until there are components available to use
            yield self.c1_buffer.get(1)
            service_time = exponential_dist(open('data/ws1.dat').read().splitlines())  # <--Generate duration here
            self.service_times.append(service_time)
            yield self.env.timeout(service_time)
            self.p1 +=1
            print('Product 1 assembled')
    
    def start_process(self):
        self.env.process(self.run())