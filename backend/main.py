from flask import Flask
from routes.matching import matching_bp
from core.nlp import setup_nltk

def create_app():
    """Create and configure the Flask application."""
    # Setup NLTK data
    setup_nltk()
    
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(matching_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(port=5000)
