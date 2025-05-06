from flask import Blueprint
from app.api.routes.convert import convert_bp
from app.api.routes.settings import settings_bp
from app.api.routes.predict import predict_bp
from app.api.routes.mock_prediction_model import mock_bp

api_routes = Blueprint('api', __name__)
api_routes.register_blueprint(convert_bp)
api_routes.register_blueprint(settings_bp)
api_routes.register_blueprint(predict_bp)
api_routes.register_blueprint(mock_bp)
