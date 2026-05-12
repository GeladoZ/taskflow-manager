# src/routes/tasks.py
# Rotas da API para gerenciamento de tarefas (CRUD completo)
# Implementa as operações: Create, Read, Update, Delete

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Task, TaskPriority, TaskStatus

# Blueprint para organizar as rotas de tarefas
tasks_bp = Blueprint("tasks", __name__)

# Valores válidos para prioridade e status
VALID_PRIORITIES = {p.value for p in TaskPriority}
VALID_STATUSES = {s.value for s in TaskStatus}


@tasks_bp.route("/", methods=["POST"])
@jwt_required()
def create_task():
    """
    [C] CREATE — Cria uma nova tarefa.
    Requer: title (obrigatório), description, priority, status, due_date
    Retorna: tarefa criada com status 201
    """
    data = request.get_json()
    user_id = get_jwt_identity()

    # Valida campo obrigatório
    if not data or not data.get("title"):
        return jsonify({"error": "O campo 'title' é obrigatório"}), 400

    # Valida prioridade se fornecida
    priority_val = data.get("priority", "medium")
    if priority_val not in VALID_PRIORITIES:
        return jsonify({"error": f"Prioridade inválida. Use: {VALID_PRIORITIES}"}), 400

    # Cria a nova tarefa no banco de dados
    task = Task(
        title=data["title"],
        description=data.get("description", ""),
        priority=TaskPriority(priority_val),
        status=TaskStatus.TODO,
        user_id=user_id
    )
    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201


@tasks_bp.route("/", methods=["GET"])
@jwt_required()
def list_tasks():
    """
    [R] READ — Lista todas as tarefas do usuário autenticado.
    Suporta filtros via query string: ?priority=high&status=todo
    Retorna: lista de tarefas com status 200
    """
    user_id = get_jwt_identity()
    query = Task.query.filter_by(user_id=user_id)

    # Aplica filtro por prioridade se fornecido
    priority_filter = request.args.get("priority")
    if priority_filter:
        if priority_filter not in VALID_PRIORITIES:
            return jsonify({"error": "Prioridade inválida para filtro"}), 400
        query = query.filter_by(priority=TaskPriority(priority_filter))

    # Aplica filtro por status se fornecido
    status_filter = request.args.get("status")
    if status_filter:
        if status_filter not in VALID_STATUSES:
            return jsonify({"error": "Status inválido para filtro"}), 400
        query = query.filter_by(status=TaskStatus(status_filter))

    tasks = query.order_by(Task.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tasks]), 200


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    """
    [U] UPDATE — Atualiza uma tarefa existente.
    Permite atualizar: title, description, priority, status, due_date
    Retorna: tarefa atualizada com status 200
    """
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404

    data = request.get_json()

    # Atualiza apenas os campos fornecidos na requisição
    if "title" in data:
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]
    if "priority" in data:
        if data["priority"] not in VALID_PRIORITIES:
            return jsonify({"error": f"Prioridade inválida. Use: {VALID_PRIORITIES}"}), 400
        task.priority = TaskPriority(data["priority"])
    if "status" in data:
        if data["status"] not in VALID_STATUSES:
            return jsonify({"error": f"Status inválido. Use: {VALID_STATUSES}"}), 400
        task.status = TaskStatus(data["status"])

    db.session.commit()
    return jsonify(task.to_dict()), 200


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    """
    [D] DELETE — Remove uma tarefa permanentemente.
    Retorna: mensagem de sucesso com status 200, ou 404 se não encontrada
    """
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": f"Tarefa '{task.title}' removida com sucesso"}), 200
