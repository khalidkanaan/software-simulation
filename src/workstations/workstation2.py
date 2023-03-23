from simpy.resources import container
import time

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
        # Time spent idle
        self.idle_time = 0
        # List of c1 buffer occupancies
        self.c1_buffer_occupancies = []
        # List of c2 buffer occupancies
        self.c2_buffer_occupancies = []

    def run(self):
        # Start message
        print('\***** Workstation 2 Running *****/')
        rv_service_times = list(map(float, open('new_data/generated_ws2.dat', 'r').read().splitlines()))
        count = 0
        while True:
            # Start time of idle
            # start_idle_time = time.time()
            start_idle_time = self.env.now

            if (self.c1_buffer.level == 2):
                self.notifier.w2_full = True
                print("W2 BUFFER IS FULL OF C1")

            # Wait until both components are available
            yield self.c1_buffer.get(1) & self.c2_buffer.get(1)

            self.c1_buffer_occupancies.append(self.c1_buffer.level)
            self.c2_buffer_occupancies.append(self.c2_buffer.level)

            if (self.notifier.all_workstations_full() and self.c1_buffer.level < self.c1_buffer.capacity):
                self.notifier.w2_full = False
                self.notifier.maybe_unblock_inspector("workstation_2")

            # Generate service time using exponential distribution
            service_time = rv_service_times[count]
            # Add the service time to the list of service times
            self.service_times.append(service_time)

            # Add the time spent idle
            # self.idle_time += (time.time() - start_idle_time)
            self.idle_time += (self.env.now - start_idle_time)

            # Wait for assembly process to complete
            yield self.env.timeout(service_time)

            # Increment the number of products assembled
            self.p2 += 1

            # Assembly complete message
            print('\***** Assembled: Product 2 *****/')
            count += 1

    def start_process(self):
        # Start the workstation's process
        self.env.process(self.run())