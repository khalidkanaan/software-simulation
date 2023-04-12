# import random
# import time

# class Inspector2(object):

#     def __init__(self, env, w2_c2_tracker, w3_c3_tracker, w2_c2_mutex, w3_c3_mutex):
#         self.env = env
#         self.service_times22 = []
#         self.service_times23 = []
#         self.blocked_time = 0
#         self.w2_c2_tracker = w2_c2_tracker
#         self.w3_c3_tracker = w3_c3_tracker
#         self.w2_c2_mutex = w2_c2_mutex
#         self.w3_c3_mutex = w3_c3_mutex
#         self.count22 = 0
#         self.count23 = 0

        
#     def run(self, workstation_2, workstation_3):
#         print('\***** Inspector 2 Running *****/')
#         rv_service_times22 = list(map(float,  open('data/servinsp22.dat', 'r').read().splitlines()))
#         rv_service_times23 = list(map(float, open('data/servinsp23.dat', 'r').read().splitlines()))
#         while True:
#             # Check which component has a higher demand
#             if workstation_3.c3_buffer.level == workstation_2.c2_buffer.level:
#                 # Generate service time for component 3 using exponential distribution
#                 service_time = rv_service_times23[self.count23]
#                 self.service_times23.append(service_time)
#                 # Wait for the service time
#                 yield self.env.timeout(service_time)

#                 # Start time of Inspector2 being blocked
#                 start_time_blocked = self.env.now

#                 # Transfer Component 3 to Workstation 3's buffer
#                 yield workstation_3.c3_buffer.put(1)

#                 workstation_3.c3_buffer_occupancies.update({self.env.now : workstation_3.c3_buffer.level})

#                 with self.w3_c3_mutex.request() as req:
#                     yield req
#                     self.w3_c3_tracker.start_time = self.env.now
#                     if (workstation_3.c3_buffer.level == 1):
#                         self.w3_c3_tracker.isLatestComponent = False
#                     else:
#                         self.w3_c3_tracker.isLatestComponent = True

#                 # Add the time Inspector2 spent blocked
#                 self.blocked_time += (self.env.now - start_time_blocked)

#                 print('\***** Transfered C3 to W3 *****/')
#                 self.count23 += 1
#             else:
#                 # Generate service time for component 2 using exponential distribution
#                 service_time = rv_service_times22[self.count22]
#                 self.service_times22.append(service_time)
#                 # Wait for the service time
#                 yield self.env.timeout(service_time)

#                 # Start time of Inspector2 being blocked
#                 start_time_blocked = self.env.now

#                 # Transfer Component 2 to Workstation 2's buffer
#                 yield workstation_2.c2_buffer.put(1)

#                 workstation_2.c2_buffer_occupancies.update({self.env.now : workstation_2.c2_buffer.level})

#                 with self.w2_c2_mutex.request() as req:
#                     yield req
#                     self.w2_c2_tracker.start_time = self.env.now
#                     if (workstation_2.c2_buffer.level == 1):
#                         self.w2_c2_tracker.isLatestComponent = False
#                     else:
#                         self.w2_c2_tracker.isLatestComponent = True
                
#                 # Add the time Inspector2 spent blocked
#                 self.blocked_time += (self.env.now - start_time_blocked)

#                 print('\***** Transfered C2 to W2 *****/')
#                 self.count22 += 1
            

#     def start_process(self, workstation_2, workstation_3):
#         # Start the run function as a SimPy process
#         self.env.process(self.run(workstation_2, workstation_3))
