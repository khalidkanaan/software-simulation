from LCM import LCM

# CLCG used to generate random numbers using Combined Linear Congruential Generators (CLCG)
class CLCG:
    def __init__(self, num_rn):
        # define the first and second LCM generators each with their respective seed, a, c, and m values
        self.generator1 = LCM(319683741, 40014, 0, 2147483563)
        self.generator2 = LCM(817968219, 40692, 0, 2147483399)

        # defines the number of random numbers to generate
        self.num_rn = num_rn
        # empty list used store the generated random numbers
        self.random_numbers = []
        
    # generates the specified number of random numbers using the CLCG algorithm
    def calc_random_numbers(self):

        for i in range(self.num_rn):
            # Generate the next random number in the sequence using the two LCM generators and the CLCG algorithm
            xjplus1 = (self.generator1.next() - self.generator2.next()) % (self.generator1.m-1)
            
            # If the generated random number is 0, append (m_1-1)/m_1 to the list of random numbers
            if(xjplus1 == 0):
                self.random_numbers.append((self.generator1.m-1)/self.generator1.m)
            # Otherwise, append xjplus1/m_1 to the list of random numbers
            else:
                self.random_numbers.append(xjplus1/self.generator1.m)
                
        # Return the list of generated random numbers
        return self.random_numbers
    
    # saves the generated random numbers to a file
    def save_rns_to_file(self, file_name):
        # calling the calc_random_numbers() to generate the random numbers
        self.calc_random_numbers()
        # write the random numbers to the file with specified path
        with open(file_name, 'w') as f:
            for rn in self.random_numbers:
                f.write(str(rn) + '\n')
