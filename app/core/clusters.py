# THE CLUSTERS
# An alias to separated devices with different layers

from flask import current_app
from ..utils.lif.layer import LIFLayer
from ..utils.lif.neuron import LIF
from ..extensions import db
from ..models.params import Params
from ..models.layer import Layer
from ..models.neurons import Neuron
import networkx as nx
import random
import threading
import time


class Cluster(threading.Thread):
    def __init__(self, id, nlayers:int=0, conn_prob:float=0.5, n_neurons_per_layer:int=10, **kwargs):
        self.app = current_app._get_current_object()
        self.id = id
        
        self.layers = [LIFLayer(ns=[LIF() for _ in range(n_neurons_per_layer)], conns=None) for _ in range(nlayers)]
        print(len(self.layers))
        self.g = nx.Graph()
        
        for i in range(nlayers):
            for j in range(nlayers):
                if i != j and random.random() > 1-conn_prob:
                    self.g.add_edge(i, j)
                    
        for i, l in enumerate(self.layers):
            l.conns = self.g.neighbors(i)
        threading.Thread.__init__(self)
    
    @staticmethod      
    def load(obj):
        def get_layer_params(layers):
            tot = []
            for layer in layers:
                ls = LIFLayer(ns=None, conns=None)
                ls.id = layer.id
                ls.neurons = get_neuron_params(layer.neurons)
                ls.conns = map(lambda x: x.id, layer.conns)
                tot.append(ls)
                
            return tot
                
        def get_neuron_params(neurons):
            ns = []
            for neuron in neurons:
                n = LIF()
                n.id = neuron.id
                n.tt = neuron.tt
                n.w = neuron.w
                ns.append(n)
                
            return ns
        
        instance = Cluster(obj.id, 0, 0, 0)
        instance.layers = get_layer_params(obj.layers)
        print(instance.layers)
        return instance
    
    def save(self):
        with self.app.app_context():
            instance = Params.query.get(self.id)
            if not instance:
                instance = Params(id=self.id)
                db.session.add(instance)
                db.session.commit()  # Ensure instance has an ID

            # Clear existing layers and their relationships
            for layer in instance.layers:
                db.session.delete(layer)
            db.session.commit()

            # Create new layer models
            layer_models = []
            for lif_layer in self.layers:
                layer_model = Layer(param_id=instance.id)
                db.session.add(layer_model)
                db.session.commit()  # Get layer ID

                # Add neurons
                for lif_neuron in lif_layer.neurons:
                    neuron_model = Neuron(layer_id=layer_model.id, tt=lif_neuron.tt, last_I=lif_neuron.last_I)
                    db.session.add(neuron_model)

                layer_models.append(layer_model)

            # Set connections
            for i, lif_layer in enumerate(self.layers):
                layer_model = layer_models[i]
                for conn_index in lif_layer.conns:
                    connected_layer = layer_models[conn_index]
                    if connected_layer not in layer_model.conns:
                        layer_model.conns.append(connected_layer)

            db.session.commit()
    
    def run(self):
        running = True
        while running:
            time.sleep(.5)
            for layer in self.layers:
                if not layer.is_alive:
                    layer.start()
                    
            with self.app.app_context():
                self.save()
            