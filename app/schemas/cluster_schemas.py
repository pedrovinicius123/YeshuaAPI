from ..extensions import marshm
from ..models.params import Params
from ..models.layer import Layer

class LayerSchema(marshm.SQLAlchemyAutoSchema):
    class Meta:
        model = Layer
        load_instance = True
        
    id = marshm.auto_field()
    neurons = marshm.auto_field()

class ParamSchema(marshm.SQLAlchemyAutoSchema):
    class Meta:
        model=Params
        load_instance=True
    
    id = marshm.auto_field()
    layers = marshm.Nested(LayerSchema, many=True)
