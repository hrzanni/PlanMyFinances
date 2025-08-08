from flask import Flask, render_template, request, redirect
import json
import csv
from datetime import datetime
import os

app = Flask(__name__)


# Proximo passo
# Desenvolverados = sorted(dados, key=lambda x: x['data'], reverse=True)  no espaço vazio um resumo geral de receitas e gastos recentes

#Precisa colocar tudo no def home
#As transações estao aparecendo add-revenue e add-expense


# Um subtipo precisa estar relacionado a um tipo



def carregar_dados_json(arquivo):
    try:
        if os.path.getsize(arquivo) == 0:
            return []
        with open(arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
def escrita_json(arquivo, dados):
    with open(arquivo , 'w') as f:
        json.dump(dados, f, indent=4)
    
    return

def carregar_dados_csv(arquivo):
    modelo_disponiveis = []
    try:
        with open(arquivo, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:
                    modelo_disponiveis.append(row[0])
    except FileNotFoundError:
        pass

    return modelo_disponiveis

def retorna_tiposDisponiveis():
    return carregar_dados_csv('data/tipos.csv')    


def retorna_subtiposDisponiveis():
    return carregar_dados_csv('data/subtipos.csv')


def retorna_ultimasMovimentacoes():
    movimentacoes = carregar_dados_json('data/transacoes.json')

    return movimentacoes

@app.route('/')
def home():

    #Chama a função que retorna uma lista com os tipos disponiveis
    tipos_disponiveis = retorna_tiposDisponiveis()
    print(f'Os TIPOS disponiveis{tipos_disponiveis}')

    #Chama a função que retorna uma lista com os subtipos disponiveis
    subtipos_disponiveis = retorna_subtiposDisponiveis()
    print(f'Os SUBTIPOS disponiveis{subtipos_disponiveis}')

    movimentacoes = retorna_ultimasMovimentacoes()


    return render_template('home.html', tipos_disponiveis=tipos_disponiveis, subtipos_disponiveis=subtipos_disponiveis, movimentacoes=movimentacoes)

@app.route('/add-revenue', methods=['POST'])
def add_revenue():
    nova_receita = {
        'categoria': 'receita',
        'valor': float(request.form['valor']),
        'descricao': request.form['descricao'],
        'tipo': request.form['tipo'],
        'subtipo': request.form.get('subtipo', ''),
        'data': request.form['data']
    }

    dados = carregar_dados_json('data/receitas.json')
    dados.append(nova_receita)
    escrita_json('data/receitas.json', dados)

    transacoes = carregar_dados_json('data/transacoes.json')
    transacoes.append(nova_receita)
    escrita_json('data/transacoes.json', transacoes)
    
    return redirect('/')

@app.route('/add-expense', methods=['POST'])
def add_expense():
    nova_despesa = {
        'categoria': 'despesa',
        'valor': float(request.form['valor']),
        'descricao': request.form['descricao'],
        'tipo': request.form['tipo'],
        'subtipo': request.form.get('subtipo', ''),
        'data': request.form['data']
    }

    despesas = carregar_dados_json('data/despesas.json')
    despesas.append(nova_despesa);
    escrita_json('data/despesas.json', despesas)

    transacoes = carregar_dados_json('data/transacoes.json')
    transacoes.append(nova_despesa)
    escrita_json('data/transacoes.json', transacoes)


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