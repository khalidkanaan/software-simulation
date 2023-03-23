import random
import time

class Inspector2(object):

    def __init__(self, env, w2_c2_tracker, w3_c3_tracker):
        self.env = env
        self.service_times22 = []
        self.service_times23 = []
        self.blocked_time = 0
        self.w2_c2_tracker = w2_c2_tracker
        self.w3_c3_tracker = w3_c3_tracker

        
    def run(self, workstation_2, workstation_3):
        print('\***** Inspector 2 Running *****/')
        rv_service_times22 = list(map(float,  open('new_data/generated_servinsp22.dat', 'r').read().splitlines()))
        rv_service_times23 = list(map(float, open('new_data/generated_servinsp23.dat', 'r').read().splitlines()))
        count22 = 0
        count23 = 0
        while True:
            # Randomly decide which component to make
            if bool(random.getrandbits(1)):  
                # Generate service time for component 2 using exponential distribution
                service_time = rv_service_times22[count22]
                self.service_times22.append(service_time)
                # Wait for the service time
                yield self.env.timeout(service_time)

                # Start time of Inspector2 being blocked
                # start_time_blocked = time.time()
                start_time_blocked = self.env.now

                workstation_2.c2_buffer_occupancies.append(workstation_2.c2_buffer.level)

                # Transfered Component 2 to Workstation 2's buffer
                yield workstation_2.c2_buffer.put(1)

                workstation_2.c2_buffer_occupancies.append(workstation_2.c2_buffer.level)
                
                # Add the time Inspector2 spent blocked
                # self.blocked_time += (time.time() - start_time_blocked)
                self.blocked_time += (self.env.now - start_time_blocked)

                print('\***** Transfered C2 to W2 *****/')
                count22 += 1
            else:
                # Generate service time for component 3 using exponential distribution
                service_time = rv_service_times23[count23]
                self.service_times23.append(service_time)
                # Wait for the service time
                yield self.env.timeout(service_time)

                # Start time of Inspector2 being blocked
                # start_time_blocked = time.time()
                start_time_blocked = self.env.now

                workstation_3.c3_buffer_occupancies.append(workstation_3.c3_buffer.level)

                # Transfered Component 3 to Workstation 3's buffer
                yield workstation_3.c3_buffer.put(1)

                workstation_3.c3_buffer_occupancies.append(workstation_3.c3_buffer.level)

                # Add the time Inspector2 spent blocked
                # self.blocked_time += (time.time() - start_time_blocked)
                self.blocked_time += (self.env.now - start_time_blocked)

                print('\***** Transfered C3 to W3 *****/')
                count23 += 1
            

    def start_process(self, workstation_2, workstation_3):
        # Start the run function as a SimPy process
        self.env.process(self.run(workstation_2, workstation_3))
