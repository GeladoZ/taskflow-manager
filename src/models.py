# src/models.py
# Modelos de dados da aplicação TaskFlow Manager
# Define as classes User, Task e Report com seus atributos e relacionamentos

from datetime import datetime
from enum import Enum as PyEnum
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class UserRole(PyEnum):
    """Papéis possíveis para um usuário no sistema."""
    ADMIN = "admin"
    MEMBER = "member"


class TaskPriority(PyEnum):
    """Níveis de prioridade para tarefas."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskStatus(PyEnum):
    """Status possíveis para uma tarefa no quadro Kanban."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class User(db.Model):
    """
    Modelo de Usuário.
    Representa um membro da equipe ou administrador do sistema.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.MEMBER, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento: um usuário pode ter muitas tarefas
    tasks = db.relationship("Task", backref="owner", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        """Gera e armazena o hash da senha."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        """Serializa o usuário para dicionário (sem dados sensíveis)."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role.value,
            "created_at": self.created_at.isoformat()
        }


class Task(db.Model):
    """
    Modelo de Tarefa.
    Representa uma tarefa no sistema de gerenciamento Kanban.
    """
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Chave estrangeira: referência ao usuário responsável pela tarefa
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def to_dict(self) -> dict:
        """Serializa a tarefa para dicionário."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "status": self.status.value,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class Report(db.Model):
    """
    Modelo de Relatório — adicionado na mudança de escopo (Sprint 2).
    Representa um relatório gerado pelo administrador para exportação de dados.
    """
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)
    format = db.Column(db.String(10), nullable=False, default="csv")  # csv ou pdf
    generated_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        """Serializa o relatório para dicionário."""
        return {
            "id": self.id,
            "format": self.format,
            "generated_by": self.generated_by,
            "created_at": self.created_at.isoformat()
        }
