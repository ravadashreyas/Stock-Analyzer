from flask import Flask
from routes.api import api_bp
from flask_cors import CORS
import os


def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.register_blueprint(api_bp, url_prefix='/api')
    return app


if __name__ == '__main__':
    HOST = os.environ.get('BACKEND_HOST', '0.0.0.0')
    PORT = int(os.environ.get('BACKEND_PORT', 5000))
    DEBUG = os.environ.get('DEBUG', 'True').lower() in ('1', 'true', 'yes')

    app = create_app()
    app.run(host=HOST, port=PORT, debug=DEBUG)
