from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.employee import employee_bp
    from app.routes.technician import technician_bp
    from app.routes.category import category_bp
    from app.routes.ticket import ticket_bp
    from app.routes.report import report_bp
    from app.routes.user import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(technician_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(ticket_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(user_bp)

    return app
