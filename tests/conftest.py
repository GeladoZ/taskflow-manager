# tests/conftest.py
# Fixtures compartilhadas entre todos os testes do PyTest
# Configura banco de dados de teste isolado e cliente HTTP para requisições

import pytest
from src.app import create_app, db
from src.models import User, UserRole


class TestConfig:
    """Configuração específica para o ambiente de testes."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Banco em memória, sem arquivos
    JWT_SECRET_KEY = "test-secret-key-for-pytest"
    WTF_CSRF_ENABLED = False


@pytest.fixture(scope="function")
def app():
    """
    Cria uma instância da aplicação para cada teste.
    Usa banco de dados SQLite em memória para isolamento total.
    """
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de teste
        yield app
        db.session.remove()
        db.drop_all()  # Limpa o banco após cada teste


@pytest.fixture(scope="function")
def client(app):
    """Retorna o cliente de teste do Flask para fazer requisições HTTP."""
    return app.test_client()


@pytest.fixture(scope="function")
def test_user(app):
    """Cria e persiste um usuário de teste no banco de dados."""
    with app.app_context():
        user = User(name="Usuário Teste", email="teste@taskflow.com")
        user.set_password("senha123")
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture(scope="function")
def admin_user(app):
    """Cria e persiste um usuário administrador para testes de relatório."""
    with app.app_context():
        admin = User(name="Admin Teste", email="admin@taskflow.com", role=UserRole.ADMIN)
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        return admin


@pytest.fixture(scope="function")
def auth_headers(client, test_user):
    """
    Realiza login e retorna os headers de autenticação JWT.
    Usado em todos os testes que precisam de autenticação.
    """
    response = client.post("/api/auth/login", json={
        "email": "teste@taskflow.com",
        "password": "senha123"
    })
    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
