from simpy.resources import container
from helper_functions import exponential_dist

class Workstation1(object):

    def __init__(self, env, notifier):
        self.env = env
        # Keeps track of the number of products assembled
        self.p1 = 0 
        # Stores the service times for each assembly process
        self.service_times = [] 
        # Buffer for component 1 with capacity 2
        self.c1_buffer = container.Container(self.env, 2)
        # Notifier
        self.notifier = notifier

    def run(self):
        print('\***** Workstation 1 Running *****/')
        while True:

            if (self.c1_buffer.level == 2):
                self.notifier.w1_full = True
                print("W1 BUFFER IS FULL OF C1")

            # Wait for component 1 to become available
            yield self.c1_buffer.get(1)

            if (self.notifier.all_workstations_full() and self.c1_buffer.level < self.c1_buffer.capacity):
                self.notifier.w1_full = False
                self.notifier.maybe_unblock_inspector("workstation_1")
                
            # Generate service time using exponential distribution
            service_time = exponential_dist(open('data/ws1.dat').read().splitlines())  
            self.service_times.append(service_time)
            # Wait for assembly process to complete
            yield self.env.timeout(service_time)
            # Increase count of products assembled
            self.p1 +=1
            print('\***** Assembled: Product 1 *****/')
    
    def start_process(self):
        # Start the run function as a SimPy process
        self.env.process(self.run())