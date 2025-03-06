
from flask import Flask, render_template, request
def get_db_connection():
    # Simulating a database connection for testing purposes
    return None

def formatinho(n):
    return n.strip()

app = Flask(__name__)

@app.route('/')
def index():
    search_value = request.args.get('search')
    tabela = [
        {'Cod_Cliente': 1, 'Nome_Cliente': 'Cliente A', 'CNPJ': '12345678000195'},
        {'Cod_Cliente': 2, 'Nome_Cliente': 'Cliente B', 'CNPJ': '98765432000196'},
    ]
    
    if search_value:
        search_value = formatinho(search_value)
        tabela = [cliente for cliente in tabela if search_value in cliente['CNPJ'] or search_value in cliente['Nome_Cliente']]
    
    return render_template('index.html', tabela=tabela)

@app.route('/details/<int:codigo>')
def details(codigo):
    clientes = {
        1: {'Cod_Cliente': 1, 'Nome_Cliente': 'Cliente A', 'CNPJ': '12345678000195'},
        2: {'Cod_Cliente': 2, 'Nome_Cliente': 'Cliente B', 'CNPJ': '98765432000196'},
    }
    cliente = clientes.get(codigo)
    return render_template('details.html', cliente=cliente)

if __name__ == '__main__':
    app.run(debug=True)