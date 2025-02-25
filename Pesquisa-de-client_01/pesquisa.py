import pandas as pd
import pyodbc
from flask import Flask, request, render_template, redirect, url_for
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
  checar = request.form['CNPJ']
  chack = formatinho(checar)
  return redirect(url_for('resultado', cnpj=chack))

@app.route('/resultado/<cnpj>')
def resultado(cnpj):
  conexao = pyodbc.connect(get())
  cursor = conexao.cursor()

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
, fatu.VLRTOTAL
, fatu.NTVALOR_CT
, fatu.NTVALOR_ST
, fatu.CUSTO_OPERACAO
, fatu.VALOR_CONTABIL
,	COUNT(fatu.VLRTOTAL)
, sum(CUSTO_OPERACAO + VALOR_CONTABIL)

FROM SA1010 A1 
inner join VW_FATURAMENTO_2023 fatu 
on A1.A1_COD =  fatu.Cod_Cliente 
inner join VW_GAIZ_CONTAS_RECEBER con
on A1.A1_COD = con.CLIENTE
where con.CNPJ = ?
GROUP BY  fatu.VALOR_CONTABIL
, fatu.CUSTO_OPERACAO, fatu.NTVALOR_ST
, fatu.NTVALOR_CT
, fatu.VLRTOTAL, A1.A1_COD
, A1.A1_LOJA, A1.A1_NOME
, fatu.Cod_Cliente
, fatu.Produto
, fatu.Descricao
, con.CNPJ
, con.EMISSAO ;
""", (cnpj,))
  tabela_SA1 = cursor.fetchall()

  tabelas = {
    'tabela': tabela_SA1
  }

  cursor.close()
  conexao.close()
  return render_template('resultado.html', tabela=tabelas)

if __name__ == '__main__':
    app.run(debug=True)