from .functional import *
import time

class LIF:    
    def __init__(self):
        self.tt = 100
        self.last_timestamp = time.time()
        self.w = {}       
        
    def __call__(self, I):
        u = lif_differential(I=I, T_total=self.tt)
        if u > 0:
            self.last_timestamp = time.time()
        return u