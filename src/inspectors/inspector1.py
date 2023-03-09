from operator import attrgetter
from helper_functions import exponential_dist

class Inspector1(object):

    def __init__(self, env, notifier):
        self.env = env
        self.service_times = []
        self.notifier = notifier
        
    def run(self, workstation_1, workstation_2, workstation_3):
        print('\***** Inspector 1 Running *****/')
        while True:
            # Generate service time using exponential distribution
            service_time = exponential_dist(open('data/servinsp1.dat').read().splitlines())  
            self.service_times.append(service_time)
            # Get list of all buffers with type 1 components
            c1_lst = [workstation_1.c1_buffer, workstation_2.c1_buffer,
                  workstation_3.c1_buffer]
            # Find the buffer with the least number of type 1 components, if full wait until a workstation is available
            if (not self.notifier.all_workstations_full()):
                selected_buffer = min(c1_lst, key=attrgetter('level'))
            else:
                while self.notifier.all_workstations_full():
                    print("/********************************** ALL BUFFERS FULL, INSPECTOR 1 WAITING FOR NEXT AVAILABLE C1 BUFFER ****************************/")
                    workstation_available = yield self.notifier.inspector_blocked()
                print("/********************************** INSPECTOR 1 FINISHED WAITING, CHOSE " + workstation_available + " ****************************/")
                if (workstation_available == "workstation_1"):
                    selected_buffer = workstation_1.c1_buffer
                elif (workstation_available == "workstation_2"):
                    selected_buffer = workstation_2.c1_buffer
                elif (workstation_available == "workstation_3"):
                    selected_buffer = workstation_3.c1_buffer

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
