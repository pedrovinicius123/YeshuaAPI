from flask import current_app
from ..extensions import db
from ..utils.response import req_response
from ..core.clusters import Cluster
from ..models.params import Params
from ..schemas.cluster_schemas import *

# There we have the controllers of the routes, wich are used for
# managing the connections between the layers (nodes) and
# Neuron segments.

params_schema = ParamSchema(many=True)
param_schema = ParamSchema()

def return_model_params(id):
    with current_app.app_context():
        p = Params.query.get_or_404(id)
        #print(p.layers)
        cluster = Cluster.load(p)
        return req_response(message="Model params", data={k: v.__repr__() for k, v in cluster.__dict__.items()})

def proc(data, id):
    with current_app.app_context():
        p = Params.query.get_or_404(id)
        print(p.layers)
        cluster = Cluster.load(p)
        if not cluster.is_alive():
            cluster.start()
        
        for layer in data.get("layers", []):
            print(data)
            cluster.layers[layer].req = data

        return req_response(message="Model processed data successfully", data={k: v.__repr__() for k, v in cluster.__dict__.items()})

def delete(id:int):
    p = Params.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return req_response(message="CLUSTER DELETED")

def gn(kwds):
    with current_app.app_context():
        id = 1
        p = Params.query.order_by(Params.id.desc()).first()
        if p is not None:
            id = p.id + 1
            
        print(kwds)
        cluster = Cluster(id, **kwds)
        cluster.save()            
        cluster.start()

        return req_response(
            status_code=201,
            message="Model created sucessfully",
            data=""
        )
