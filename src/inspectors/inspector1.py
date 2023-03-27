from operator import attrgetter
import time

class Inspector1(object):

    def __init__(self, env, notifier, w1_c1_tracker, w2_c1_tracker, w3_c1_tracker, w1_c1_mutex, w2_c1_mutex, w3_c1_mutex):
        self.env = env
        self.service_times = []
        self.notifier = notifier
        self.blocked_time = 0
        self.w1_c1_tracker = w1_c1_tracker
        self.w2_c1_tracker = w2_c1_tracker
        self.w3_c1_tracker = w3_c1_tracker
        self.w1_c1_mutex = w1_c1_mutex
        self.w2_c1_mutex = w2_c1_mutex
        self.w3_c1_mutex = w3_c1_mutex
        self.count = 0
        
    def run(self, workstation_1, workstation_2, workstation_3):
        print('\***** Inspector 1 Running *****/')
        rv_service_times = list(map(float, open('data/servinsp1.dat', 'r').read().splitlines()))
        while True:
            service_time = rv_service_times[self.count]
            self.service_times.append(service_time)

            # Get list of all buffers with type 1 components
            c1_lst = [workstation_1.c1_buffer, workstation_2.c1_buffer,
                  workstation_3.c1_buffer]
            
            # Find the buffer with the least number of type 1 components, if full wait until a workstation is available
            if (not self.notifier.all_workstations_full()):
                selected_buffer = min(c1_lst, key=attrgetter('level'))
                workstation_chosen = c1_lst.index(selected_buffer) + 1
            else:
                # Start time of Inspector1 being blocked
                start_time_blocked = self.env.now

                while self.notifier.all_workstations_full():
                    print("/********************************** ALL BUFFERS FULL, INSPECTOR 1 WAITING FOR NEXT AVAILABLE C1 BUFFER ****************************/")
                    workstation_available = yield self.notifier.inspector_blocked()

                print("/********************************** INSPECTOR 1 FINISHED WAITING, CHOSE " + workstation_available + " ****************************/")
                if (workstation_available == "workstation_1"):
                    selected_buffer = workstation_1.c1_buffer
                    workstation_chosen = 1
                elif (workstation_available == "workstation_2"):
                    selected_buffer = workstation_2.c1_buffer
                    workstation_chosen = 2
                elif (workstation_available == "workstation_3"):
                    selected_buffer = workstation_3.c1_buffer
                    workstation_chosen = 3

                # Add the time Inspector1 spent blocked
                self.blocked_time += (self.env.now - start_time_blocked)

            # Wait for the service time
            yield self.env.timeout(service_time)

            # Start time of Inspector1 being blocked
            start_time_blocked = self.env.now

            # Add type 1 component to the selected container
            yield selected_buffer.put(1)

            if (workstation_chosen == 1):
                workstation_1.c1_buffer_occupancies.append(workstation_1.c1_buffer.level)
                with self.w1_c1_mutex.request() as req:
                    yield req
                    self.w1_c1_tracker.start_time = self.env.now
                    if (workstation_1.c1_buffer.level == 1):
                        self.w1_c1_tracker.isLatestComponent = False
                    else:
                        self.w1_c1_tracker.isLatestComponent = True
            elif (workstation_chosen == 2):
                workstation_2.c1_buffer_occupancies.append(workstation_2.c1_buffer.level)
                with self.w2_c1_mutex.request() as req:
                    yield req
                    self.w2_c1_tracker.start_time = self.env.now
                    if (workstation_2.c1_buffer.level == 1):
                        self.w2_c1_tracker.isLatestComponent = False
                    else:
                        self.w2_c1_tracker.isLatestComponent = True
            elif (workstation_chosen == 3):
                workstation_3.c1_buffer_occupancies.append(workstation_3.c1_buffer.level)
                with self.w3_c1_mutex.request() as req:
                    yield req
                    self.w3_c1_tracker.start_time = self.env.now
                    if (workstation_3.c1_buffer.level == 1):
                        self.w3_c1_tracker.isLatestComponent = False
                    else:
                        self.w3_c1_tracker.isLatestComponent = True

            # Add the time Inspector1 spent blocked
            self.blocked_time += (self.env.now - start_time_blocked)

            # Print which workstation received the type 1 component
            if selected_buffer is workstation_1.c1_buffer:
                print('\***** Transfered C1 to W1 *****/')
            elif selected_buffer is workstation_2.c1_buffer:
                print('\***** Transfered C1 to W2 *****/')
            elif selected_buffer is workstation_3.c1_buffer:
                print('\***** Transfered C1 to W3 *****/')
            
            self.count += 1

    def start_process(self, workstation_1, workstation_2, workstation_3):
        # Start the run function as a SimPy process
        self.env.process(self.run(workstation_1, workstation_2, workstation_3))
