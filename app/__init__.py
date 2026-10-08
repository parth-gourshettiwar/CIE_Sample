from flask import Flask
from .metrics import setup_metrics

def create_app():
    app = Flask(__name__)
    
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    setup_metrics(app)
    
    return app
