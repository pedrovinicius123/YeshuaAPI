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
                with current_app._get_current_app().app_context(), lock:
                    tot = 0
                    for neuron in self.neurons:
                        # TIMESTAMP
                        current_timestamp = time.time()
                        
                        # INPUT FEATURES
                        inp = np.array(self.req.get("output", []))
                        ant = self.req.get("from")
                                            
                        # PROCESSING
                        for i, (we, n) in enumerate(zip(neuron.w[ant], self.req.get("from_neurons", []))):                   
                            out = inp[i] * we
                            tot += out
                            prev_timestamp = n["last_timestamp"]                        
                            neuron.w[ant][i] = update_stdp(neuron.w[ant][i], prev_timestamp, current_timestamp)                        
                                
                    output = [sum([neuron(u) for u in self.req.get("output", [])]) for neuron in self.neurons]
                    output_json = {
                        "from":self.id,
                        "from_neurons": [{k:v for k, v in neuron.__dict__.items() if k != "w"} for neuron in self.neurons],
                        "layers": list(self.conns),
                        "output":output,
                        "timestamp":time.time()
                    }
                    
                    print(output_json)
                    self.req = {}
                    
                    requests.put("http://localhost:5000/processing", json=output_json)
