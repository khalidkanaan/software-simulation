# LCM class used to generate pseudorandom numbers using linear congruential method (LCM)
class LCM:
    
    # Constructor method to initialize the LCM object with input parameters
    def __init__(self, seed, a, c, m):
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m
        # Initialize current value with seed value
        self.current = seed  

    # Method to generate next pseudorandom number in the sequence
    def next(self):
        self.current = ((self.a * self.current) + self.c) % self.m
        return self.current