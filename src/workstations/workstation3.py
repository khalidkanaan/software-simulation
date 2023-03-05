from simpy.resources import container
from helper_functions import exponential_dist

class Workstation3(object):

    def __init__(self, env, event_list, event_index, resource, notifier):
        self.env = env
        # Counter for number of product 3 assembled
        self.p3 = 0
        # List to store the service times for each assembled product
        self.service_times = []
        # Container for component 1
        self.c1_buffer = container.Container(self.env, 2)
        # Container for component 3
        self.c3_buffer = container.Container(self.env, 2)
        # Workstation 3 event
        self.event_list = event_list
        self.event_index = event_index
        self.resource = resource
        self.notifier = notifier

    def run(self):
        print('\***** Workstation 3 Running *****/')
        while True:
            if (self.c1_buffer.level == 2):
                self.notifier.w3_full = True
                print("W3 BUFFER IS FULL OF C1")
            elif (self.notifier.all_workstations_full() and self.c1_buffer.level < self.c1_buffer.capacity):
                self.notifier.w3_full = False
                self.event_list[self.event_index[0]].succeed("workstation_3")
                request = self.resource.request()
                yield request
                self.event_index[0] += 1
                print(f"W3 incremented event index to {self.event_index[0]}")
                yield self.env.timeout(1)
                self.resource.release(request)

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
