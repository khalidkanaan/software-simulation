from simpy.resources import container
from helper_functions import exponential_dist

class Workstation3(object):

    def __init__(self, env):
        self.env = env
        # Counter for number of product 3 assembled
        self.p3 = 0
        # List to store the service times for each assembled product
        self.service_times = []
        # Container for component 1
        self.c1_buffer = container.Container(self.env, 2)
        # Container for component 3
        self.c3_buffer = container.Container(self.env, 2)

    def run(self):
        print('\***** Workstation 3 Running *****/')
        while True:
            # Yields until components 1 and 3 are available
            yield self.c1_buffer.get(1) & self.c3_buffer.get(1)
            # Generate service time using exponential distribution
            service_time = exponential_dist(open('data/ws3.dat').read().splitlines())
            self.service_times.append(service_time)
            # Wait for the duration of the service time
            yield self.env.timeout(service_time)
            # Increment product 3 assembled counter
            self.p3 += 1
            print('\***** Assembled: Product 3 *****/')
    
    def start_process(self):
        # Start the run process as a SimPy process
        self.env.process(self.run())
