from ..extensions import db
from .layer import Layer


class Params(db.Model):
    __tablename__ = "params"
    id = db.Column(db.Integer, primary_key=True)
    # Relação 1:N com Layer
    layers = db.relationship("Layer", backref="param", lazy=True, cascade="all, delete-orphan")
