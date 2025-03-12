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

@app.route('/chack', methods=['POST'])
def chack():
  tipo = request.form['tipo']
  match tipo:
    case 'Códigopag1':
      codigo = request.form['codig']
      nome = request.form['name']
      cnpj= request.form['cnpj']
      loja= request.form['loja']
      reg= request.form['reg']
      muni= request.form['muni']
      estado= request.form['estado']
      tipo = 'codigo'
      return redirect(url_for('ini', codigo=codigo, nome=nome, cnpj=cnpj, tipo=tipo, loja=loja, reg=reg, estado=estado, muni=muni ))
    case 'nfpag2':
      nf = request.form['nf']
      inf = request.form['inf']

      codigo = request.form['codig']
      nome = request.form['name']
      cnpj= request.form['cnpj']
      loja= request.form['loja']
      reg= request.form['reg']
      muni= request.form['muni']
      estado= request.form['estado']
      tipo = 'nf'
      return redirect(url_for('ini', codigo=codigo, nome=nome, cnpj=cnpj, tipo=tipo, loja=loja, reg=reg, estado=estado, muni=muni, nf=nf, inf=inf ))



##############ressultado filtro#######################
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
, VW.Loja_Cliente
, VW.REGIAO_DESC
, VW.Estado_Entrega
, VW.Minucipio_entrega

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
, VW.Loja_Cliente
, VW.REGIAO_DESC
, VW.Estado_Entrega
, VW.Minucipio_entrega

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
  return render_template('resultado.html', tabela=tabelas)

################resultados do click no campo da tabela################# 
@app.route('/detalhes/<codigo>')
def ini(codigo):
  codigo=codigo
  tipo = request.args.get('tipo')

  conexao = pyodbc.connect(get())
  cursor = conexao.cursor()
  
  match tipo:
    case 'codigo':
      nome = request.args.get('nome')
      cnpj = request.args.get('cnpj')
      loja = request.args.get('loja')
      reg = request.args.get('reg')
      estado = request.args.get('estado')
      muni = request.args.get('muni')
      tipagem = 'codigo'

      query="""
      SELECT
      VW.Cod_Cliente
    , VW.NF
    , VW.ITEMNF
    , VW.VLRTOTAL
    , SUM(VW.Quantidade)
    , VW.Loja_Cliente

    FROM VW_FATURAMENTO_2023 VW
      
      """
      conditions = []
      params = []

      if codigo:
        conditions.append("VW.Cod_Cliente = ?")
        params.append(codigo)
      if loja:
        conditions.append("VW.Loja_Cliente = ?")
        params.append(loja)

    # Se houver condições, adiciona WHERE
      if conditions:
        query += " WHERE " + " AND ".join(conditions)


      query +="""
      GROUP BY
      VW.Cod_Cliente
      , VW.NF
      , VW.ITEMNF
      , VW.VLRTOTAL
      , VW.Loja_Cliente

    """ 
    case 'nf':
      nome = request.args.get('nome')
      cnpj = request.args.get('cnpj')
      loja = request.args.get('loja')
      reg = request.args.get('reg')
      estado = request.args.get('estado')
      muni = request.args.get('muni')
      nf = request.args.get('nf')
      inf = request.args.get('inf')
      tipagem = 'nf'


      query="""
      SELECT
      VW.NF
    , VW.ITEMNF
    , VW.Valor_Unitario
    , VW.Quantidade
    , VW.Descricao
    , VW.DescricaoCientifica
    , VW.Produto

    FROM VW_FATURAMENTO_2023 VW
      
      """
      conditions = []
      params = []

      if codigo:
        conditions.append("VW.NF = ?")
        params.append(nf)
      

    # Se houver condições, adiciona WHERE
      if conditions:
        query += " WHERE " + " AND ".join(conditions)


      query +="""
      GROUP BY
      VW.NF
    , VW.ITEMNF
    , VW.Valor_Unitario
    , VW.Quantidade
    , VW.Descricao
    , VW.DescricaoCientifica
    , VW.Produto

    """ 
      



############render da pagina################       
  cursor.execute(query, params)  
  
  resultado_final = cursor.fetchall()
      
  
  tabelas = {
    'tabela': resultado_final
  }

  cursor.close()
  conexao.close()
  return render_template('clint.html', tabela=tabelas, nome=nome, codigo=codigo, CNPJ=cnpj , tipo=tipagem, loja=loja, reg=reg, estado=estado, muni=muni, nf=nf )

#############final#################
if __name__ == '__main__':
    app.run(debug=True)