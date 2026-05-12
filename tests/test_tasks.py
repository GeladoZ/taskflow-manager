# tests/test_tasks.py
# Testes automatizados para o módulo de tarefas (CRUD)
# Cobre os testes T01 a T04 descritos na documentação teórica

import pytest


class TestCreateTask:
    """Testes para a operação de criação de tarefa (T01, T02)."""

    def test_create_task_valid(self, client, auth_headers):
        """
        T01 — Verifica que a criação de tarefa com dados válidos retorna status 201
        e os dados da tarefa criada no corpo da resposta.
        """
        data = {
            "title": "Implementar módulo de autenticação",
            "description": "Criar endpoints de login e registro",
            "priority": "high"
        }
        response = client.post("/api/tasks/", json=data, headers=auth_headers)

        assert response.status_code == 201
        body = response.get_json()
        assert body["title"] == "Implementar módulo de autenticação"
        assert body["priority"] == "high"
        assert body["status"] == "todo"  # Status inicial sempre é 'todo'

    def test_create_task_missing_title(self, client, auth_headers):
        """
        T02 — Verifica que a tentativa de criar uma tarefa sem título
        retorna erro 400 com mensagem descritiva.
        """
        data = {"description": "Sem título, deve falhar", "priority": "medium"}
        response = client.post("/api/tasks/", json=data, headers=auth_headers)

        assert response.status_code == 400
        body = response.get_json()
        assert "error" in body
        assert "title" in body["error"].lower()

    def test_create_task_invalid_priority(self, client, auth_headers):
        """
        Verifica que prioridade com valor inválido retorna erro 400.
        """
        data = {"title": "Tarefa teste", "priority": "urgentissimo"}
        response = client.post("/api/tasks/", json=data, headers=auth_headers)

        assert response.status_code == 400

    def test_create_task_requires_auth(self, client):
        """
        Verifica que a criação de tarefa sem token JWT retorna erro 401.
        """
        data = {"title": "Sem autenticação"}
        response = client.post("/api/tasks/", json=data)

        assert response.status_code == 401


class TestUpdateTask:
    """Testes para a operação de atualização de tarefa (T03)."""

    def test_update_task_status(self, client, auth_headers):
        """
        T03 — Verifica que a atualização do status de uma tarefa aceita apenas
        valores válidos (todo, in_progress, done).
        """
        # Primeiro cria uma tarefa
        create_resp = client.post("/api/tasks/", json={"title": "Tarefa para atualizar"}, headers=auth_headers)
        task_id = create_resp.get_json()["id"]

        # Atualiza o status para 'in_progress'
        update_resp = client.put(f"/api/tasks/{task_id}", json={"status": "in_progress"}, headers=auth_headers)
        assert update_resp.status_code == 200
        assert update_resp.get_json()["status"] == "in_progress"

    def test_update_task_invalid_status(self, client, auth_headers):
        """
        Verifica que status com valor inválido retorna erro 400.
        """
        create_resp = client.post("/api/tasks/", json={"title": "Tarefa teste"}, headers=auth_headers)
        task_id = create_resp.get_json()["id"]

        update_resp = client.put(f"/api/tasks/{task_id}", json={"status": "em_andamento"}, headers=auth_headers)
        assert update_resp.status_code == 400


class TestDeleteTask:
    """Testes para a operação de exclusão de tarefa (T04)."""

    def test_delete_task_not_found(self, client, auth_headers):
        """
        T04 — Verifica que a tentativa de excluir uma tarefa com ID inexistente
        retorna erro 404.
        """
        response = client.delete("/api/tasks/99999", headers=auth_headers)

        assert response.status_code == 404
        body = response.get_json()
        assert "error" in body

    def test_delete_task_success(self, client, auth_headers):
        """
        Verifica que a exclusão de uma tarefa existente retorna status 200.
        """
        # Cria uma tarefa para depois excluir
        create_resp = client.post("/api/tasks/", json={"title": "Tarefa a deletar"}, headers=auth_headers)
        task_id = create_resp.get_json()["id"]

        # Exclui a tarefa
        delete_resp = client.delete(f"/api/tasks/{task_id}", headers=auth_headers)
        assert delete_resp.status_code == 200

        # Confirma que a tarefa não existe mais
        get_resp = client.delete(f"/api/tasks/{task_id}", headers=auth_headers)
        assert get_resp.status_code == 404


class TestFilterTasks:
    """Testes para filtragem de tarefas (T07)."""

    def test_filter_by_priority(self, client, auth_headers):
        """
        T07 — Verifica que o filtro por prioridade retorna apenas as tarefas
        com a prioridade solicitada.
        """
        # Cria tarefas com prioridades diferentes
        client.post("/api/tasks/", json={"title": "Tarefa Alta 1", "priority": "high"}, headers=auth_headers)
        client.post("/api/tasks/", json={"title": "Tarefa Alta 2", "priority": "high"}, headers=auth_headers)
        client.post("/api/tasks/", json={"title": "Tarefa Baixa", "priority": "low"}, headers=auth_headers)

        # Filtra apenas as de alta prioridade
        response = client.get("/api/tasks/?priority=high", headers=auth_headers)

        assert response.status_code == 200
        tasks = response.get_json()
        # Todas as tarefas retornadas devem ter prioridade 'high'
        assert all(t["priority"] == "high" for t in tasks)
        assert len(tasks) == 2
