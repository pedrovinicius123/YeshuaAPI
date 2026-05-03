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
        p = Params.query.order_by(Params.id.desc()).first()
        self.id = p.id if p else 1
        self.g = nx.Graph()
        
        for i in range(nlayers):
            for j in range(nlayers):
                if i != j and random.random() > 1-conn_prob:
                    self.g.add_edge(i, j)
        
        self.layers = [LIFLayer(ns=[LIF() for _ in range(n_neurons_per_layer)], conns=list(self.g.neighbors(i))) for i in range(nlayers)]
        print(len(self.layers))             
        self.save()
        threading.Thread.__init__(self)
    
    @staticmethod      
    def load(obj):
        print(obj.layers[10].neurons)
        instance = Cluster(obj.id, 0, 0, 0)
        for i in range(len(obj.layers)):
            print(i, obj.layers[i].neurons)
            ls = LIFLayer(ns=[], conns=list(map(lambda x: x.id, obj.layers[i].conns)))
            ls.id = obj.layers[i].id
            ls.conns = [c.id for c in obj.layers[i].conns]                          
            for neuron in obj.layers[i].neurons:
                n = LIF()
                n.id = neuron.id
                n.tt = neuron.tt
                n.w = neuron.w
                ls.neurons.append(n)
                
            instance.layers.append(ls)                        
        return instance
    
    def save(self):
        with self.app.app_context():
            instance = Params.query.get(self.id)
            if not instance:
                instance = Params(id=self.id)
                db.session.add(instance)
                

            # Clear existing layers and their relationships
            for layer in instance.layers:
                db.session.delete(layer)

            # Create new layer models
            layer_models = []
            #print("LAYERS", self.layers)
            for lif_layer in self.layers:
                layer_model = Layer(param_id=instance.id)
                db.session.add(layer_model)
                db.session.flush()  # Get the layer ID without committing

                # Add neurons
                for lif_neuron in lif_layer.neurons:
                    neuron_model = Neuron(layer_id=layer_model.id, tt=lif_neuron.tt, w=lif_neuron.w)
                    db.session.add(neuron_model)
                
                layer_models.append(layer_model)

            db.session.flush()  # Flush before setting connections

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
            for layer in self.layers:
                if not layer.is_alive:
                    layer.start()
                    
            with self.app.app_context():
                self.save()
            time.sleep(30)
            