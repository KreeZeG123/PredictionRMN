from flask import Blueprint, send_from_directory, current_app
import os
import sys

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
@main_routes.route('/<path:path>')
def serve(path=""):
    static_folder = current_app.static_folder
    
    if path != "" and os.path.exists(os.path.join(static_folder, path)):
        return send_from_directory(static_folder, path)
    else:
        return send_from_directory(static_folder, 'index.html')
