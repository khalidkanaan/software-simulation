import simpy

class Notifier(object):

    def __init__(self, env):
        self.env = env
        self.w1_full = False
        self.w2_full = False
        self.w3_full = False
        self.event = None
        
    def all_workstations_full(self):
        return self.w1_full and self.w2_full and self.w3_full
    
    def inspector_blocked(self):
        assert self.event is None, "INFO: Inspector1 got blocked a second time before unblocking"
        self.event = simpy.events.Event(self.env)
        return self.event
    
    def maybe_unblock_inspector(self, workstation):
        if self.event is None:
            return print("INFO: Inspector1 is not currently blocked, do nothing")
        self.event.succeed(workstation)
        self.event = None # remove reference so we don't trigger a second time
