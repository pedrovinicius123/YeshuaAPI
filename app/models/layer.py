from ..extensions import db


class Layer(db.Model):
    __tablename__ = "Layer"
    id = db.Column(db.Integer, primary_key=True)
    param_id = db.Column(db.Integer, db.ForeignKey("params.id"), nullable=False)
    neurons = db.relationship("Neuron", backref="layer", lazy=True)
    edges = db.relationship(
        'Layer', 
        secondary='network',
        primaryjoin='Layer.id==network.c.source_id',
        secondaryjoin='Layer.id==network.c.target_id',
        backref='connected_to'
    )

# Tabela de associação para os links do grafo
network = db.Table('network',
    db.Column('source_id', db.Integer, db.ForeignKey('Layer.id')),
    db.Column('target_id', db.Integer, db.ForeignKey('Layer.id'))
)
