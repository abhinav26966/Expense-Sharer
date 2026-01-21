"""
Application factory for Daily Expense Sharing Application.
Uses the factory pattern for flexible configuration.
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app(config_name=None):
    """
    Application factory function.
    
    Args:
        config_name: Configuration to use ('development', 'testing', 'production')
                    Defaults to FLASK_ENV environment variable or 'development'
    
    Returns:
        Configured Flask application instance
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))

    db.init_app(app)

    with app.app_context():
        from app import routes
        app.register_blueprint(routes.bp)
        db.create_all()

    return app
