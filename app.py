from flask import Flask, request, jsonify
from flask_cors import CORS 
import sqlite3 


app = Flask(__name__)
CORS(app) 



def conectar_db():
    return sqlite3.connect("db_gerenciador_tarefas.db")



@app.route("/tarefas", methods=["GET"])
def get_tarefas():

    conn = conectar_db()
    if conn is None: 
        return jsonify({"error": "Erro ao conectar com o banco de dados"}), 500 
    
    cursor = conn.cursor()
    sql_command = "SELECT * FROM tarefas"
    cursor.execute(sql_command)
    
    resultados = cursor.fetchall()
    if not resultados:
        return jsonify([]), 404
    
    tarefas = [{"id": tarefa[0], "titulo": tarefa[1], "descricao": tarefa[2]} for tarefa in resultados]
    return jsonify(tarefas), 200 


if __name__ == '__main__':
    app.run(debug=True)
