from flask import Flask
from config import ApplicationConfig
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_session import Session
import os

bcrypt = Bcrypt()
server_session = Session()

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.config.from_object(ApplicationConfig)
    
    bcrypt.init_app(app)
    server_session.init_app(app)
    
    from routes.api import api_bp
    from routes.auth import auth_bp
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    return app


if __name__ == '__main__':
    HOST = os.environ.get('BACKEND_HOST', '0.0.0.0')
    PORT = int(os.environ.get('BACKEND_PORT', 5000))
    DEBUG = os.environ.get('DEBUG', 'True').lower() in ('1', 'true', 'yes')

    app = create_app()
    app.run(host=HOST, port=PORT, debug=DEBUG)
