# THE CLUSTERS
# An alias to separated devices with different layers

from ..utils.lif.layer import LIFLayer, LIF
from ..extensions import db
from ..models.params import Params
from ..models.layer import Layer
from ..models.neurons import Neuron
import networkx as nx
import random


all_models = []


class Cluster:
    def __init__(self, id, nlayers:int=0, conn_prob:float=0.5, n_neurons_per_layer:int=10):
        self.id = id
        self.layers = [LIFLayer(ns=[LIF() for _ in range(n_neurons_per_layer)], conns=None) for _ in range(nlayers)]
        self.g = nx.Graph()
        for i in range(nlayers):
            for j in range(nlayers):
                if i != j and random.random() > 1-conn_prob:
                    self.g.add_edge(i, j)
                    
        for i, l in enumerate(self.layers):
            l.conns = self.g.neighbors(i)
    
    @staticmethod      
    def load(obj):
        def get_layer_params(layers):
            ls = LIFLayer(id=0, ns=None, conns=None)
            for layer in layers:
                ls.id = layer.id
                ls.neurons = get_neuron_params(layer.neurons)
                ls.conns = map(lambda x: x.id, layer.edges)
            return ls
                
        def get_neuron_params(neurons):
            ns = []
            for neuron in neurons:
                n = LIF()
                n.id = neuron.id
                n.tt = neuron.tt
                n.last_I = neuron.last_I
                ns.append(n)
                
            return ns
        
        instance = Cluster(obj.id, 0, 0, 0)
        instance.layers = get_layer_params(obj.params)
        return instance
    
    def save(self):
        def get_layer_params(instance):
            for l, layer in zip(instance.layers, self.layers):
                get_neuron_params(l, layer.neurons)
                l.edges = map(lambda x: x.id, layer.edges)
                instance.params.append(l)                
            db.session.commit()
                            
        def get_neuron_params(layer, neurons):
            for neuron in neurons:
                n = Neuron()
                n.tt = neuron.tt
                n.last_I = neuron.last_I
                layer.neurons.append(n)
            db.session.commit()
                
        instance = Params.query.get(self.id)
        get_layer_params(instance)
    
    def start(self):
        for layer in self.layers:
            layer.start()          
            