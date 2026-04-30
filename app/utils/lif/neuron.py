from app.utils.lif.functional import *

class LIF:    
    def __call__(self, *args, **kwds):
        u = calc_delta_t_neuron(*args, **kwds)
        return u
