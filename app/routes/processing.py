from flask.blueprints import Blueprint
from flask import request
from ..controllers.processing_controller import (
    return_model_params,
    proc,
    delete,
    gn
)

# Blueprint for neural processing of the model
bp_processing = Blueprint("processing", __name__, url_prefix="/processing")

@bp_processing.route("/<int:id>", methods=["GET"])
def get_model_params(id):
    return return_model_params(id)

@bp_processing.route("/<int:id>", methods=["PUT"])
def receive_input(id):
    data = request.json
    return proc(data, id)

@bp_processing.route("/<int:id>", methods=["DELETE"])
def delete_cluster(id):
    return delete(id)

@bp_processing.route("/", methods=["POST"])
def generate_model():
    return gn(request.json)
