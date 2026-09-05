import sqlite3

conn = sqlite3.connect('barbershop.db')
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute('''
CREATE TABLE IF NOT EXISTS barbeiro (
    id_barbeiro INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_barbeiro TEXT NOT NULL,
    tempo_experiencia INTEGER NOT NULL,
    descricao_barbeiro TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS servico (
    id_servico INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_servico TEXT NOT NULL,
    preco REAL NOT NULL,
    duracao INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS barbeiro_servico (
    id_barbeiro INTEGER NOT NULL,
    id_servico INTEGER NOT NULL,
    PRIMARY KEY (id_barbeiro, id_servico),
    FOREIGN KEY (id_barbeiro) REFERENCES barbeiro(id_barbeiro) ON DELETE CASCADE,
    FOREIGN KEY (id_servico) REFERENCES servico(id_servico) ON DELETE CASCADE
)
''')

conn.commit()
conn.close()
