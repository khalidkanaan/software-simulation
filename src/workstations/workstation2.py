from simpy.resources import container
from helper_functions import exponential_dist

class Workstation2(object):

    def __init__(self, env, notifier):
        # Define the environment where this workstation runs
        self.env = env
        # Counter to keep track of the number of products assembled
        self.p2 = 0
        # List to keep track of the service times for each product assembled
        self.service_times = []
        # Component 1 buffer with a capacity of 2
        self.c1_buffer = container.Container(self.env, 2)
        # Component 2 buffer with a capacity of 2
        self.c2_buffer = container.Container(self.env, 2)
        # Notifier
        self.notifier = notifier

    def run(self):
        # Start message
        print('\***** Workstation 2 Running *****/')
        while True:
            
            if (self.c1_buffer.level == 2):
                self.notifier.w2_full = True
                print("W2 BUFFER IS FULL OF C1")

            # Wait until both components are available
            yield self.c1_buffer.get(1) & self.c2_buffer.get(1)

            if (self.notifier.all_workstations_full() and self.c1_buffer.level < self.c1_buffer.capacity):
                self.notifier.w2_full = False
                self.notifier.maybe_unblock_inspector("workstation_2")

            # Generate service time using exponential distribution
            service_time = exponential_dist(open('data/ws2.dat').read().splitlines())
            # Add the service time to the list of service times
            self.service_times.append(service_time)
            # Wait for the specified service time
            yield self.env.timeout(service_time)
            # Increment the number of products assembled
            self.p2 += 1
            # Assembly complete message
            print('\***** Assembled: Product 2 *****/')

    def start_process(self):
        # Start the workstation's process
        self.env.process(self.run())