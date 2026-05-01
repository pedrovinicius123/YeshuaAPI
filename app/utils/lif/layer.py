from .neuron import LIF
from ...extensions import db
from flask import current_app
from flask import request
import threading
import requests

lock = threading.Lock()

class LIFLayer(threading.Thread):
    def __init__(self, ns, conns):
        self.id = LIFLayer.id
        self.conns = conns
        self.neurons = ns
        self.running = False
        
        threading.Thread.__init__(self)
        
        
    def run(self):
        self.running = True
        while self.running:
            with current_app.app_context(), lock:
                args = request.json
                if self.id in args.get("destiny", []):
                    output = [{dest: neuron(u) for dest, (_,u,_) in zip(args.get("destiny", []), args.get("output", []))} for neuron in self.neurons]
                    output_json = {"destiny": list(self.conns),"output":output}
                    requests.put("http://localhost:5000/processing", json=output_json)
