import sqlite3
import os

DB_PATH = 'usuarios.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nombre TEXT UNIQUE NOT NULL,
                  saldo REAL DEFAULT 100.0)''')
    conn.commit()
    conn.close()

def get_usuario(nombre):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE nombre = ?", (nombre,))
    usuario = c.fetchone()
    conn.close()
    return usuario

def crear_usuario(nombre, saldo_inicial=100.0):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO usuarios (nombre, saldo) VALUES (?, ?)",
                  (nombre, saldo_inicial))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def actualizar_saldo(nombre, nuevo_saldo):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE usuarios SET saldo = ? WHERE nombre = ?",
              (nuevo_saldo, nombre))
    conn.commit()
    conn.close()

def listar_usuarios():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT nombre, saldo FROM usuarios")
    usuarios = c.fetchall()
    conn.close()
    return usuarios
