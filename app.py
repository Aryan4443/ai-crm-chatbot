"""
Main Flask Application for CRM Chatbot
"""

from flask import Flask
from flask_cors import CORS
from app.api.auth import init_auth
from app.api.routes import api_bp
import os
import json

# Load configuration
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', config['security']['jwt_secret_key'])

# Enable CORS
CORS(app)

# Initialize authentication
jwt = init_auth(app)

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api/v1')

# Create necessary directories
os.makedirs('logs', exist_ok=True)
os.makedirs('models', exist_ok=True)
os.makedirs('data', exist_ok=True)


@app.route('/')
def index():
    """Root endpoint"""
    return {
        'message': 'CRM Chatbot API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/v1/health',
            'login': '/api/v1/auth/login',
            'chat': '/api/v1/chat',
            'analytics': '/api/v1/analytics'
        }
    }


if __name__ == '__main__':
    host = config['api']['host']
    port = config['api']['port']
    debug = config['api']['debug']
    
    print(f"Starting CRM Chatbot API on {host}:{port}")
    print(f"Debug mode: {debug}")
    
    app.run(host=host, port=port, debug=debug)

