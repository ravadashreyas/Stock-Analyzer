from flask import Flask
from routes.api import api_bp
from routes.frontend import frontend_bp

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(frontend_bp)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
