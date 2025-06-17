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
    sql_command = "SELECT t.* FROM tarefas t"
    cursor.execute(sql_command)
    
    resultados = cursor.fetchall()
    if not resultados:
        return jsonify([]), 200
    
    tarefas = [{"id": tarefa[0], "titulo": tarefa[1], "descricao": tarefa[2]} for tarefa in resultados]
    return jsonify(tarefas), 200 


@app.route("/tarefas", methods=["POST"])
def adiciona_tarefa():

    dados = request.json 

    conn = conectar_db()
    if conn is None: 
        return jsonify({"error": "Erro ao conectar com o banco de dados"}), 500 
    
    cursor = conn.cursor()
    sql_command = "INSERT INTO tarefas (titulo, descricao) VALUES (?, ?)"
    cursor.execute(sql_command, (dados.get("titulo"), dados.get("descricao")))
    conn.commit()
    conn.close()

    return jsonify({"menssagem": "Tarefa adicionada com sucesso"}), 201
    


@app.route("/tarefas/<int:id>", methods=["PUT"])
def edita_tarefa(id):
    dados = request.json 

    conn = conectar_db()
    if conn is None: 
        return jsonify({"error": "Erro ao conectar com o banco de dados"}), 500 
    
    cursor = conn.cursor()
    sql_command = "UPDATE tarefas SET titulo=?, descricao=? WHERE id=?"
    cursor.execute(sql_command, (dados.get("titulo"), dados.get("descricao"), id))
    conn.commit()
    conn.close()

    return jsonify({"messagem": "Tarefa atualizada com sucesso"}), 200 
    


if __name__ == '__main__':
    app.run(debug=True)
