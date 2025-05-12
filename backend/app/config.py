import os
import sys
from platformdirs import user_config_dir

class Config:
    DEBUG = True
    CORS_ORIGINS = ["http://localhost:5173"]

    # Gère le dossier static selon le mode (développement vs PyInstaller)
    if getattr(sys, 'frozen', False):
        STATIC_FOLDER = os.path.join(sys._MEIPASS, 'frontend', 'build')
    else:
        STATIC_FOLDER = os.path.join(os.path.dirname(__file__), '../../frontend/build')

    APP_NAME = "PredictionRMN"
    APP_AUTHOR = "LERIA"

    @staticmethod
    def get_user_settings_dir():
        return user_config_dir(Config.APP_NAME, Config.APP_AUTHOR)

    @staticmethod
    def get_settings_file_path(filename):
        settings_dir = Config.get_user_settings_dir()
        os.makedirs(settings_dir, exist_ok=True)
        return os.path.join(settings_dir, filename)
