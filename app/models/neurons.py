from ..extensions import db


class Neuron(db.Model):
    __tablename__ = "Neuron"
    id = db.Column(db.Integer, primary_key=True)
    layer_id = db.Column(db.Integer, db.ForeignKey("param.id"), nullable=False)
    tt = db.Column(db.Integer)
    last_I = db.Column(db.Float)
