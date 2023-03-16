from LCG import LCG

class CLCG:
    def __init__(self):
        self.generator1 = LCG(123456, 1664525, 0, 2 ** 32)
        self.generator2 = LCG(678904, 65539, 0, 2 ** 31)
        self.random_numbers = []
        
    def calc_random_numbers(self):
        for i in range(300):
            xjplus1 = (self.generator1.next() - self.generator2.next()) % (self.generator1.m-1)
            
            if(xjplus1 == 0):
                self.random_numbers.append((self.generator1.m-1)/self.generator1.m)
            else:
                self.random_numbers.append(xjplus1/self.generator1.m)
                
        return self.random_numbers