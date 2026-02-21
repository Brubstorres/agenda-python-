from sqlite3 import Cursor
from models.database import Database
from typing import Optional, Self, Any
from datetime import datetime


class Tarefa:
    """
        Classe para representar tarefa, com metodos para salvar, 
        obter, excluir e atualizar tarefas em um banco de dados usando a classe `Database`.
    """
    def __init__(
        self: Self, 
        titulo_tarefa: Optional[str], 
        data_conclusao: Optional[str] = None, 
        id_tarefa: Optional[int] = None,
        concluida: int = 0,
        data_hora_conclusao: Optional[str] = None
    ) -> None:
        self.titulo_tarefa = titulo_tarefa
        self.data_conclusao = data_conclusao
        self.id_tarefa = id_tarefa
        self.concluida = concluida
        self.data_hora_conclusao = data_hora_conclusao

    @classmethod
    def id(cls, id: int) -> Self:
        with Database() as db:
            query = '''
            SELECT titulo_tarefa, data_conclusao, concluida, data_hora_conclusao 
            FROM tarefas WHERE id = ?;
            '''
            params = (id,)
            [[titulo, data, concluida, data_hora]] = db.buscar_tudo(query, params)

        return cls(titulo, data, id, concluida, data_hora)

    def salvar_tarefa(self: Self) -> None:
        with Database() as db:
            query = """
            INSERT INTO tarefas 
            (titulo_tarefa, data_conclusao, concluida, data_hora_conclusao) 
            VALUES (?, ?, 0, NULL);
            """
            params = (self.titulo_tarefa, self.data_conclusao)
            db.executar(query, params)

    @classmethod
    def obter_tarefas(cls) -> list[Self]:
        with Database() as db:
            query = '''
            SELECT titulo_tarefa, data_conclusao, id, concluida, data_hora_conclusao 
            FROM tarefas;
            '''
            resultados = db.buscar_tudo(query)
            tarefas = [
                cls(titulo, data, id, concluida, data_hora)
                for titulo, data, id, concluida, data_hora in resultados
            ]
            return tarefas 
        
    def excluir_tarefa(self) -> Cursor:
        if self.concluida == 1:
            return None

        with Database() as db:
            query = 'DELETE FROM tarefas WHERE id = ?;'
            params = (self.id_tarefa,)
            return db.executar(query, params)
        
    def atualizar_tarefa(self) -> Cursor:
        with Database() as db:
            query = '''
            UPDATE tarefas 
            SET titulo_tarefa = ?, data_conclusao = ? 
            WHERE id = ?;
            '''
            params = (self.titulo_tarefa, self.data_conclusao, self.id_tarefa)
            return db.executar(query, params)

    def concluir(self) -> None:
        if self.concluida == 1:
            return

        with Database() as db:
            agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = '''
            UPDATE tarefas 
            SET concluida = 1, data_hora_conclusao = ?
            WHERE id = ?;
            '''
            params = (agora, self.id_tarefa)
            db.executar(query, params)

    def reabrir(self) -> None:
        with Database() as db:
            query = '''
            UPDATE tarefas 
            SET concluida = 0, data_hora_conclusao = NULL
            WHERE id = ?;
            '''
            params = (self.id_tarefa,)
            db.executar(query, params)