from simpy.resources import container
from helper_functions import exponential_dist

class Workstation2(object):

    def __init__(self, env):
        self.env = env
        self.p2 = 0
        self.service_times = []
        self.c1_buffer = container.Container(self.env, 2)
        self.c2_buffer = container.Container(self.env, 2)

    def run(self):
        print('Workstation 2 starting')
        while True:
            # Waits until there are components available to use
            yield self.c1_buffer.get(1) & self.c2_buffer.get(1)
            service_time = exponential_dist(open('data/ws2.dat').read().splitlines())  # <--Generate duration here
            self.service_times.append(service_time)
            yield self.env.timeout(service_time)
            self.p2 += 1
            print('Product 2 assembled')

    def start_process(self):
        self.env.process(self.run())