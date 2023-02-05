import random
from helper_functions import exponential_dist

class Inspector2(object):

    def __init__(self, env):
        self.env = env
        self.service_times22 = []
        self.service_times23 = []
        
    def run(self, workstation_2, workstation_3):
        print('\***** Inspector 2 Running *****/')
        while True:
            # Randomly decide which component to make
            if bool(random.getrandbits(1)):  
                # Generate service time for component 2 using exponential distribution
                service_time = exponential_dist(open('data/servinsp22.dat').read().splitlines())  
                self.service_times22.append(service_time)
                # Wait for the service time
                yield self.env.timeout(service_time)
                # Transfered Component 2 to Workstation 2's buffer
                yield workstation_2.c2_buffer.put(1)
                print('\***** Transfered C2 to W2 *****/')
            else:
                # Generate service time for component 3 using exponential distribution
                service_time = exponential_dist(open('data/servinsp23.dat').read().splitlines())  
                self.service_times23.append(service_time)
                # Wait for the service time
                yield self.env.timeout(service_time)
                # Transfered Component 3 to Workstation 3's buffer
                yield workstation_3.c3_buffer.put(1)
                print('\***** Transfered C3 to W3 *****/')

    def start_process(self, workstation_2, workstation_3):
        # Start the run function as a SimPy process
        self.env.process(self.run(workstation_2, workstation_3))
