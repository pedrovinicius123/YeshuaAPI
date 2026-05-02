from ..extensions import db

edges = db.Table("edges",
    db.Column("pred_id", db.Integer, db.ForeignKey("layer.id"), primary_key=True),
    db.Column("post_id", db.Integer, db.ForeignKey("layer.id"), primary_key=True)
)

class Layer(db.Model):
    __tablename__ = "layer"
    id = db.Column(db.Integer, primary_key=True)
    param_id = db.Column(db.Integer, db.ForeignKey("Params.id"), nullable=False)        
    neurons = db.relationship("Neuron", backref="layer", lazy=True, cascade="all, delete-orphan")
    conns = db.relationship(
        'Layer',
        secondary=edges,
        primaryjoin=(edges.c.pred_id == id),
        secondaryjoin=(edges.c.post_id == id),
        backref=db.backref('reversed', lazy='dynamic'),
        lazy='dynamic'
    )
