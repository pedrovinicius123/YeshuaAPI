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
        
        for i, neuron in zip(conns, self.neurons):
            neuron.w[i] = np.random.rand(len(ns))
            
        self.running = False
        self.req = {}
        
        threading.Thread.__init__(self)
        
        
    def run(self):
        self.running = True
        while self.running:
            with current_app.app_context(), lock:
                total_neuron_I = 0 
                for neuron in self.neurons:
                    # TIMESTAMP
                    current_timestamp = time.time()
                    
                    # INPUT FEATURES
                    inp = np.array(self.req.get("output", []))
                    ant = self.req.get("from")
                                        
                    # PROCESSING
                    tot = 0
                    for i, (w, n) in enumerate(zip(neuron.w[ant], self.req.get("from_neurons", []))):                   
                        out = inp*w
                        tot += out
                        prev_timestamp = n["last_timestamp"]                        
                        neuron.w[ant][i] = update_stdp(neuron[ant][i], prev_timestamp, current_timestamp)                           
                              
                output = [sum([neuron(u) for u in self.req.get("output", [])]) for neuron in self.neurons]
                output_json = {
                    "from":self.id,
                    "from_neurons": [{k:v for k, v in neuron.__dict__.items() if k != "w"} for neuron in self.neurons],
                    "layers": list(self.conns),
                    "output":output,
                    "timestamp":time.time()
                }
                
                requests.put("http://localhost:5000/processing", json=output_json)
