from flask import Blueprint, render_template, request, redirect, url_for

main = Blueprint("main", __name__)

tarefas = []


@main.route("/")
def index():
    return render_template("index.html", tarefas=tarefas)


@main.route("/add", methods=["POST"])
def add():
    tarefa = request.form.get("tarefa")
    if tarefa:
        tarefas.append(tarefa)
    return redirect(url_for("main.index"))
