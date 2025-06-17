import sqlite3 as sql 

conn = sql.connect("db_gerenciador_tarefas.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS tarefas")

sql_command = '''CREATE TABLE "tarefas" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "titulo" TEXT NOT NULL, 
    "descricao" TEXTE NOT NULL
)'''

cursor.execute(sql_command)
conn.commit()
conn.close()