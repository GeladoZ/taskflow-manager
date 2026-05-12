# src/config.py
# Configurações da aplicação TaskFlow Manager
# Separa configurações por ambiente (desenvolvimento, teste, produção)

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuração base da aplicação."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///taskflow.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # Token expira em 1 hora
