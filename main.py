



import streamlit as st
import sqlite3
from datetime import datetime

# Função para criar a tabela de tarefas se não existir
def criar_tabela():
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT DEFAULT 'Pendente',
            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
            data_conclusao DATETIME
        )
    ''')
    conn.commit()
    conn.close()

# Função para adicionar uma nova tarefa
def adicionar_tarefa(titulo, descricao):
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tarefas (titulo, descricao) 
        VALUES (?, ?)
    ''', (titulo, descricao))
    conn.commit()
    conn.close()

# Função para listar todas as tarefas
def listar_tarefas():
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tarefas')
    tarefas = cursor.fetchall()
    conn.close()
    return tarefas

# Função para atualizar o status de uma tarefa
def atualizar_status_tarefa(id_tarefa, novo_status):
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    
    if novo_status == 'Concluída':
        cursor.execute('''
            UPDATE tarefas 
            SET status = ?, data_conclusao = ? 
            WHERE id = ?
        ''', (novo_status, datetime.now(), id_tarefa))
    else:
        cursor.execute('''
            UPDATE tarefas 
            SET status = ? 
            WHERE id = ?
        ''', (novo_status, id_tarefa))
    
    conn.commit()
    conn.close()

# Função para excluir uma tarefa
def excluir_tarefa(id_tarefa):
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tarefas WHERE id = ?', (id_tarefa,))
    conn.commit()
    conn.close()

# Configuração do Streamlit
def main():
    st.title('📋 Gerenciador de Tarefas')
    
    # Criar tabela se não existir
    criar_tabela()
    
    # Seção de adição de tarefas
    st.header('Adicionar Nova Tarefa')
    titulo = st.text_input('Título da Tarefa')
    descricao = st.text_area('Descrição')
    
    if st.button('Adicionar Tarefa'):
        if titulo:
            adicionar_tarefa(titulo, descricao)
            st.success('Tarefa adicionada com sucesso!')
        else:
            st.warning('O título da tarefa é obrigatório!')
    
    # Seção de listagem de tarefas
    st.header('Tarefas Cadastradas')
    
    tarefas = listar_tarefas()
    
    if tarefas:
        for tarefa in tarefas:
            with st.expander(f"📌 {tarefa[1]}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Descrição:** {tarefa[2] or 'Sem descrição'}")
                    st.write(f"**Data de Criação:** {tarefa[4]}")
                
                with col2:
                    status_atual = st.selectbox(
                        'Status', 
                        ['Pendente', 'Em Progresso', 'Concluída'], 
                        index=['Pendente', 'Em Progresso', 'Concluída'].index(tarefa[3]),
                        key=f'status_{tarefa[0]}'
                    )
                    
                    if status_atual != tarefa[3]:
                        atualizar_status_tarefa(tarefa[0], status_atual)
                        st.experimental_rerun()
                
                if st.button(f'Excluir Tarefa {tarefa[0]}', key=f'excluir_{tarefa[0]}'):
                    excluir_tarefa(tarefa[0])
                    st.experimental_rerun()
    else:
        st.info('Nenhuma tarefa cadastrada ainda.')

# Executar o aplicativo
if __name__ == '__main__':
    main()


print("Hello World")