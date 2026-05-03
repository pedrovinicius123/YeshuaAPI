from app import create_app
from app.models.layer import Layer
from app.models.params import Params
from app.models.neurons import Neuron
from app.extensions import db
from app.core.clusters import Cluster

app = create_app()

with app.app_context():
    # Clean up old test data
    db.session.query(Neuron).delete()
    db.session.query(Layer).delete()
    db.session.query(Params).delete()
    db.session.commit()
    
    # Create a cluster with 3 layers and 2 neurons per layer
    cluster = Cluster(id=1, nlayers=3, conn_prob=0.5, n_neurons_per_layer=2)
    
    # Load the saved data and verify
    p = db.session.get(Params, 1)
    print(f"Params ID: {p.id}")
    print(f"Number of layers: {len(p.layers)}")
    
    for idx, layer in enumerate(p.layers):
        print(f"  Layer {idx}: ID={layer.id}, neurons={len(layer.neurons)}")
        for nidx, neuron in enumerate(layer.neurons):
            print(f"    Neuron {nidx}: ID={neuron.id}, tt={neuron.tt}")

