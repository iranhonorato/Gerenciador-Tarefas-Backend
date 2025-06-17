from flask import Flask, request, jsonify
from flask_cors import CORS 
import sqlite3 


app = Flask(__name__)
CORS(app) 



def conectar_db():
    return sqlite3.connect("db_gerenciador_tarefas.db")



@app.route("/tarefas", methods=["GET"])
def get_all_tarefas():

    conn = conectar_db()
    if conn is None: 
        return jsonify({"erro": "Erro ao conectar com o banco de dados"}), 500 
    
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
        return jsonify({"erro": "Erro ao conectar com o banco de dados"}), 500 
    
    cursor = conn.cursor()
    sql_command = "INSERT INTO tarefas (titulo, descricao) VALUES (?, ?)"
    cursor.execute(sql_command, (dados.get("titulo"), dados.get("descricao")))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Tarefa adicionada com sucesso"}), 201
    

@app.route("/tarefas/<int:id>", methods=["GET"])
def get_tarefa(id): 
    conn = conectar_db()
    if conn is None: 
        return jsonify({"erro":"Erro ao conectar com o banco de dados"}), 500
    
    cursor = conn.cursor()
    sql_command = "SELECT * FROM tarefas WHERE id=?"
    cursor.execute(sql_command, (id, ))

    resultado = cursor.fetchone()
    if not resultado:
        return jsonify([]), 200 
    
    tarefa = [{"id": resultado[0], "titulo": resultado[1], "descricao":resultado[2]}]
    return jsonify(tarefa), 200 



@app.route("/tarefas/<int:id>", methods=["PUT"])
def edita_tarefa(id):
    dados = request.json 

    conn = conectar_db()
    if conn is None: 
        return jsonify({"erro": "Erro ao conectar com o banco de dados"}), 500 
    
    cursor = conn.cursor()
    sql_command = "UPDATE tarefas SET titulo=?, descricao=? WHERE id=?"
    cursor.execute(sql_command, (dados.get("titulo"), dados.get("descricao"), id))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Tarefa atualizada com sucesso"}), 200 
    



@app.route("/tarefas/<int:id>", methods=["DELETE"])
def deleta_tarefa(id): 

    conn = conectar_db()
    if conn is None: 
        return jsonify({"erro": "Erro ao conectar com o banco de dados"}), 500 
    
    cursor = conn.cursor()
    sql_command = "DELETE FROM tarefas WHERE id=?"
    cursor.execute(sql_command, (id, ))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    return jsonify({"mensagem": "Tarefa deletada com sucesso"}), 200 
    

if __name__ == '__main__':
    app.run(debug=True)
