from sqlite3 import Connection, connect, Cursor 
from types import TracebackType
from typing import Any, Optional, Self, Type
from unittest.mock import Base
from dotenv import load_dotenv
import traceback
import os

load_dotenv() # Procura um arquivo .env com variaveis 
DB_PATH = os.getenv('DATABASE', './data/tarefas.sqlite3') 

def init_db(db_name: str = DB_PATH) -> None:
    with connect(db_name) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo_tarefa TEXT NOT NULL,
            data_conclusao TEXT);
        """)

class Database:
    """
        Classe que gerencia conexões e operações com um banco de dados 
        SQLite. Utiliza o protocolo de gerenciamento de contexto para 
        garantir que a conexão seja encerrada corretamente.
    """
    def __init__(self, db_name: str = DB_PATH) -> None:
        self.connection: Connection = connect(db_name)
        self.cursor = self.connection.cursor()

    def executar(self, query: str, params: tuple = ()) -> Cursor:
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor
    
    def buscar_tudo(self, query: str, params: tuple = ()) -> list[Any]:
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def close(self) -> None:
        self.connection.close()

    # Metodos para o gerenciamento de contextos

    # Metodo de entrada do contexto

    def __enter__(self) -> Self:
        return self
    
    # Metodo de saida do contexto

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException], tb: Optional[TracebackType]) -> None:

        if exc_type is not None:
            print('Exceção capturada no contexto:')
            print(f'Tipo: {exc_type.__name__}')
            print(f'Mensagem: {exc_value}')
            print('Traceback completo:')




        self.close()

#Area de teste 
#try:
#     db = Database('./data/tarefas.sqlite3')
#     db.executar('''
#         CREATE TABLE IF NOT EXISTS tarefas (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             titulo_tarefa TEXT NOT NULL,
#             data_conclusao TEXT);
#     ''')
#     db.executar('INSERT INTO tarefas (titulo_tarefa,data_conclusao) VALUES (?, ?);', ('Estudar Python', '2026-02-02'))
# except Exception as e:
#     print(f'Erro ao criar a tabela: {e}')
# finally:
#     db.close()