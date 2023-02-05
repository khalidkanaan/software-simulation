from operator import attrgetter
from helper_functions import exponential_dist

class Inspector1(object):

    def __init__(self, env):
        self.env = env
        self.service_times = []
        
    def run(self, workstation_1, workstation_2, workstation_3):
        print('\***** Inspector 1 Running *****/')
        while True:
            # Generate service time using exponential distribution
            service_time = exponential_dist(open('data/servinsp1.dat').read().splitlines())  
            self.service_times.append(service_time)
            # Get list of all buffers with type 1 components
            c1_lst = [workstation_1.c1_buffer, workstation_2.c1_buffer,
                  workstation_3.c1_buffer]
            # Find the buffer with the least number of type 1 components
            selected_buffer = min(c1_lst, key=attrgetter('level'))
            # Wait for the service time
            yield self.env.timeout(service_time)
            # Add type 1 component to the selected container
            yield selected_buffer.put(1)
            # Print which workstation received the type 1 component
            if selected_buffer is workstation_1.c1_buffer:
                print('\***** Transfered C1 to W1 *****/')
            elif selected_buffer is workstation_2.c1_buffer:
                print('\***** Transfered C1 to W2 *****/')
            elif selected_buffer is workstation_3.c1_buffer:
                print('\***** Transfered C1 to W3 *****/')

    def start_process(self, workstation_1, workstation_2, workstation_3):
        # Start the run function as a SimPy process
        self.env.process(self.run(workstation_1, workstation_2, workstation_3))
