import os
import sys
import platform

class Config:
    DEBUG = True
    CORS_ORIGINS = ["http://localhost:5173"]

    # Gère le dossier static selon le mode (développement vs PyInstaller)
    if getattr(sys, 'frozen', False):
        STATIC_FOLDER = os.path.join(sys._MEIPASS, 'frontend', 'build')
    else:
        STATIC_FOLDER = os.path.join(os.path.dirname(__file__), '../../frontend/build')

    # Nom de l'application (utilisé pour les dossiers de config)
    APP_NAME = "PredictionRMN"

    @staticmethod
    def get_user_settings_dir():
        system = platform.system()
        if system == "Windows":
            return os.path.join(os.getenv('APPDATA'), Config.APP_NAME)
        elif system == "Darwin":  # macOS
            return os.path.join(os.path.expanduser('~/Library/Application Support/'), Config.APP_NAME)
        else:  # Linux and autres
            return os.path.join(os.path.expanduser('~/.config/'), Config.APP_NAME)

    @staticmethod
    def get_settings_file_path(filename="settings.json"):
        settings_dir = Config.get_user_settings_dir()
        os.makedirs(settings_dir, exist_ok=True)
        return os.path.join(settings_dir, filename)
