from flask import Flask, render_template, request, redirect
import json
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

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


if __name__ == '__main__':
    app.run(debug=True, port=5000)  