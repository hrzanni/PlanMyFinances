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

def retorna_Apenas_SubtitulosDisponiveis():
    
    subtipos = set()
    try:
        with open('data/subtipos.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # Ignora o cabeçalho
            for row in reader:
                if row and len(row) >= 1:
                    subtipo = row[0].strip()
                    if subtipo:
                        subtipos.add(subtipo)
    except FileNotFoundError:
        pass

    return subtipos 

def retorna_subtipos_por_tipo():
    subtipos_por_tipo = {}
    try:
        with open('data/subtipos.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # Pula a primeira linha (cabeçalho)
            for row in reader:
                if row and len(row) == 2:
                    subtipo, tipo = row
                    subtipos_por_tipo.setdefault(tipo.strip().lower(), []).append(subtipo.strip())
    except FileNotFoundError:
        pass
    return subtipos_por_tipo


def retorna_ultimasMovimentacoes():
    movimentacoes = carregar_dados_json('data/transacoes.json')
    
    return movimentacoes[::-1]

@app.route('/')
def home():

    #Chama a função que retorna uma lista com os tipos disponiveis
    tipos_disponiveis = retorna_tiposDisponiveis()
    print(f'Os TIPOS disponiveis{tipos_disponiveis}')

    subtipos_por_tipo = retorna_subtipos_por_tipo()

    movimentacoes = retorna_ultimasMovimentacoes()


    return render_template('home.html', tipos_disponiveis=tipos_disponiveis, subtipos_por_tipo=subtipos_por_tipo, movimentacoes=movimentacoes[:5])

@app.route('/add-revenue', methods=['POST'])
def add_revenue():

    tipo = request.form['tipo'].lower()
    subtipo = request.form.get('subtipo', '')

    nova_receita = {
        'categoria': 'receita',
        'valor': float(request.form['valor']),
        'descricao': request.form['descricao'],
        'tipo': tipo,
        'subtipo': subtipo,
        'data': request.form['data']
    }

    subtipos_por_tipo = retorna_subtipos_por_tipo()

    
    
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
    tipo_relacionado = request.form['tipo_relacionado']

    with open('data/subtipos.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([novo_subtipo, tipo_relacionado])

    return redirect('/')


@app.route('/histórico')
def historico():

    movimentacoes = retorna_ultimasMovimentacoes()

    tipos_disponiveis = retorna_tiposDisponiveis()
    todos_subtipos_disponiveis = retorna_Apenas_SubtitulosDisponiveis()

    categoria_filtro = request.args.get('categoria', '').strip().lower()
    tipo_filtro = request.args.get('tipo', '').strip().lower()
    subtipo_filtro = request.args.get('subtipo', '').strip().lower()

    # Aplica o filtro
    if categoria_filtro:
        movimentacoes = [m for m in movimentacoes if m['categoria'].strip().lower() == categoria_filtro]
    if tipo_filtro:
        movimentacoes = [m for m in movimentacoes if m['tipo'].strip().lower() == tipo_filtro]
    if subtipo_filtro:
        movimentacoes = [m for m in movimentacoes if m['subtipo'].strip().lower() == subtipo_filtro]

    return render_template('historico.html',  movimentacoes_historico=movimentacoes, tipos_disponiveis=tipos_disponiveis,
                           subtipos_disponiveis=todos_subtipos_disponiveis)

if __name__ == '__main__':
    app.run(debug=True, port=5000)  