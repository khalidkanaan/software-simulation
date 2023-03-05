class Notifier(object):

    def __init__(self):
        self.w1_full = False
        self.w2_full = False
        self.w3_full = False
        
    def all_workstations_full(self):
        return self.w1_full and self.w2_full and self.w3_full
