# src/app.py
# Arquivo principal da aplicação TaskFlow Manager
# Utiliza o padrão Application Factory do Flask para melhor testabilidade

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config

# Inicializa as extensões sem vinculá-las à app (padrão factory)
db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_class=Config):
    """
    Fábrica de aplicação Flask.
    Permite criar instâncias separadas para produção e testes.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa extensões com a aplicação
    db.init_app(app)
    jwt.init_app(app)

    # Registra os blueprints (módulos de rotas)
    from routes.auth import auth_bp
    from routes.tasks import tasks_bp
    from routes.reports import reports_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    app.register_blueprint(reports_bp, url_prefix="/api/reports")

    # Cria as tabelas no banco de dados se não existirem
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
