# 📋 TaskFlow Manager

![CI](https://github.com/seu-usuario/taskflow-manager/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

> Sistema de Gerenciamento de Tarefas baseado em metodologias ágeis — desenvolvido para a TechFlow Solutions.

---

## 🎯 Objetivo do Projeto

O **TaskFlow Manager** é um sistema web de gerenciamento de tarefas desenvolvido para uma startup de logística. Permite acompanhar o fluxo de trabalho em tempo real, priorizar tarefas críticas e monitorar o desempenho da equipe.

---

## 📐 Escopo Inicial

O sistema foi planejado com as seguintes funcionalidades:

| Módulo | Funcionalidade | Prioridade |
|--------|---------------|-----------|
| Autenticação | Login e cadastro com JWT | Alta |
| Tarefas | CRUD completo (Create, Read, Update, Delete) | Alta |
| Priorização | Classificação por urgência (Alta/Média/Baixa) | Alta |
| Status | Controle de status (To Do / In Progress / Done) | Alta |
| Interface | Dashboard web responsivo | Média |

---

## 🔄 Metodologia Adotada

Utilizamos uma abordagem **híbrida Scrum + Kanban**:

- **Scrum**: Sprints semanais com planejamento e revisão
- **Kanban**: Quadro visual no GitHub Projects com colunas *To Do*, *In Progress* e *Done*
- **CI/CD**: Integração contínua via GitHub Actions com testes automatizados (PyTest)
- **Commits semânticos**: Padrão Conventional Commits para rastreabilidade

---

## 📝 Mudança de Escopo

> **Mudança realizada na Sprint 2 — Módulo de Exportação de Relatórios**

**Justificativa:** O cliente (startup de logística) solicitou a inclusão de um módulo de exportação de relatórios em CSV para apresentar dados de produtividade semanal aos investidores. Essa funcionalidade não estava prevista no escopo inicial.

**Impacto:** Sprint estendida de 5 para 8 dias. Adição de 2 novos cards no Kanban e da classe `Report` no sistema.

**Ações tomadas:**
- Criação de card `#10: Implementar exportação CSV` no Kanban
- Implementação da rota `GET /api/reports/export`
- Adição de teste automatizado `test_export_csv_report` (T08)
- Atualização deste README.md

---

## 🚀 Como Executar o Sistema

### Pré-requisitos
- Python 3.11+
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/taskflow-manager.git
cd taskflow-manager

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env

# Execute a aplicação
python src/app.py
```

A aplicação estará disponível em `http://localhost:5000`

### Executar os Testes

```bash
# Todos os testes com verbose
pytest tests/ -v

# Com relatório de cobertura
pytest tests/ --cov=src --cov-report=html
```

---

## 📁 Estrutura do Repositório

```
taskflow-manager/
├── src/                    # Código-fonte principal
│   ├── app.py              # Fábrica da aplicação Flask
│   ├── models.py           # Modelos de dados (User, Task, Report)
│   ├── routes/
│   │   ├── auth.py         # Rotas de autenticação
│   │   ├── tasks.py        # Rotas de tarefas (CRUD)
│   │   └── reports.py      # Rotas de relatórios (mudança de escopo)
│   └── config.py           # Configurações da aplicação
├── tests/                  # Testes automatizados (PyTest)
│   ├── conftest.py         # Fixtures compartilhadas
│   ├── test_tasks.py       # Testes do módulo de tarefas
│   ├── test_auth.py        # Testes de autenticação
│   └── test_reports.py     # Testes de relatórios
├── docs/                   # Documentação do projeto
│   └── parte_teorica.pdf   # Documento teórico completo
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline de CI/CD (GitHub Actions)
├── requirements.txt        # Dependências Python
├── .env.example            # Exemplo de variáveis de ambiente
└── README.md               # Este arquivo
```

---

## 🧪 Testes Automatizados

| Teste | O que valida | Status |
|-------|-------------|--------|
| T01 - test_create_task_valid | Criação de tarefa válida retorna 201 | ✅ PASS |
| T02 - test_create_task_missing_title | Título obrigatório retorna erro 400 | ✅ PASS |
| T03 - test_update_task_status | Status aceita apenas valores válidos | ✅ PASS |
| T04 - test_delete_task_not_found | Tarefa inexistente retorna 404 | ✅ PASS |
| T05 - test_login_valid_user | Login válido retorna token JWT | ✅ PASS |
| T06 - test_login_invalid_password | Senha errada retorna 401 | ✅ PASS |
| T07 - test_filter_by_priority | Filtro por prioridade funciona corretamente | ✅ PASS |
| T08 - test_export_csv_report | Exportação CSV com cabeçalhos corretos | ✅ PASS |

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feat/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: add nova funcionalidade'`)
4. Push para a branch (`git push origin feat/nova-funcionalidade`)
5. Abra um Pull Request

---

## 📚 Referências

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Flask Documentation](https://flask.palletsprojects.com)
- [PyTest Documentation](https://docs.pytest.org)
- Pressman, R. S. — *Engenharia de Software: Uma Abordagem Profissional*
