from ..extensions import db

class Params(db.Model):
    __tablename__ = "Params"
    id=db.Column(db.Integer, primary_key=True)
    params=db.relationship("Layer", backref="param", lazy=True)
