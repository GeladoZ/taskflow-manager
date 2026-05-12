# tests/test_reports.py
# Testes para o módulo de exportação de relatórios — MUDANÇA DE ESCOPO
# Cobre o teste T08 descrito na documentação teórica

import pytest


class TestReportExport:
    """Testes para o endpoint de exportação de relatórios (T08)."""

    def test_export_csv_report(self, client, auth_headers):
        """
        T08 — Verifica que a exportação CSV gera um arquivo com os
        cabeçalhos corretos e dados das tarefas do usuário.
        Funcionalidade adicionada na mudança de escopo da Sprint 2.
        """
        # Cria algumas tarefas para serem exportadas
        client.post("/api/tasks/", json={"title": "Tarefa Exportada 1", "priority": "high"}, headers=auth_headers)
        client.post("/api/tasks/", json={"title": "Tarefa Exportada 2", "priority": "low"}, headers=auth_headers)

        # Solicita a exportação em CSV
        response = client.get("/api/reports/export", headers=auth_headers)

        assert response.status_code == 200
        # Verifica o tipo de conteúdo da resposta
        assert "text/csv" in response.content_type
        # Verifica que o arquivo tem nome para download
        assert "taskflow_report.csv" in response.headers.get("Content-Disposition", "")

        # Decodifica o conteúdo e verifica os cabeçalhos do CSV
        content = response.data.decode("utf-8")
        lines = content.strip().split("\n")

        # Verifica que o cabeçalho contém as colunas esperadas
        header = lines[0]
        assert "ID" in header
        assert "Título" in header or "Titulo" in header
        assert "Prioridade" in header
        assert "Status" in header

        # Verifica que as duas tarefas criadas estão no CSV
        assert len(lines) >= 3  # cabeçalho + 2 tarefas

    def test_export_csv_requires_auth(self, client):
        """
        Verifica que a exportação sem autenticação retorna erro 401.
        """
        response = client.get("/api/reports/export")
        assert response.status_code == 401

    def test_export_csv_empty(self, client, auth_headers):
        """
        Verifica que a exportação sem tarefas retorna apenas o cabeçalho.
        """
        response = client.get("/api/reports/export", headers=auth_headers)

        assert response.status_code == 200
        content = response.data.decode("utf-8")
        lines = [l for l in content.strip().split("\n") if l]
        # Apenas o cabeçalho, sem linhas de dados
        assert len(lines) == 1
