# This code implements a simulation of a production line with inspectors and workstations
import simpy
from helper_functions import find_list_mean
from inspectors.inspector1 import Inspector1
from inspectors.inspector2 import Inspector2
from workstations.workstation1 import Workstation1
from workstations.workstation2 import Workstation2
from workstations.workstation3 import Workstation3
from notifier import Notifier

# The main method of the program, responsible for setting up and running the simulation
if __name__ == '__main__':
    # Define the runtime of the simulation in seconds
    RUNTIME = 1500

    print('Creating simulation environment')
    # Create the simulation environment
    simulation_env = simpy.Environment()

    # Event to be triggered for Inspector 1
    # create an empty list to hold the events
    event_list = []
    event_index = [0]

    # create 10 events and append them to the list
    for i in range(10):
      event_list.append(simpy.events.Event(simulation_env))

    resource = simpy.Resource(simulation_env, capacity=1)

    notifier = Notifier()

    # Create instances of the inspector and workstation classes
    inspector_1 = Inspector1(simulation_env, event_list, event_index)
    inspector_2 = Inspector2(simulation_env)
    workstation_1 = Workstation1(simulation_env, event_list, event_index, resource, notifier)
    workstation_2 = Workstation2(simulation_env, event_list, event_index, resource, notifier)
    workstation_3 = Workstation3(simulation_env, event_list, event_index, resource, notifier)

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
    print(f'Execution times\n'
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
          f'Total execution time: {RUNTIME}\n'
          f'\nProducts produced:\n'
          f'{workstation_1.p1} of product 1, {workstation_2.p2} of product 2, {workstation_3.p3} of product 3\n')

