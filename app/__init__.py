from app.routes.processing import bp_processing
from app.extensions import db, migrate, marshm
from app.utils.response import req_response
from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    marshm.init_app(app)
    
    @app.errorhandler(404)
    def handle_404(err):
        return req_response(
            status_code=404,
            message="Resource not found",
            data=err.__repr__(),
        )
    
    app.register_blueprint(bp_processing)
    return app
