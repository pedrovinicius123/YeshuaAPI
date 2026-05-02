from ..extensions import db


class Params(db.Model):
    __tablename__ = "Params"
    id = db.Column(db.Integer, primary_key=True)
    # Relação 1:N com Layer
    layers = db.relationship("Layer", backref="param", lazy=True, cascade="all, delete-orphan")
