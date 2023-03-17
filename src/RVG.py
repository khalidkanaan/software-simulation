import numpy as np
from CLCG import CLCG

# Random variant generation class for generating random service times using inverse of the CDF
class RVG:
    def __init__(self, file_path, num_service_times, output_file=None):
            # path to the .dat historical data file containing service times
            self.file_path = file_path
            # number of service times that need to be generated
            self.num_service_times = num_service_times
            # the path and name of the output file containing randomly generated service times based on historical data
            self.output_file = output_file

            # list containing the service times from the historical data file
            self.service_times = self.read_service_times()
            # lambda value = 1/mean(historical)
            self.lmbda = 1/(np.mean(self.service_times))
            # n random numbers generated using CLCG
            self.random_numbers = CLCG(num_service_times).calc_random_numbers()

    # Reads the service times from the historical .dat file and returns them as a list
    def read_service_times(self):
            with open(self.file_path, 'r') as f:
                data = [float(line.strip()) for line in f.readlines()]
            return data

    # Generates the new service times using the inverse of the CDF
    def generate_service_times(self):
        generated_service_times = []
        # if the path to the output file is specified write random service times to file
        if self.output_file is not None:
            with open(self.output_file, 'w') as f:
                for rn in self.random_numbers:
                    service_time = -(np.log(1 - rn)/self.lmbda)
                    f.write(str(round(service_time, 3)) + '\n')
                    generated_service_times.append(service_time)
         # if the path to the output file is not specified return the random service times     
        else:
            for rn in self.random_numbers:
                 service_time = -(np.log(1 - rn)/self.lmbda)
                 generated_service_times.append(service_time)
        return generated_service_times
    

        