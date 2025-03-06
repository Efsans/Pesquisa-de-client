import pandas as pd
import pyodbc
from flask import Flask, request, render_template, redirect, url_for
import re
import jsonify

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
  return render_template('resultado.html')

@app.route('/', methods=['POST'])
def pesquisa():
  
  mult = request.form['mult']
  tipo = request.form['tipo_valor']

  return redirect(url_for('resultado', mult=mult, tipo=tipo))
##############ressultado normal#######################
@app.route('/resultado')
def resultado():
  tipo= request.args.get('tipo')
  valor= request.args.get('mult')
  conexao = pyodbc.connect(get())
  cursor = conexao.cursor()

  query="""
SELECT
	VW.Cod_Cliente
,	VW.Nome_Cliente
,	COUNT(VW.Produto)
,	COUNT(VW.Pedido)
,	VW.CNPJ
,	SUM(VW.Quantidade)
,	SUM(VW.Valor_Unitario)
,	SUM(VW.Valor_Total)
, SUM(VW.VLRTOTAL)

FROM VW_FATURAMENTO_2023 VW

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
    query += " WHERE " + " AND ".join(conditions)


  query +="""
  GROUP BY
	VW.Cod_Cliente
,	VW.Nome_Cliente
,	VW.CNPJ

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

################resultado do click no campo da tabela################# 
@app.route('/detalhes_cliente', methods=['PUT'])
def ini():

  cod = request.form.get('cod')
  nome = request.form.get('nome')
  cnpj = request.form.get('cnpj')

  conexao = pyodbc.connect(get())
  cursor = conexao.cursor()
  
  query="""
  SELECT
	VW.Cod_Cliente
, VW.Loja_Cliente
, VW.FILIAL
, VW.MUNICIPIO
, VW.REGIAO_DESC  
,	VW.Nome_Cliente
,	VW.CNPJ
, SUM(VW.VLRTOTAL)

FROM VW_FATURAMENTO_2023 VW
  
  """
  conditions = []
  params = []

  if cod:
    conditions.append("VW.Cod_Cliente = ?")
    params.append(cod)

# Se houver condições, adiciona WHERE
  if conditions:
    query += " WHERE " + " AND ".join(conditions)


  query +="""
  GROUP BY
	VW.Cod_Cliente
, VW.Loja_Cliente
, VW.FILIAL
, VW.MUNICIPIO
, VW.REGIAO_DESC  
,	VW.Nome_Cliente
,	VW.CNPJ


"""
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
  return render_template('clint.html', tabela=tabelas)
  
  # return jsonify({
  # 'redirect_url': '/pagina_resultado/' +  cod
  # })
# def pagina_resultado(cod_cliente):
#     # Aqui você pode buscar informações e mostrar os detalhes relacionados ao Cod_Cliente
#   return render_template('detalhes_cliente.html', cod_cliente=cod_cliente)
#   # return render_template('clint.html', tabela=tabelas)  

if __name__ == '__main__':
    app.run(debug=True)