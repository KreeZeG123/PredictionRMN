from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.routes import main_routes
from app.api import api_routes

def create_app():
    # Créer une instance de l'application Flask
    app = Flask(__name__, static_folder=Config.STATIC_FOLDER)
    
    # Charger la configuration
    app.config.from_object(Config)

    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Enregistrer les Blueprints
    app.register_blueprint(main_routes)
    app.register_blueprint(api_routes, url_prefix='/api')  # Le préfixe /api est important pour tes routes API
    
    return app
