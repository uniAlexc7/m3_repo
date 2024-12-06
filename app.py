import streamlit as st
import sqlite3
import time
from middleware import criar_tarefa, criar_categoria, criar_branch, listar_tarefas, atualizar_status_tarefa, deletar_tarefa



def task_listing():
    st.title("📋 Resumo de Tasks")
    
    # Filtros
    col1, col2 = st.columns(2)
    
    with col1:
        # Filtro de Estágio
        estagio_selecionado = st.selectbox(
            "Filtrar por Estágio", 
            ["Todos", "Pendente", "Em Progresso", "Concluída"]
        )
    
    with col2:
        # Opção de Ordenação
        ordem_selecionada = st.radio(
            "Ordenar por Data de Criação",
            ["Mais Recente", "Mais Antiga"]
        )
    
    # Buscar tarefas
    tarefas = listar_tarefas()
    
    # Aplicar filtro de estágio
    if estagio_selecionado != "Todos":
        tarefas = [tarefa for tarefa in tarefas if tarefa[3] == estagio_selecionado]
    
    # Aplicar ordenação
    tarefas_ordenadas = sorted(
        tarefas, 
        key=lambda x: x[4],  # Ordenar pela data de criação
        reverse=(ordem_selecionada == "Mais Recente")
    )
    
    # Exibir tarefas
    if tarefas_ordenadas:
        for tarefa in tarefas_ordenadas:
            with st.expander(f"🔹 {tarefa[1]}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Status:** {tarefa[3]}")
                    st.markdown(f"**Criada em:** {tarefa[4]}")
                
                with col2:
                    st.markdown(f"**Descrição:** {tarefa[2] or 'Sem descrição'}")
                
                # Botão para ver detalhes
                if st.button(f"Ver Detalhes {tarefa[0]}", key=f"task_{tarefa[0]}"):
                    st.info(f"Redirecionando para detalhes da Task {tarefa[0]}")
    else:
        st.info("Nenhuma task encontrada com os filtros selecionados.")

@st.dialog("Nova Task")
def new_task():
    with st.form("task"):
        st.write("Preencha os campos")
        nova_task_titulo = st.text_input("Título da Task")
        nova_task_descricao = st.text_area("Descrição")
        submitted = st.form_submit_button("Salvar Task")
        if submitted:
            if nova_task_titulo:
                criar_tarefa(nova_task_titulo, nova_task_descricao)
                st.toast("Task criada com sucesso!")
                st.rerun()
            else:
                st.warning("Preencha o titulo")


## Nova categoria
@st.dialog("Nova Categoria")
def new_category():
    with st.form("Categoria"):
        nova_categoria_nome = st.text_input("Nome da Categoria")
        submitted = st.form_submit_button("Criar Categoria")
        if submitted:
            if nova_categoria_nome:
                criar_categoria(nova_categoria_nome)        
                st.toast("Categoria criada com sucesso!")
                time.sleep(.5)
                st.rerun()
            else:
                st.warning("Preencha o Nome")
   
@st.dialog("Nova Branch")
def new_Branch():
    with st.form("Branch"):
        nova_branch_nome = st.text_input("Nome da Branch")
        submitted = st.form_submit_button("Criar Branch")
        if submitted:
            if nova_branch_nome:
                criar_branch(nova_branch_nome)        
                st.toast("Branch criada com sucesso!")
                st.rerun()
            else:
                st.warning("Preencha o Nome")

@st.dialog("Deletar tarefa")
def delete_task(task_id):
    st.write("Cofirmar exclusão da tarefa")
    if st.button("Deletar"):
        deletar_tarefa(task_id)
        st.rerun()
    if st.button("Cancelar", type="primary"):
        st.rerun()
def main():
    # Configuração do layout da página
    st.set_page_config(layout="wide")
    
    # Sidebar com botões de ação
    with st.sidebar:
        st.title("Painel de Ações")
        
        # Botão para Criar Nova Task
        if st.button("Criar Nova Task"):
            new_task()
        
                
        
        # Botão para Criar Nova Categoria
        if st.button(" Criar Nova Categoria"): 
            new_category()
            
        
        # Botão para Criar Nova Branch
        if st.button("Criar Nova Branch"):
            new_Branch()
            

    
    # Corpo principal da página
    st.title("Resumo de Tasks")
    
    # Listar tarefas
    tarefas = listar_tarefas()
    
    if tarefas:
        # Layout em colunas para exibição das tasks
        for i in range(0, len(tarefas), 3):
            cols = st.columns(3)
            
            for j in range(3):
                if i + j < len(tarefas):
                    tarefa = tarefas[i + j]
                    with cols[j]:
                        with st.container(border=True):
                            st.markdown(f"## {tarefa[1]} \n ##### {tarefa[2]} \n")
                            st.write(f"**Status:** {tarefa[3]}")
                            st.write(f"**Criada em:** {tarefa[4]}")
                            task_id = tarefa[0]
                            # Botão para redirecionar para detalhes da task
                            if st.button("Atualizar Estágio", key=f"task_{tarefa[0]}"):
                                
                                stage = tarefa[3]
                                if stage == "Pendente":
                                    new_stage = "Em Progresso"
                                elif stage == "Em Progresso":
                                    new_stage = "Concluída"
                                else:
                                    new_stage = "Arquivado"
                                
                                atualizar_status_tarefa(task_id, new_stage)
                                st.rerun()
                            if st.button("Delete",  key=f"taskdel_{tarefa[0]}"):
                                delete_task(task_id)
    else:
        st.info("Nenhuma task cadastrada ainda.")

if __name__ == "__main__":
    main()