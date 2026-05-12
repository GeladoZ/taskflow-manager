# src/routes/auth.py
# Rotas de autenticação — Login e cadastro de usuários
# Utiliza JWT (JSON Web Token) para autenticação stateless

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app import db
from models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Cadastra um novo usuário no sistema.
    Requer: name, email, password
    Retorna: dados do usuário criado com status 201
    """
    data = request.get_json()

    # Valida campos obrigatórios
    required = ["name", "email", "password"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Campos obrigatórios: {missing}"}), 400

    # Verifica se o e-mail já está em uso
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "E-mail já cadastrado"}), 409

    # Cria o usuário com senha hasheada (nunca armazenamos senha em texto puro)
    user = User(name=data["name"], email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Autentica um usuário e retorna um token JWT.
    Requer: email, password
    Retorna: access_token JWT com status 200, ou erro 401
    """
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "E-mail e senha são obrigatórios"}), 400

    # Busca o usuário pelo e-mail
    user = User.query.filter_by(email=data["email"]).first()

    # Verifica credenciais (sem revelar qual campo está errado — segurança)
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Credenciais inválidas"}), 401

    # Gera o token JWT com o ID do usuário como identity
    access_token = create_access_token(identity=user.id)
    return jsonify({
        "access_token": access_token,
        "user": user.to_dict()
    }), 200
