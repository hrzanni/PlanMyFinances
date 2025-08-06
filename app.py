from flask import Flask, render_template, request, redirect
import json
import csv
from datetime import datetime
import os

app = Flask(__name__)


@app.route('/')
def home():

    tipos_disponiveis =[]
    try:
        with open('data/tipos.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # evita linhas vazias
                    tipos_disponiveis.append(row[0])
    except FileNotFoundError:
        pass 

    subtipos_disponiveis =[]
    try:
        with open('data/subtipos.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # evita linhas vazias
                    subtipos_disponiveis.append(row[0])
    except FileNotFoundError:
        pass  # caso o arquivo ainda não exista

    return render_template('home.html', tipos_disponiveis=tipos_disponiveis, subtipos_disponiveis=subtipos_disponiveis)

@app.route('/add-revenue', methods=['POST'])
def add_revenue():
    nova_receita = {
        'valor': float(request.form['valor']),
        'descricao': request.form['descricao'],
        'tipo': request.form['tipo'],
        'subtipo': request.form.get('subtipo', ''),
        'data': request.form['data']
    }

    if os.path.exists('receitas.json'):
        with open('receitas.json', 'r') as f:
            dados = json.load(f)

    else:
        dados = []

    dados.append(nova_receita)

    with open('receitas.json' , 'w') as f:
        json.dump(dados, f, indent=4)
    
    return redirect('/')

@app.route('/add-expense', methods=['POST'])
def add_expense():
    nova_despesa = {
        'valor': float(request.form['valor']),
        'descricao': request.form['descricao'],
        'tipo': request.form['tipo'],
        'subtipo': request.form.get('subtipo', ''),
        'data': request.form['data']
    }

    if os.path.exists('despesas.json'):
        with open('despesas.json', 'r') as f:
            despesas = json.load(f)
    
    else:
        despesas = []

    despesas.append(nova_despesa);

    with open('despesas.json', 'w') as f:
        json.dump(despesas, f, indent=4)

    return redirect('/')

@app.route('/add-type', methods=['POST'])
def add_type():
    novo_tipo = request.form['tipos']

    with open('data/tipos.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([novo_tipo])

    return redirect('/')

@app.route('/remove-type')
def remove_type():

    return

@app.route('/add-subtype', methods=['POST'])
def add_subtype():
    novo_subtipo = request.form['subtipos']

    with open('data/subtipos.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([novo_subtipo])

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)  