import sqlite3

conn = sqlite3.connect('barbershop.db')
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")


cursor.execute('''
CREATE TABLE IF NOT EXISTS barbeiro (
    id_barbeiro INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_barbeiro TEXT NOT NULL,
    anos_experiencia INTEGER NOT NULL,
    descricao_barbeiro TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_cliente TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS servico (
    id_servico INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_servico TEXT NOT NULL,
    descricao_servico TEXT NOT NULL,
    preco REAL NOT NULL,
    duracao INTEGER NOT NULL
)
''')

cursor.execute("""
    CREATE TABLE IF NOT EXISTS agendamento (
        id_agendamento INTEGER PRIMARY KEY AUTOINCREMENT,
        id_barbeiro INTEGER NOT NULL,
        id_cliente INTEGER NOT NULL,
        data_agendamento DATE NOT NULL,
        hora_agendamento TIME NOT NULL,
        FOREIGN KEY (id_barbeiro) REFERENCES barbeiro(id_barbeiro) ON DELETE CASCADE,
        FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS agendamento_servico (
        id_agendamento INTEGER NOT NULL,
        id_servico INTEGER NOT NULL,
        PRIMARY KEY (id_agendamento, id_servico),
        FOREIGN KEY (id_agendamento) REFERENCES agendamentos(id_agendamento) ON DELETE CASCADE,
        FOREIGN KEY (id_servico) REFERENCES servico(id_servico) ON DELETE CASCADE
);
""")


conn.commit()
conn.close()

