from .functional import *
from ...models.neurons import Neuron
import time

class LIF:    
    def __init__(self):
        nid = Neuron.query.order_by(Neuron.id.desc()).first()
        if not nid:
            nid = 1

        self.id = nid
        self.tt = 30
        self.last_I = 0
        self.last_timestamp = time.time()
        self.w = {}
        
        
    def __call__(self, I):
        u = lif_differential(I=I, T_total=self.tt)
        if u > 0:
            self.last_timestamp = time.time()
        return u