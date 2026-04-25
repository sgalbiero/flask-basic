# Flask Educacional — Template Base

Template de estudo com Flask explicado linha a linha. Cobre estrutura de projeto, rotas, Jinja2, flash messages e boas práticas.

---

## Sumário

1. [Stack](#stack)
2. [Estrutura do projeto](#estrutura-do-projeto)
3. [Como rodar](#como-rodar)
4. [Conceitos cobertos](#conceitos-cobertos)
   - [Application Factory](#application-factory)
   - [Blueprints](#blueprints)
   - [Rotas e métodos HTTP](#rotas-e-métodos-http)
   - [Parâmetros dinâmicos na URL](#parâmetros-dinâmicos-na-url)
   - [PRG Pattern](#prg-pattern)
   - [Flash Messages](#flash-messages)
   - [Jinja2 — Herança de templates](#jinja2--herança-de-templates)
   - [Jinja2 — Sintaxe rápida](#jinja2--sintaxe-rápida)
   - [Comentários em templates](#comentários-em-templates)
   - [SECRET_KEY](#secret_key)
5. [Rotas disponíveis](#rotas-disponíveis)
6. [Como escalar para produção](#como-escalar-para-produção)

---

## Stack

| Camada     | Tecnologia                        |
|------------|-----------------------------------|
| Backend    | Python 3 + Flask 3                |
| Templates  | Jinja2 (incluído no Flask)        |
| Estilo     | CSS puro                          |
| Banco      | Em memória (lista Python) — pronto para migrar para SQLite/SQLAlchemy |

---

## Estrutura do projeto

```
flask-basic/
│
├── app/
│   ├── __init__.py   ← Application Factory (create_app)
│   ├── routes.py     ← Rotas organizadas em Blueprint
│   └── models.py     ← Placeholder para modelos de banco de dados
│
├── templates/
│   ├── base.html     ← Layout base com herança Jinja2
│   └── index.html    ← Página principal (estende base.html)
│
├── static/
│   └── style.css     ← Estilos da aplicação
│
├── config.py         ← Configurações centralizadas (SECRET_KEY, DB URI, etc.)
├── run.py            ← Ponto de entrada: python run.py
├── requirements.txt  ← Dependências do projeto
└── README.md
```

---

## Como rodar

**1. Clone e entre na pasta**
```bash
git clone <url-do-repo>
cd flask-basic
```

**2. Crie e ative a virtual environment**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

> Uma virtual environment isola as dependências do projeto do Python global da máquina.

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Rode o servidor**
```bash
python run.py
```

**5. Acesse no navegador**
```
http://127.0.0.1:5000
```

---

## Conceitos cobertos

### Application Factory

Em vez de criar `app = Flask(__name__)` diretamente no módulo, usamos uma função `create_app()`:

```python
# app/__init__.py
def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    from .routes import main
    app.register_blueprint(main)
    return app
```

**Por quê?**
- Permite criar múltiplas instâncias (útil em testes)
- Evita importações circulares
- Facilita trocar configurações por ambiente (dev, test, prod)

---

### Blueprints

Um Blueprint agrupa rotas relacionadas em um módulo independente:

```python
# app/routes.py
from flask import Blueprint
main = Blueprint("main", __name__)

@main.route("/")
def index():
    ...
```

Registrado no app em `create_app()`:
```python
app.register_blueprint(main)
```

Em projetos maiores, você teria múltiplos blueprints:
```
blueprints/
├── auth/routes.py    ← Blueprint "auth"  (/login, /logout)
├── api/routes.py     ← Blueprint "api"   (/api/users)
└── admin/routes.py   ← Blueprint "admin" (/admin/dashboard)
```

---

### Rotas e métodos HTTP

```python
@main.route("/")                          # GET (padrão)
@main.route("/add", methods=["POST"])     # só POST
@main.route("/delete/<int:id>", methods=["POST"])  # POST com parâmetro
```

| Método | Uso típico           |
|--------|----------------------|
| GET    | Buscar / exibir dados |
| POST   | Enviar / criar dados  |
| PUT    | Substituir um recurso |
| PATCH  | Atualizar parcialmente |
| DELETE | Remover um recurso    |

> HTML nativo só suporta GET e POST em `<form>`. Para usar PUT/DELETE em formulários, é preciso JavaScript ou uma biblioteca como Flask-WTF.

---

### Parâmetros dinâmicos na URL

```python
@main.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    # index é convertido para int automaticamente
    tarefas.pop(index)
```

Conversores disponíveis: `string` (padrão), `int`, `float`, `path`, `uuid`.

---

### PRG Pattern

**P**ost / **R**edirect / **G**et — evita que recarregar a página reenvie o formulário:

```
Navegador → POST /add → servidor processa → redirect → GET / → renderiza página
```

```python
@main.route("/add", methods=["POST"])
def add():
    tarefas.append(request.form.get("tarefa"))
    return redirect(url_for("main.index"))  # ← PRG: redireciona após POST
```

Sem isso, apertar F5 após enviar um formulário re-enviaria os dados.

---

### Flash Messages

Mensagens de feedback de uma única exibição — desaparecem após serem lidas:

```python
# Em routes.py (escreve a mensagem)
flash("Tarefa adicionada!", "sucesso")

# Em base.html (lê e exibe)
{% with mensagens = get_flashed_messages(with_categories=True) %}
    {% for categoria, mensagem in mensagens %}
        <div class="flash flash-{{ categoria }}">{{ mensagem }}</div>
    {% endfor %}
{% endwith %}
```

Categorias usadas neste projeto: `sucesso`, `erro`, `aviso`.
Flash depende da `SECRET_KEY` para assinar o cookie de sessão.

---

### Jinja2 — Herança de templates

```
base.html          ← define o layout completo com {% block content %}
  └── index.html   ← {% extends "base.html" %} + preenche {% block content %}
```

`base.html` define blocos que as páginas filhas podem sobrescrever:
```html
<title>{% block title %}Padrão{% endblock %}</title>
```

`index.html` sobrescreve:
```html
{% extends "base.html" %}
{% block title %}Minha Página{% endblock %}
```

---

### Jinja2 — Sintaxe rápida

| Sintaxe | Descrição |
|---------|-----------|
| `{{ variavel }}` | Exibe valor (HTML escapado automaticamente — proteção XSS) |
| `{{ variavel \| upper }}` | Aplica filtro (`upper`, `lower`, `length`, `default`, `join`...) |
| `{% if condicao %}` | Condicional |
| `{% elif / else / endif %}` | Complementos do if |
| `{% for item in lista %}` | Loop |
| `loop.index` / `loop.index0` | Posição no loop (1-based / 0-based) |
| `loop.first` / `loop.last` | Primeiro/último item |
| `{% block nome %}` | Define área sobrescritível |
| `{% extends "base.html" %}` | Herda layout |
| `{% include "partial.html" %}` | Inclui fragmento reutilizável |
| `{% raw %} ... {% endraw %}` | Exibe sintaxe Jinja2 como texto literal |
| `{# comentário #}` | Comentário (não aparece no HTML final) |

---

### Comentários em templates

**Regra importante:** o Jinja2 processa `{% %}` e `{{ }}` em qualquer lugar do template, inclusive dentro de comentários HTML `<!-- -->`.

```html
<!-- ERRADO: Jinja2 processa isso e pode causar TemplateSyntaxError -->
<!-- use {% block content %} para preencher -->

{# CERTO: use comentário Jinja2 quando o texto contém sintaxe Jinja2 #}
{# use "block content" para preencher #}
```

Use `<!-- -->` para comentários de HTML puro.
Use `{# #}` quando o conteúdo descreve ou contém sintaxe Jinja2.

---

### SECRET_KEY

Usada pelo Flask para assinar criptograficamente cookies de sessão e flash messages:

```python
# config.py — desenvolvimento
import secrets
SECRET_KEY = secrets.token_hex(32)

# config.py — produção (use variável de ambiente)
import os
SECRET_KEY = os.environ.get("SECRET_KEY")
```

> Em produção, **nunca** deixe a SECRET_KEY hardcoded no código. Use variáveis de ambiente (`.env` com `python-dotenv` ou configuração do servidor).

---

## Rotas disponíveis

| Método | URL | Descrição |
|--------|-----|-----------|
| GET | `/` | Lista todas as tarefas |
| POST | `/add` | Adiciona nova tarefa |
| POST | `/delete/<index>` | Remove tarefa pelo índice |
| POST | `/clear` | Remove todas as tarefas |

---

## Como escalar para produção

**1. Adicionar banco de dados (SQLite → PostgreSQL)**
```bash
pip install flask-sqlalchemy
```
Ver `app/models.py` para exemplo de modelo.

**2. Separar configurações por ambiente**
```python
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
```

**3. Usar servidor WSGI em vez do servidor de desenvolvimento**
```bash
pip install gunicorn
gunicorn "app:create_app()"
```

**4. Variáveis de ambiente com python-dotenv**
```bash
pip install python-dotenv
```
Crie um `.env` (nunca commite no git):
```
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=sqlite:///tarefas.db
```
