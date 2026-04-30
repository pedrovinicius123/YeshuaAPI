import numpy as np
from ..core.model import model
from ..utils.response import req_response


# There we have the controllers of the routes, wich are used for
# managing the connections between the layers (nodes) and
# Neuron segments.

def return_model_params():
    return req_response(message="Model params", data=model.params)

def add_model_param(data):
    model.add(data)
    return req_response(message="Model params added", data=model.params)
