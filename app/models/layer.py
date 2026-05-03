from ..extensions import db
from .neurons import Neuron

# 1. Definição da tabela de associação (use strings para os nomes e FKs)


class Layer(db.Model):
    __tablename__ = 'layer'
    id = db.Column(db.Integer, primary_key=True)
    param_id = db.Column(db.Integer, db.ForeignKey('params.id'), nullable=False) # Garanta que 'params' existe   
    neurons = db.relationship('Neuron', backref='contained_in', lazy=True, cascade='all, delete-orphan')

edges = db.Table('edges',
    db.Column('pred_id', db.Integer, db.ForeignKey('layer.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('layer.id'), primary_key=True)
)

# Self-referential many-to-many
Layer.conns = db.relationship(
    'Layer', 
    secondary=edges, 
    primaryjoin=(edges.c.pred_id == Layer.id), 
    secondaryjoin=(edges.c.post_id == Layer.id), 
    backref=db.backref('reversed', lazy=True), 
    lazy=True
)



