import os
import sqlite3

# Conectar ao banco de dados
def conexao():
    if not os.path.exists('database'):
        os.makedirs('database')
    if not os.path.exists('database/sqlite.db'):
        conn = sqlite3.connect('database/sqlite.db')
        criarTabela(conn)
    else:
        conn = sqlite3.connect('database/sqlite.db')
        criarTabela(conn)
    conn.row_factory = sqlite3.Row
    return conn

# Criação das tabelas
def criarTabela(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS especie (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            ativo INTEGER,
            img BLOB
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS animal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            descricao TEXT NOT NULL,
            porte Varchar(50),
            sexo Varchar(10),
            castrado Varchar(3),
            raca Varchar(20),
            faixa_etaria Varchar(50),
            comportamento Varchar(20),
            img BLOB,
            ativo INTEGER,
            id_especie INTEGER,
            FOREIGN KEY(id_especie) REFERENCES especie(id)
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL         
           
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS adocao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL,
            endereco TEXT NOT NULL,
            id_animal INTERGER,
            FOREIGN KEY(id_animal) REFERENCES animal(id)         
           
        )
    ''')

    #inserir(conn)
    
    conn.commit()