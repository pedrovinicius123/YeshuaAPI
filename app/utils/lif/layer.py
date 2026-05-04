from ...models.layer import Layer
from flask import current_app
from .functional import update_stdp
import time
import threading
import requests
import numpy as np

lock = threading.Lock()

class LIFLayer(threading.Thread):
    def __init__(self, ns, conns):
        lid = Layer.query.order_by(Layer.id.desc()).first()
        if not lid:
            lid = 1
        self.id = lid
        self.conns = conns
        self.neurons = ns
        
        for neuron in self.neurons:
            for i in conns:
                neuron.w[i] = np.random.rand(len(ns)).tolist()
            
        self.running = False
        self.req = {}
        
        threading.Thread.__init__(self)
        
        
    def run(self):
        self.running = True
        while self.running:
            if self.req:              
                with lock:
                    tot = 0
                    output = []
                    timestamps = []
                    for neuron in self.neurons:
                        # TIMESTAMP
                        
                        
                        # INPUT FEATURES
                        inp = np.array(self.req.get("output", []))
                        ant = self.req.get("from")
                                   
                                   
                        tot = 0     
                        # PROCESSING
                        if ant == None:
                            for i in inp:
                                tot += i
                        elif not self.req.get("from_neurons_timestamp", []):
                            current_timestamp = time.time()
                            prev_timestamp = time.time()  
                            print(neuron.w)  
                            
                            for i, we in enumerate(neuron.w[ant]):                   
                                out = inp[i] * we
                                tot += out                        
                                neuron.w[ant][i] = update_stdp(neuron.w[ant][i], prev_timestamp, current_timestamp)
                                
                        else:
                            for i, (we, t) in enumerate(zip(neuron.w[ant], self.req.get("from_neurons_timestamp"))):
                                out = inp[i] * we
                                tot += out             
                                prev_timestamp = t          
                                neuron.w[ant][i] = update_stdp(neuron.w[ant][i], prev_timestamp, neuron.last_timestamp)
                        
                        tot = neuron(tot)
                        output.append(tot)
                        timestamps.append(neuron.last_timestamp)
                        
                    output_json = {
                        "from":self.id,
                        "from_neurons_timestamp": timestamps,
                        "layers": list(self.conns),
                        "output":output,
                    }
                    
                    print(output_json)
                    self.req = {}
                    
                    requests.put("http://localhost:5000/processing", json=output_json)
