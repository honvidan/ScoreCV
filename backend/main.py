from flask import Flask
from flask_cors import CORS
from routes.matching import matching_bp
from core.nlp import setup_nltk
import os

def create_app():
    """Create and configure the Flask application."""
    # Setup NLTK data
    setup_nltk()
    
    app = Flask(__name__)
    
    # Enable CORS for frontend
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(matching_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
