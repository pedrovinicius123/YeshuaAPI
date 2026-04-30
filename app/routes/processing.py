from flask.blueprints import Blueprint
from flask import request
from ..controllers.processing_controller import return_model_params, add_model_param

# Blueprint for neural processing of the model
bp_processing = Blueprint("processing", __name__, url_prefix="/processing")

@bp_processing.route("/", methods=["GET"])
def get_model_params():
    return return_model_params()

@bp_processing.route("/", methods=["POST"])
def add_params_to_model():
    data = request.json
    return add_model_param(data)

