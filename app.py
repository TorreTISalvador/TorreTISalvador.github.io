import json
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# JSON com os dados de funcionários
FUNCIONARIOS_DB = 'funcionarios.json'

# carregar dados do JSON
def carregar_funcionarios():
    try:
        with open(FUNCIONARIOS_DB, 'r', encoding='utf-8') as file:
            funcionarios = json.load(file)
            return funcionarios
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return []
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

# rota para receber os dados do formulario
@app.route('/submit', methods=['POST'])
def submit():
    matricula = request.form['matricula']
    data_admissao = request.form['data_admissao']

    funcionarios = carregar_funcionarios()

    # buscar o funcionario pela matricula
    funcionario_encontrado = None
    for funcionario in funcionarios:
        if funcionario['matricula'] == matricula:
            funcionario_encontrado = funcionario
            break

    # se o funcionario n for encontrado exibir mensagem de erro
    if not funcionario_encontrado:
        return f"Erro: Funcionário com matrícula {matricula} não encontrado."

    # se o funcionario for encontrado
    if funcionario_encontrado['data_de_admissao'] == data_admissao:
        return render_template('index.html', resultado=funcionario_encontrado)
    else:
        return f"Erro: Data de admissão incorreta."

if __name__ == '__main__':
    app.run(debug=True)
