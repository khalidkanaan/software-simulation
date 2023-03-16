class LCG:
    def __init__(self, seed, a, c, m):
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m
        self.current = seed

    def next(self):
        self.current = (self.a * self.current + self.c) % self.m
        return self.current / self.m

    def reset(self):
        self.current = self.seed