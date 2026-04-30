from app.utils.lif.neuron import LIF
import numpy as np

class LIFLayer:
    def __init__(self, ns:int):
        self.neurons = [LIF() for _ in range(ns)]

    def __call__(self, *args):
        return np.array([[neuron(arg) for arg in enumerate(args)] for neuron in self.neurons])
