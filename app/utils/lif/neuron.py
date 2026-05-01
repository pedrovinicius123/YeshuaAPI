from app.utils.lif.functional import *

class LIF:    
    def __init__(id, self):
        self.id = id
        self.tt = 100
        self.last_I = 0
    def __call__(self, I):
        u = lif_differential(I=I, T_total=self.tt)
        self.last_I = I
        return u