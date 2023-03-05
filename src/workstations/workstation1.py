from simpy.resources import container
from helper_functions import exponential_dist

class Workstation1(object):

    def __init__(self, env, event_list, event_index, resource, notifier):
        self.env = env
        # Keeps track of the number of products assembled
        self.p1 = 0 
        # Stores the service times for each assembly process
        self.service_times = [] 
        # Buffer for component 1 with capacity 2
        self.c1_buffer = container.Container(self.env, 2)
        # Workstation 1 event
        self.event_list = event_list
        self.event_index = event_index
        self.resource = resource
        self.notifier = notifier

    def run(self):
        print('\***** Workstation 1 Running *****/')
        while True:
            if (self.c1_buffer.level == 2):
                self.notifier.w1_full = True
                print("W1 BUFFER IS FULL OF C1")
            elif (self.notifier.all_workstations_full() and self.c1_buffer.level < self.c1_buffer.capacity):
                self.notifier.w1_full = False
                self.event_list[self.event_index[0]].succeed("workstation_1")
                request = self.resource.request()
                yield request
                self.event_index[0] += 1
                print(f"W1 incremented event index to {self.event_index[0]}")
                yield self.env.timeout(1)
                self.resource.release(request)

            # Wait for component 1 to become available
            yield self.c1_buffer.get(1)
                
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