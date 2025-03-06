from flask import Flask, render_template, request, redirect, url_for
import pyodbc
import re

app = Flask(__name__)

def get_db_connection():
    connection_string = (
        "Driver={SQL Server};"
        "Server=YOUR_SERVER_NAME;"
        "Database=YOUR_DATABASE_NAME;"
        "UID=YOUR_USERNAME;"
        "PWD=YOUR_PASSWORD;"
    )
    return pyodbc.connect(connection_string)

def formatinho(n):
    return re.sub(r'\D', '', n)

@app.route('/')
def index():
    search_value = request.args.get('search')
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT Cod_Cliente, Nome_Cliente, CNPJ FROM YOUR_TABLE"
    conditions = []
    params = []

    if search_value:
        search_value = formatinho(search_value)
        conditions.append("CNPJ = ? OR Cod_Cliente = ? OR Nome_Cliente LIKE ?")
        params.extend([search_value, search_value, f"%{search_value}%"])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, params)
    tabela = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', tabela=tabela)

@app.route('/details/<int:codigo>')
def details(codigo):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM YOUR_TABLE WHERE Cod_Cliente = ?", codigo)
    details = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('details.html', cliente=details)

if __name__ == '__main__':
    app.run(debug=True)