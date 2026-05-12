# src/routes/reports.py
# Módulo de Exportação de Relatórios — MUDANÇA DE ESCOPO (Sprint 2)
# Adicionado a pedido do cliente para exportação de dados de produtividade
# Suporta exportação em formato CSV

import csv
import io
from flask import Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Task, Report, User, UserRole
from app import db

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/export", methods=["GET"])
@jwt_required()
def export_csv():
    """
    Exporta todas as tarefas do usuário em formato CSV.
    Rota adicionada na mudança de escopo da Sprint 2.
    Retorna: arquivo CSV para download com todas as tarefas do usuário
    """
    user_id = get_jwt_identity()

    # Busca todas as tarefas do usuário autenticado
    tasks = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()

    # Cria o arquivo CSV em memória (sem salvar em disco)
    output = io.StringIO()
    writer = csv.writer(output)

    # Cabeçalho do CSV com nomes descritivos das colunas
    writer.writerow(["ID", "Título", "Descrição", "Prioridade", "Status", "Prazo", "Criado em"])

    # Dados das tarefas
    for task in tasks:
        writer.writerow([
            task.id,
            task.title,
            task.description or "",
            task.priority.value,
            task.status.value,
            task.due_date.isoformat() if task.due_date else "",
            task.created_at.isoformat()
        ])

    # Registra o relatório no banco de dados para auditoria
    report = Report(format="csv", generated_by=user_id)
    db.session.add(report)
    db.session.commit()

    # Retorna o CSV como resposta HTTP com headers de download
    response = make_response(output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = "attachment; filename=taskflow_report.csv"
    return response
