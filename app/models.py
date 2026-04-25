# MODELOS (Models)
# Em uma arquitetura MVC (Model-View-Controller):
#   - Model  → define a estrutura dos dados (este arquivo)
#   - View   → os templates HTML em /templates/
#   - Controller → as rotas em routes.py
#
# Quando o projeto crescer, instale o SQLAlchemy:
#   pip install flask-sqlalchemy
#
# Depois inicialize assim em __init__.py:
#   from flask_sqlalchemy import SQLAlchemy
#   db = SQLAlchemy()
#   db.init_app(app)
#
# Exemplo de modelo para persistir tarefas no banco SQLite:
#
# class Tarefa(db.Model):
#     # Chave primária — identificador único de cada registro
#     id = db.Column(db.Integer, primary_key=True)
#
#     # Campo de texto com limite de 200 caracteres, obrigatório
#     descricao = db.Column(db.String(200), nullable=False)
#
#     # Campo booleano com valor padrão False
#     concluida = db.Column(db.Boolean, default=False)
#
#     # Representação legível do objeto (útil no terminal/debug)
#     def __repr__(self):
#         return f"<Tarefa {self.id}: {self.descricao}>"
