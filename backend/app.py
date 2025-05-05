from app import create_app

# Créer l'application Flask
app = create_app()

# Si le fichier est exécuté directement, démarrer le serveur
if __name__ == '__main__':
    app.run(debug=True)
