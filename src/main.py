# This code implements a simulation of a production line with inspectors and workstations
import simpy
from helper_functions import find_list_mean
from helper_functions import get_batch_means
from inspectors.inspector1 import Inspector1
from inspectors.inspector2 import Inspector2
from workstations.workstation1 import Workstation1
from workstations.workstation2 import Workstation2
from workstations.workstation3 import Workstation3
from notifier import Notifier
from RVG import RVG
from component_tracker import ComponentTracker

# The main method of the program, responsible for setting up and running the simulation
if __name__ == '__main__':
      # Define the runtime of the simulation in seconds
      RUNTIME = 3000

      print('Creating simulation environment')
      # Create the simulation environment
      simulation_env = simpy.Environment()

      notifier = Notifier(simulation_env)

      # Generating service times for Inspector1, Inspector2, Workstation1, Workstation2, Workstation3 using RVG which uses CLCG
      random_servinsp1 = RVG('data/servinsp1.dat', 300, 'new_data/generated_servinsp1.dat').generate_service_times()
      random_servinsp22 = RVG('data/servinsp22.dat', 300, 'new_data/generated_servinsp22.dat').generate_service_times()
      random_servinsp23 = RVG('data/servinsp23.dat', 300, 'new_data/generated_servinsp23.dat').generate_service_times()

      random_ws1 = RVG('data/ws1.dat', 300, 'new_data/generated_ws1.dat').generate_service_times()
      random_ws2 = RVG('data/ws2.dat', 300, 'new_data/generated_ws2.dat').generate_service_times()
      random_ws3 = RVG('data/ws3.dat', 300, 'new_data/generated_ws3.dat').generate_service_times()

      # Component Trackers
      w1_c1_tracker = ComponentTracker()
      w2_c1_tracker = ComponentTracker()
      w2_c2_tracker = ComponentTracker()
      w3_c1_tracker = ComponentTracker()
      w3_c3_tracker = ComponentTracker()

      # Mutexes
      w1_c1_mutex = simpy.Resource(simulation_env, capacity=1)
      w2_c1_mutex = simpy.Resource(simulation_env, capacity=1)
      w2_c2_mutex = simpy.Resource(simulation_env, capacity=1)
      w3_c1_mutex = simpy.Resource(simulation_env, capacity=1)
      w3_c3_mutex = simpy.Resource(simulation_env, capacity=1)


      # Create instances of the inspector and workstation classes
      inspector_1 = Inspector1(simulation_env, notifier, w1_c1_tracker, w2_c1_tracker, w3_c1_tracker, w1_c1_mutex, w2_c1_mutex, w3_c1_mutex)
      inspector_2 = Inspector2(simulation_env, w2_c2_tracker, w3_c3_tracker, w2_c2_mutex, w3_c3_mutex)
      workstation_1 = Workstation1(simulation_env, notifier, w1_c1_tracker, w1_c1_mutex)
      workstation_2 = Workstation2(simulation_env, notifier, w2_c1_tracker, w2_c2_tracker, w2_c1_mutex, w2_c2_mutex)
      workstation_3 = Workstation3(simulation_env, notifier, w3_c1_tracker, w3_c3_tracker, w3_c1_mutex, w3_c3_mutex)

      # Start the inspector processes
      inspector_1.start_process(workstation_1, workstation_2, workstation_3)
      inspector_2.start_process(workstation_2, workstation_3)

      # Start the workstation processes
      workstation_1.start_process()
      workstation_2.start_process()
      workstation_3.start_process()

      # Run the simulation for the defined runtime
      simulation_env.run(until=RUNTIME)

      # Print the results of the simulation
      print('\n====================\n' +
            ' Simulation results' +
            '\n====================\n')
      # Print the execution times for each inspector and workstation
      print(f'Execution times:\n'
            f'Inspector 1 {inspector_1.service_times} \n\n'
            f'Inspector 22 {inspector_2.service_times22} \n\n'
            f'Inspector 23 {inspector_2.service_times23} \n\n'
            f'Workstation 1 {workstation_1.service_times} \n\n'
            f'Workstation 2 {workstation_2.service_times} \n\n'
            f'Workstation 3 {workstation_3.service_times} \n\n')
      # Print the average service time for each inspector and workstation
      print(f'\nAverage service times:\n'
            f'Inspector 1 - {find_list_mean(inspector_1.service_times)}, '
            f'Inspector 22 - {find_list_mean(inspector_2.service_times22)}, '
            f'Inspector 23 - {find_list_mean(inspector_2.service_times23)}, '
            f'\nWorkstation 1 - {find_list_mean(workstation_1.service_times)}, '
            f'Workstation 2 - {find_list_mean(workstation_2.service_times)}, '
            f'Workstation 3 - {find_list_mean(workstation_3.service_times)}\n'
            f'Total execution time: 1500\n'
            f'\nComponents Inspected:\n'
            f'{inspector_1.count} inspected of C1, {inspector_2.count22} inspected of C2, {inspector_2.count23} inspected of C3\n'
            f'\nProducts produced:\n'
            f'{workstation_1.p1} of product 1, {workstation_2.p2} of product 2, {workstation_3.p3} of product 3\n')

      print(f'Heuristics:\n'
            f'Inspector 1 Blocked Time (as fraction of total simulation time) - {inspector_1.blocked_time / RUNTIME} \n'
            f'Inspector 2 Blocked Time (as fraction of total simulation time) - {inspector_2.blocked_time / RUNTIME} \n\n'
            f'Workstation 1 Idle Time (as fraction of total simulation time) - {workstation_1.idle_time / RUNTIME} \n'
            f'Workstation 2 Idle Time (as fraction of total simulation time) - {workstation_2.idle_time / RUNTIME} \n'
            f'Workstation 3 Idle Time (as fraction of total simulation time) - {workstation_3.idle_time / RUNTIME} \n\n'
            f'Product 1 Throughput (# of Product 1 per second) - {workstation_1.p1 / RUNTIME} \n'
            f'Product 2 Throughput (# of Product 2 per second) - {workstation_2.p2 / RUNTIME} \n'
            f'Product 3 Throughput (# of Product 3 per second) - {workstation_3.p3 / RUNTIME} \n\n'
            f'Workstation 1 C1 Avg Buffer Occupancy - {sum(workstation_1.c1_buffer_occupancies.values()) / len(workstation_1.c1_buffer_occupancies)} \n'
            f'Workstation 2 C1 Avg Buffer Occupancy - {sum(workstation_2.c1_buffer_occupancies.values()) / len(workstation_2.c1_buffer_occupancies)} \n'
            f'Workstation 3 C1 Avg Buffer Occupancy - {sum(workstation_3.c1_buffer_occupancies.values()) / len(workstation_3.c1_buffer_occupancies)} \n'
            f'Workstation 2 C2 Avg Buffer Occupancy - {sum(workstation_2.c2_buffer_occupancies.values()) / len(workstation_2.c2_buffer_occupancies)} \n'
            f'Workstation 3 C3 Avg Buffer Occupancy - {sum(workstation_3.c3_buffer_occupancies.values()) / len(workstation_3.c3_buffer_occupancies)} \n\n'
            f'Workstation 1 C1 Avg Time In Buffer - {sum(w1_c1_tracker.total_times) / len(w1_c1_tracker.total_times)} \n'
            f'Workstation 2 C1 Avg Time In Buffer - {sum(w2_c1_tracker.total_times) / len(w2_c1_tracker.total_times)} \n'
            f'Workstation 2 C2 Avg Time In Buffer - {sum(w2_c2_tracker.total_times) / len(w2_c2_tracker.total_times)} \n'
            f'Workstation 3 C1 Avg Time In Buffer - {sum(w3_c1_tracker.total_times) / len(w3_c1_tracker.total_times)} \n'
            f'Workstation 3 C3 Avg Time In Buffer - {sum(w3_c3_tracker.total_times) / len(w3_c3_tracker.total_times)} \n')
      
      print(f'Batch intervals:\n'
            f'Workstation 1 C1 Batch Means - {get_batch_means(workstation_1.c1_buffer_occupancies)} \n'
            f'Workstation 2 C1 Batch Means - {get_batch_means(workstation_2.c1_buffer_occupancies)} \n'
            f'Workstation 3 C1 Batch Means - {get_batch_means(workstation_3.c1_buffer_occupancies)} \n'
            f'Workstation 2 C2 Batch Means - {get_batch_means(workstation_2.c2_buffer_occupancies)} \n'
            f'Workstation 3 C3 Batch Means - {get_batch_means(workstation_3.c3_buffer_occupancies)} \n') 
