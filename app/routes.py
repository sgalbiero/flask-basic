# ROTAS da aplicação
# Cada rota é uma URL que o navegador pode acessar.
# Flask mapeia URLs para funções Python usando decoradores (@).

# Importações do Flask:
#   Blueprint      → agrupador de rotas; permite modularizar o app
#   render_template → renderiza um arquivo HTML da pasta /templates/
#   request        → objeto com dados da requisição HTTP (form, args, etc.)
#   redirect       → redireciona o navegador para outra URL
#   url_for        → gera URLs dinamicamente a partir do nome da função
#   flash          → envia mensagens de feedback para o próximo request
from flask import Blueprint, render_template, request, redirect, url_for, flash

# Criamos um Blueprint chamado "main".
# O primeiro argumento é o nome do blueprint (usado em url_for).
# O segundo é o __name__ do módulo (para o Flask saber onde estão os templates).
main = Blueprint("main", __name__)

# ARMAZENAMENTO em memória (lista Python).
# Simples para aprender, mas os dados somem ao reiniciar o servidor.
# Em produção, use um banco de dados (SQLite, PostgreSQL, etc.).
tarefas = []


# ROTA GET "/"
# Responde quando o navegador acessa http://127.0.0.1:5000/
# methods=["GET"] é o padrão, então pode ser omitido.
@main.route("/")
def index():
    # render_template busca o arquivo em /templates/index.html
    # e passa a variável `tarefas` para o Jinja2 usar no HTML.
    return render_template("index.html", tarefas=tarefas)


# ROTA POST "/add"
# Só aceita POST (formulário enviando dados).
# GET nessa rota retornaria 405 Method Not Allowed.
@main.route("/add", methods=["POST"])
def add():
    # request.form é um dicionário com os campos do <form> HTML.
    # .get("tarefa") retorna None se o campo não existir (seguro).
    tarefa = request.form.get("tarefa", "").strip()

    if tarefa:
        tarefas.append(tarefa)
        # flash() armazena uma mensagem na sessão do usuário.
        # Ela é exibida UMA VEZ no próximo template renderizado.
        # O segundo argumento é a categoria (usamos para estilizar).
        flash(f'Tarefa "{tarefa}" adicionada!', "sucesso")
    else:
        flash("Digite algo antes de adicionar.", "erro")

    # Redireciona para a função index() do blueprint "main".
    # url_for("main.index") → "/" 
    # Isso evita que o formulário seja reenviado ao atualizar a página (PRG pattern).
    return redirect(url_for("main.index"))


# ROTA POST "/delete/<int:index>"
# <int:index> é um parâmetro dinâmico na URL, convertido para inteiro.
# Exemplo: POST /delete/0 remove a primeira tarefa.
@main.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    # Verifica se o índice é válido antes de tentar remover.
    if 0 <= index < len(tarefas):
        removida = tarefas.pop(index)
        flash(f'Tarefa "{removida}" removida.', "aviso")
    else:
        flash("Tarefa não encontrada.", "erro")
    return redirect(url_for("main.index"))


# ROTA POST "/clear"
# Remove todas as tarefas de uma vez.
@main.route("/clear", methods=["POST"])
def clear():
    # .clear() esvazia a lista no lugar (in-place), sem criar uma nova.
    tarefas.clear()
    flash("Todas as tarefas foram removidas.", "aviso")
    return redirect(url_for("main.index"))
