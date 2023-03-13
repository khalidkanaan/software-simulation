import numpy as np

class CLCG:
    def __init__(self, seed=None):
        self.m = 2**32
        self.a = np.array([1664525, 22695477, 524287, 470745, 17489])
        self.c = np.array([1013904223, 1662033893, 907633385, 1500450271, 351230859])
        self.q = len(self.a)
        self.x = np.zeros(self.q, dtype=np.uint32)
        self.service_times = None
        if seed is not None:
            self.set_seed(seed)

    def set_seed(self, seed):
        self.x[0] = seed
        for i in range(1, self.q):
            self.x[i] = (self.a[i-1]*self.x[i-1] + self.c[i-1]) % self.m

    def rand(self):
        xnew = (np.sum(self.a * self.x) + self.c) % self.m
        self.x[:-1] = self.x[1:]
        self.x[-1] = xnew
        return xnew / self.m

    
    def generate_service_times(self, file_path, num_samples, seed=None, output_file=None):
        if seed is not None:
            self.set_seed(seed)
        with open(file_path, 'r') as f:
            service_times = np.loadtxt(f)
        service_times = np.random.permutation(service_times)[:num_samples]
        self.service_times = service_times
        if output_file is not None:
            with open(output_file, 'w') as f:
                np.savetxt(f, service_times, fmt='%.3f')
        return service_times

