
import pandas as pd
import pyodbc
from flask import Flask, request, render_template
import re

app = Flask(__name__)

def get():  
  dados_conexao = ("Driver={SQL Server};"
                  "Server=TOTVSAPL;"
                  "Database=protheus12_producao;"
                  "UID=consulta;"
                  "PWD=consulta;")
  return dados_conexao
def formatinho(n):
  return re.sub(r'\D', '', n)

@app.route('/')
def inicial_pesquisar():
  return render_template('clint.html')


@app.route('/', methods=['POST'])
def pesquisa():
  conexao = pyodbc.connect(get())
  cursor = conexao.cursor()
  checar = request.form['CNPJ']
  print(checar)
  chack = formatinho(checar)

  cursor.execute("""
SELECT 
  A1.A1_COD
, A1.A1_LOJA
, A1.A1_NOME
, fatu.Cod_Cliente
, fatu.Produto
, fatu.Descricao
, con.CNPJ
, con.EMISSAO 
FROM SA1010 A1 
inner join VW_FATURAMENTO_2023 fatu 
on A1.A1_COD =  fatu.Cod_Cliente 
inner join VW_GAIZ_CONTAS_RECEBER con
on A1.A1_COD = con.CLIENTE
where con.CNPJ = ?""",(chack))
  tabela_SA1 = cursor.fetchall()

  tabelas ={
    'tabela' : tabela_SA1

  }

  cursor.close()
  conexao.close()
  return render_template('clint.html', tabela=tabelas)

if __name__ == '__main__':
    app.run(debug=True)