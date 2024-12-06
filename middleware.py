import sqlite3
from datetime import datetime

#########


import sqlite3
from datetime import datetime

class DatabaseManager:

## Incialiação do BD
    def __init__(self, db_path='task_manager.db'):
        self.db_path = db_path
        self.criar_tabelas() 

    def _conectar(self):
        """Estabelece conexão com o banco de dados"""
        return sqlite3.connect(self.db_path)

    def criar_tabelas(self):
        """Cria todas as tabelas necessárias se não existirem"""
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            # Tabela de Branches
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS branches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT UNIQUE NOT NULL,
                    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de Categorias
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categorias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT UNIQUE NOT NULL,
                    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de Tarefas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tarefas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    descricao TEXT,
                    status TEXT DEFAULT 'Pendente',
                    prioridade TEXT DEFAULT 'Baixa',
                    categoria_id INTEGER,
                    branch_id INTEGER,
                    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                    data_conclusao DATETIME,
                    FOREIGN KEY(categoria_id) REFERENCES categorias(id),
                    FOREIGN KEY(branch_id) REFERENCES branches(id)
                )
            ''')
            
            conn.commit()
## Funções Crud
    def criar_branch(self, nome):
        """Cria uma nova branch"""
        try:
            with self._conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO branches (nome) VALUES (?)', 
                    (nome,)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def criar_categoria(self, nome):
        """Cria uma nova categoria"""
        try:
            with self._conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO categorias (nome) VALUES (?)', 
                    (nome,)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def criar_tarefa(self, 
                     titulo, 
                     descricao=None, 
                     status='Pendente', 
                     prioridade='Baixa', 
                     categoria_id=None, 
                     branch_id=None):
        """Cria uma nova tarefa"""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tarefas 
                (titulo, descricao, status, prioridade, categoria_id, branch_id) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (titulo, descricao, status, prioridade, categoria_id, branch_id))
            conn.commit()
            return cursor.lastrowid

    def consultar_tarefas(self, 
                           status=None, 
                           categoria_id=None, 
                           branch_id=None, 
                           ordem='data_criacao DESC'):
        """Consulta tarefas com múltiplos filtros"""
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            # Construção dinâmica da query
            query = "SELECT * FROM tarefas WHERE 1=1"
            params = []
            
            if status:
                query += " AND status = ?"
                params.append(status)
            
            if categoria_id:
                query += " AND categoria_id = ?"
                params.append(categoria_id)
            
            if branch_id:
                query += " AND branch_id = ?"
                params.append(branch_id)
            
            query += f" ORDER BY {ordem}"
            
            cursor.execute(query, params)
            return cursor.fetchall()

    def atualizar_status_tarefa(self, tarefa_id, novo_status):
        """Atualiza o status de uma tarefa"""
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            # Se o novo status for 'Concluída', adiciona data de conclusão
            if novo_status == 'Concluída':
                cursor.execute('''
                    UPDATE tarefas 
                    SET status = ?, data_conclusao = ? 
                    WHERE id = ?
                ''', (novo_status, datetime.now(), tarefa_id))
            else:
                cursor.execute('''
                    UPDATE tarefas 
                    SET status = ? 
                    WHERE id = ?
                ''', (novo_status, tarefa_id))
            
            conn.commit()
            return cursor.rowcount > 0

    def deletar_tarefa(self, tarefa_id):
        """Deleta uma tarefa específica"""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tarefas WHERE id = ?', (tarefa_id,))
            conn.commit()
            return cursor.rowcount > 0

    def deletar_categoria(self, categoria_id):
        """Deleta uma categoria e remove referências em tarefas"""
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            # Remove tarefas associadas à categoria
            cursor.execute('DELETE FROM tarefas WHERE categoria_id = ?', (categoria_id,))
            
            # Remove a categoria
            cursor.execute('DELETE FROM categorias WHERE id = ?', (categoria_id,))
            
            conn.commit()
            return cursor.rowcount > 0

# Instância global do gerenciador de banco de dados
db_manager = DatabaseManager()

# Funções de conveniência para importação direta
def criar_branch(nome):
    return db_manager.criar_branch(nome)

def criar_categoria(nome):
    return db_manager.criar_categoria(nome)

def criar_tarefa(titulo, descricao=None, status='Pendente', prioridade='Baixa', categoria_id=None, branch_id=None):
    return db_manager.criar_tarefa(titulo, descricao, status, prioridade, categoria_id, branch_id)

def listar_tarefas(status=None, categoria_id=None, branch_id=None, ordem='data_criacao DESC'):
    return db_manager.consultar_tarefas(status, categoria_id, branch_id, ordem)

def atualizar_status_tarefa(tarefa_id, novo_status):
    return db_manager.atualizar_status_tarefa(tarefa_id, novo_status)

def deletar_tarefa(tarefa_id):
    return db_manager.deletar_tarefa(tarefa_id)

def deletar_categoria(categoria_id):
    return db_manager.deletar_categoria(categoria_id)

######
