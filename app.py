from flask import Flask, redirect, render_template, request, url_for
from models.tarefa import Tarefa
from models.database import init_db 

app = Flask(__name__)

init_db()

@app.route('/')
def home():
    return render_template('home.html', titulo='Home')

@app.route('/agenda', methods=['GET', 'POST'])
def agenda():
    if request.method == 'POST':
        titulo_tarefa = request.form['titulo_tarefa']
        data_conclusao = request.form['data_conclusao']
        tarefa = Tarefa(titulo_tarefa, data_conclusao)
        tarefa.salvar_tarefa()

    tarefas = Tarefa.obter_tarefas()
    return render_template('agenda.html', titulo='Agenda', tarefas=tarefas)

@app.route('/delete/<int:idTarefa>')
def delete(idTarefa):
    tarefa = Tarefa.id(idTarefa)
    tarefa.excluir_tarefa()
    return redirect(url_for('agenda'))

@app.route('/update/<int:idTarefa>', methods=['GET', 'POST'])
def update(idTarefa):
    if request.method == 'POST':
        titulo = request.form['titulo_tarefa']
        data = request.form['data_conclusao']
        tarefa = Tarefa(titulo, data, idTarefa)
        tarefa.atualizar_tarefa()
        return redirect(url_for('agenda'))

    tarefas = Tarefa.obter_tarefas()
    tarefa_selecionada = Tarefa.id(idTarefa)
    return render_template(
        'agenda.html',
        titulo=f'Editando a tarefa ID: {idTarefa}',
        tarefas=tarefas,
        tarefa_selecionada=tarefa_selecionada
    )

@app.route('/toggle/<int:idTarefa>')
def toggle(idTarefa):
    tarefa = Tarefa.id(idTarefa)

    if tarefa.concluida == 1:
        tarefa.reabrir()
    else:
        tarefa.concluir()

    return redirect(url_for('agenda'))

@app.route('/Hello')
def hello_world():
    return 'Hello, World!'