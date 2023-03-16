import numpy as np
from LCG import LCG

class CLCG:
    def __init__(self, file_path, num_service_times, seeds, params):
        self.service_times = self._read_service_times(file_path)
        self.mean = np.mean(self.service_times)
        self.std_dev = np.std(self.service_times)
        self.num_service_times = num_service_times
        
        self.generators = []
        for seed, (a, c, m) in zip(seeds, params):
            generator = LCG(seed, a, c, m)
            self.generators.append(generator)

    def _read_service_times(self, file_path):
        with open(file_path, 'r') as f:
            data = [float(line.strip()) for line in f.readlines()]
        return data

    def next(self):
        values = []
        for generator in self.generators:
            values.append(generator.next())
        
        new_value = (values[0] - values[1]) % (self.generators[0].m - 1)
        
        if new_value > 0:
            new_value = new_value/self.generators[0].m
        elif new_value == 0:
            new_value = (self.generators[0].m-1)/self.generators[0].m
    
        # combined = sum(generator.next() for generator in self.generators) / len(self.generators)
        return new_value # combined * self.std_dev + self.mean

    def reset(self):
        for generator in self.generators:
            generator.reset()