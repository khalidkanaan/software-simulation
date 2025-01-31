from simpy.resources import container
import time

class Workstation3(object):

    def __init__(self, env, notifier, w3_c1_tracker, w3_c3_tracker, w3_c1_mutex, w3_c3_mutex):
        self.env = env
        # Counter for number of product 3 assembled
        self.p3 = 0
        # List to store the service times for each assembled product
        self.service_times = []
        # Container for component 1
        self.c1_buffer = container.Container(self.env, 2)
        # Container for component 3
        self.c3_buffer = container.Container(self.env, 2)
        # Notifier
        self.notifier = notifier
        # Time spent idle
        self.idle_time = 0
        # List of c1 buffer occupancies
        self.c1_buffer_occupancies = dict()
        # List of c3 buffer occupancies
        self.c3_buffer_occupancies = dict()
        self.w3_c1_tracker = w3_c1_tracker
        self.w3_c3_tracker = w3_c3_tracker
        self.w3_c1_mutex = w3_c1_mutex
        self.w3_c3_mutex = w3_c3_mutex

    def run(self):
        print('\***** Workstation 3 Running *****/')
        rv_service_times = list(map(float, open('data/ws3.dat', 'r').read().splitlines()))
        count = 0
        while True:

            # Start time of idle
            start_idle_time = self.env.now

            if (self.c1_buffer.level == 2):
                self.notifier.w3_full = True
                print("W3 BUFFER IS FULL OF C1")

            # Yields until components 1 and 3 are available
            yield self.c1_buffer.get(1) & self.c3_buffer.get(1)

            self.c1_buffer_occupancies.update({self.env.now : self.c1_buffer.level})
            self.c3_buffer_occupancies.update({self.env.now : self.c3_buffer.level})

            with self.w3_c1_mutex.request() as req1, self.w3_c3_mutex.request() as req2:
                yield req1 & req2
                if (self.w3_c1_tracker.isLatestComponent and self.w3_c3_tracker.isLatestComponent):
                    self.w3_c1_tracker.end_time = self.env.now
                    self.w3_c1_tracker.add_time_spent_in_buffer()
                    self.w3_c3_tracker.end_time = self.env.now
                    self.w3_c3_tracker.add_time_spent_in_buffer()
                elif (self.w3_c1_tracker.isLatestComponent and not self.w3_c3_tracker.isLatestComponent):
                    self.w3_c1_tracker.end_time = self.env.now
                    self.w3_c1_tracker.add_time_spent_in_buffer()
                    self.w3_c3_tracker.isLatestComponent = True
                elif (not self.w3_c1_tracker.isLatestComponent and self.w3_c3_tracker.isLatestComponent):
                    self.w3_c3_tracker.end_time = self.env.now
                    self.w3_c3_tracker.add_time_spent_in_buffer()
                    self.w3_c1_tracker.isLatestComponent = True
                else:
                    self.w3_c1_tracker.isLatestComponent = True
                    self.w3_c3_tracker.isLatestComponent = True

            if (self.notifier.all_workstations_full() and self.c1_buffer.level < self.c1_buffer.capacity):
                self.notifier.w3_full = False
                self.notifier.maybe_unblock_inspector("workstation_3")

            # Generate service time using exponential distribution
            service_time = rv_service_times[count]
            self.service_times.append(service_time)

            # Add the time spent idle
            self.idle_time += (self.env.now - start_idle_time)

            # Wait for assembly process to complete
            yield self.env.timeout(service_time)

            # Increment product 3 assembled counter
            self.p3 += 1

            # Assembly complete message
            print('\***** Assembled: Product 3 *****/')
            self.notifier.w3_full = False
            count += 1
    
    def start_process(self):
        # Start the run process as a SimPy process
        self.env.process(self.run())
