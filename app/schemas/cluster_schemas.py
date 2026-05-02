from ..extensions import marshm
from ..models.params import Params
from ..models.layer import Layer
from ..models.neurons import Neuron

class NeuronSchema(marshm.SQLAlchemyAutoSchema):
    class Meta:
        model=Neuron
        load_instance = True
        
    id = marshm.auto_field()
    tt = marshm.auto_field()
    w = marshm.auto_field()

class LayerSchema(marshm.SQLAlchemyAutoSchema):
    class Meta:
        model = Layer
        load_instance = True
        
    id = marshm.auto_field()
    neurons = marshm.Nested(NeuronSchema, many=True)

class ParamSchema(marshm.SQLAlchemyAutoSchema):
    class Meta:
        model=Params
        load_instance=True
    
    id = marshm.auto_field()
    layers = marshm.Nested(LayerSchema, many=True)
