# tests/test_auth.py
# Testes automatizados para o módulo de autenticação
# Cobre os testes T05 e T06 descritos na documentação teórica

import pytest


class TestLogin:
    """Testes para o endpoint de autenticação (T05, T06)."""

    def test_login_valid_user(self, client, test_user):
        """
        T05 — Verifica que o login com credenciais válidas retorna
        um token JWT de acesso no corpo da resposta.
        """
        response = client.post("/api/auth/login", json={
            "email": "teste@taskflow.com",
            "password": "senha123"
        })

        assert response.status_code == 200
        body = response.get_json()
        assert "access_token" in body  # Token JWT deve estar presente
        assert "user" in body          # Dados do usuário também retornados
        assert body["user"]["email"] == "teste@taskflow.com"

    def test_login_invalid_password(self, client, test_user):
        """
        T06 — Verifica que o login com senha incorreta retorna erro 401
        sem revelar qual campo está errado (segurança).
        """
        response = client.post("/api/auth/login", json={
            "email": "teste@taskflow.com",
            "password": "senha_errada"
        })

        assert response.status_code == 401
        body = response.get_json()
        assert "error" in body

    def test_login_nonexistent_email(self, client):
        """
        Verifica que o login com e-mail não cadastrado retorna erro 401.
        """
        response = client.post("/api/auth/login", json={
            "email": "naoexiste@taskflow.com",
            "password": "qualquersenha"
        })

        assert response.status_code == 401

    def test_login_missing_fields(self, client):
        """
        Verifica que o login sem campos obrigatórios retorna erro 400.
        """
        response = client.post("/api/auth/login", json={"email": "apenas@email.com"})
        assert response.status_code == 400


class TestRegister:
    """Testes para o endpoint de cadastro."""

    def test_register_valid_user(self, client):
        """
        Verifica que o cadastro com dados válidos cria o usuário e retorna 201.
        """
        response = client.post("/api/auth/register", json={
            "name": "Novo Usuário",
            "email": "novo@taskflow.com",
            "password": "senha456"
        })

        assert response.status_code == 201
        body = response.get_json()
        assert body["email"] == "novo@taskflow.com"
        assert "password_hash" not in body  # Senha nunca é retornada

    def test_register_duplicate_email(self, client, test_user):
        """
        Verifica que o cadastro com e-mail duplicado retorna erro 409.
        """
        response = client.post("/api/auth/register", json={
            "name": "Outro Usuário",
            "email": "teste@taskflow.com",  # E-mail já usado pelo test_user
            "password": "outrasenha"
        })

        assert response.status_code == 409
