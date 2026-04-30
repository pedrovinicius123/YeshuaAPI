# THE CLUSTERS
# An alias to separated devices with different layers

from ..utils.lif.layer import LIFLayer

class Cluster:
    def __init__(self, nlayers:int, conn_prob:float=0.5):
        self.layers = [LIFLayer() for _ in range(nlayers)]

