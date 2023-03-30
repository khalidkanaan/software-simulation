from simpy.resources import container
import time

class Workstation1(object):

    def __init__(self, env, notifier, w1_c1_tracker, w1_c1_mutex):
        self.env = env
        # Keeps track of the number of products assembled
        self.p1 = 0 
        # Stores the service times for each assembly process
        self.service_times = [] 
        # Buffer for component 1 with capacity 2
        self.c1_buffer = container.Container(self.env, 2)
        # Notifier
        self.notifier = notifier
        # Time spent idle
        self.idle_time = 0
        # List of buffer occupancies
        self.c1_buffer_occupancies = dict()
        self.w1_c1_tracker = w1_c1_tracker
        self.w1_c1_mutex = w1_c1_mutex


    def run(self):
        print('\***** Workstation 1 Running *****/')
        rv_service_times = list(map(float, open('data/ws1.dat', 'r').read().splitlines()))
        count = 0
        while True:

            # Start time of idle
            start_idle_time = self.env.now

            if (self.c1_buffer.level == 2):
                self.notifier.w1_full = True
                print("W1 BUFFER IS FULL OF C1")

            # Wait for component 1 to become available
            yield self.c1_buffer.get(1)

            self.c1_buffer_occupancies.update({self.env.now : self.c1_buffer.level})

            with self.w1_c1_mutex.request() as req:
                yield req
                if (self.w1_c1_tracker.isLatestComponent):
                    self.w1_c1_tracker.end_time = self.env.now
                    self.w1_c1_tracker.add_time_spent_in_buffer()
                else:
                    self.w1_c1_tracker.isLatestComponent = True

            if (self.notifier.all_workstations_full() and self.c1_buffer.level < self.c1_buffer.capacity):
                self.notifier.w1_full = False
                self.notifier.maybe_unblock_inspector("workstation_1")
                
            # Generate service time using exponential distribution
            service_time = rv_service_times[count]
            self.service_times.append(service_time)

            # Add the time spent idle
            self.idle_time += (self.env.now - start_idle_time)

            # Wait for assembly process to complete
            yield self.env.timeout(service_time)

            # Increase count of products assembled
            self.p1 +=1

            # Assembly complete message
            print('\***** Assembled: Product 1 *****/')
            count += 1
    
    def start_process(self):
        # Start the run function as a SimPy process
        self.env.process(self.run())