from simpy.resources import container

class Workstation3(object):

    def __init__(self, env, notifier):
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

    def run(self):
        print('\***** Workstation 3 Running *****/')
        rv_service_times = list(map(float, open('new_data/generated_ws3.dat', 'r').read().splitlines()))
        count = 0
        while True:

            if (self.c1_buffer.level == 2):
                self.notifier.w3_full = True
                print("W3 BUFFER IS FULL OF C1")

            # Yields until components 1 and 3 are available
            yield self.c1_buffer.get(1) & self.c3_buffer.get(1)

            if (self.notifier.all_workstations_full() and self.c1_buffer.level < self.c1_buffer.capacity):
                self.notifier.w3_full = False
                self.notifier.maybe_unblock_inspector("workstation_3")

            # Generate service time using exponential distribution
            service_time = rv_service_times[count]
            self.service_times.append(service_time)
            # Wait for the duration of the service time
            yield self.env.timeout(service_time)
            # Increment product 3 assembled counter
            self.p3 += 1
            print('\***** Assembled: Product 3 *****/')

            count += 1
    
    def start_process(self):
        # Start the run process as a SimPy process
        self.env.process(self.run())
