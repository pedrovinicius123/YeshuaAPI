from routes.processing import bp_processing
from extensions import db, migrate
from utils.response import req_response
from flask import Flask

def create_app():
    app = Flask(__name__)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.errorhandler(404)
    def handle_404(err):
        return req_response(
            status_code=404,
            message="Resource not found",
            data=err,
        )
    
    app.register_blueprint(bp_processing)
    return app
