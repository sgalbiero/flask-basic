# Flask é o micro-framework web que usamos para criar o servidor.
from flask import Flask


# PADRÃO: Application Factory
# Em vez de criar o app diretamente no módulo (app = Flask(...)),
# usamos uma função create_app(). Isso permite:
#   - Criar múltiplas instâncias do app (útil para testes)
#   - Configurar o app antes de registrar extensões
#   - Evitar importações circulares
def create_app():
    # __name__ diz ao Flask qual é o pacote raiz do projeto,
    # para que ele saiba onde encontrar templates e arquivos estáticos.
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    # Carrega as configurações da classe Config em config.py.
    # Usando uma string ("config.Config") o Flask importa o módulo dinamicamente.
    app.config.from_object("config.Config")

    # BLUEPRINT: um Blueprint é um conjunto de rotas agrupadas.
    # Permite dividir o app em módulos independentes.
    # Importamos aqui (dentro da função) para evitar importação circular.
    from .routes import main
    app.register_blueprint(main)

    # Retorna o app configurado para ser usado em run.py
    return app
