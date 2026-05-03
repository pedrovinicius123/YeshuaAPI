from ..extensions import db
from sqlalchemy.types import JSON


class Neuron(db.Model):
    __tablename__ = "neuron"
    id = db.Column(db.Integer, primary_key=True)
    layer_id = db.Column(db.Integer, db.ForeignKey("layer.id"), nullable=False)
    tt = db.Column(db.Integer)
    w = db.Column(JSON, nullable=False)
