import threading, time
from ..utils.response import req_response
from ..core.clusters import Cluster, all_models
from ..models.params import Params
from ..schemas.cluster_schemas import *

# There we have the controllers of the routes, wich are used for
# managing the connections between the layers (nodes) and
# Neuron segments.

params_schema = ParamSchema(many=True)
param_schema = ParamSchema()

def return_model_params(id):
    cluster = Cluster.load(Params.query.get_or_404(id))
    return req_response(message="Model params", data={k: v.__repr__() for k, v in cluster.__dict__().items()})

def proc(data, id):
    cluster = Cluster.load(Params.query.get_or_404(id))
    for layer in data.get("layers", []):
        cluster.layers[layer](data.get("output"))

    return req_response(message="Model processed data successfully", data={k: v.__repr__() for k, v in cluster.__dict__().items()})

def gn(kwds):
    instance = param_schema.load(kwds)
    cluster = Cluster(*{k: v for k, v in instance.__dict__().items() if k in ["id", "nlayers", "conn_prob", "n_neurons_per_layer"]})
    all_models.append(cluster)

def save_all():
    for m in all_models:
        m.save()
        time.sleep(0.1)
        
cluster_saving_thread = threading.Thread(target=save_all)
cluster_saving_thread.start()
