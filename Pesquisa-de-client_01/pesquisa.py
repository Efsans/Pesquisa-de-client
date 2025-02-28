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

@app.route('/azul')
def ini():
  return render_template('clint.html')
@app.route('/')
def inicial_pesquisar():
  return render_template('resultado.html')

@app.route('/', methods=['POST'])
def pesquisa():
  
  mult = request.form['mult']
  tipo = request.form['tipo_valor']

  return redirect(url_for('resultado', mult=mult, tipo=tipo))

@app.route('/resultado')
def resultado():
  tipo= request.args.get('tipo')
  valor= request.args.get('mult')
  conexao = pyodbc.connect(get())
  cursor = conexao.cursor()

  query="""
SELECT
	VW.Cod_Cliente
,	VW.Loja_Cliente
,	VW.Nome_Cliente
,	VW.Produto
,	VW.Descricao
,	VW.Pedido
,	VW.CNPJ
,	VW.Quantidade
,	VW.Valor_Unitario
,	VW.Valor_Total
,	VW.CHASSI
,	VW.Vendedor
,COUNT(VW.Valor_Total)

FROM VW_FATURAMENTO_2023 VW

WHERE YEAR(VW.DATA_FAT) = 2025

  """
  conditions = []
  params = []

  match tipo:
    case 'CNPJ':
        valor = formatinho(valor)
        conditions.append("VW.CNPJ = ?")
        params.append(valor)

    case 'Nome':
        conditions.append("VW.Nome_Cliente = ?")
        params.append(valor)

    case 'Código do Cliente':
        valor = formatinho(valor)
        conditions.append("VW.Cod_Cliente = ?")
        params.append(valor)

    case 'CPF':
      valor = formatinho(valor)
      conditions.append("VW.CNPJ = ?")
      params.append(valor)    

# Se houver condições, adiciona WHERE
  if conditions:
    query += " AND " + " AND ".join(conditions)


  query +="""
  GROUP BY
  VW.FILIAL
,	VW.Cod_Cliente
,	VW.Loja_Cliente
,	VW.Nome_Cliente
,	VW.Produto
,	VW.Descricao
,	VW.Pedido
,	VW.CNPJ
,	VW.Quantidade
,	VW.Valor_Unitario
,	VW.Valor_Total
,	VW.CHASSI
,	VW.Vendedor

"""
# VW_GAIZ_CONTAS_RECEBER
  # print(query)
  # print(tipo) 

  if params:
    cursor.execute(query, params)
  else:
    cursor.execute(query)  
  resultado_final = cursor.fetchall()

  tabelas = {
    'tabela': resultado_final
  }

  cursor.close()
  conexao.close()
  return render_template('resultado.html', tabela=tabelas)

if __name__ == '__main__':
    app.run(debug=True)