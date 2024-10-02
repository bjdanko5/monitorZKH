import streamlit as st
import pandas as pd
import utils.utils as utils
import utils.orgs_db as orgs_db
utils.auth_check()
conn = utils.get_conn_status()
    
def fill_orgs_container():
    orgs_df = orgs_db.get_orgs()
    column_configuration = {
        "org_id": st.column_config.TextColumn(
            "ИД", help="ИД", width="small"
        ),
        "org_name": st.column_config.TextColumn(
            "Наименование",
            help="Тип НП",
            width="medium"       
        )
    }
    return orgs_df,column_configuration 


#Форма для добавления пользователя
@st.dialog("Добавить Организацию")
def add_org_form():
    with st.form(key='add_org_form'):
        name = st.text_input("Наименование")
        submit_button = st.form_submit_button("Добавить Организацию")

        if submit_button:
            orgs_db.add_org(name)
            utils.queue_op_status("Организация добавлена успешно!")
            st.rerun()

# Форма для обновления пользователя 
@st.dialog("Обновить Организацию")
def update_org_form():
    with st.form(key='update_org_form'):
        update_id = st.session_state.selected_org_id
        selected_org_name = st.session_state.selected_org_name
        update_name_old = st.text_input("Старое Наименование",disabled=True,value=selected_org_name)
        update_name = st.text_input("Новое Наименование")
        update_button = st.form_submit_button("Обновить Организацию")
  
        if update_button:
            orgs_db.update_org(update_id, update_name)
            utils.queue_op_status("Организация обновлена успешно!")
            del st.session_state.selected_org_id
            st.rerun()

# Форма для удаления пользователя
@st.dialog("Удалить Организацию")
def delete_org_form():
    with st.form(key='delete_org_form'):
        delete_id = st.session_state.selected_org_id
        delete_button = st.form_submit_button("(Опасно) Удалить Организацию")

        if delete_button:
            orgs_db.delete_org(delete_id)
            utils.queue_op_status("Организация удалена успешно!")
            del st.session_state.selected_org_id
            st.rerun()
def orgs_df_callback():
    selected_org = st.session_state.event_orgs_df.selection.rows   
    if len(selected_org) > 0:
        for org in selected_org:
            filtered_org = orgs_df.iloc[org]
            st.session_state.selected_org_id = int(filtered_org["id"])
            st.session_state.selected_org_name = str(filtered_org["name"])
            utils.show_op_status(op_status_container,"Выбрана Организация " + st.session_state.selected_org_name)
    else:
        if "selected_org_id" in st.session_state:
            del st.session_state.selected_org_id 
        if "selected_org_name" in st.session_state:    
            del st.session_state.selected_org_name
        utils.show_op_status(op_status_container,"Организация не выбрана.")

st.header("Организации")
orgs_df,column_configuration = fill_orgs_container()
orgs_container = st.empty()
with orgs_container:
    orgs_df
    event_orgs_df= st.dataframe(
        orgs_df,
        column_config=column_configuration,
        use_container_width=True,
        hide_index=True,
        on_select=orgs_df_callback,
        selection_mode="single-row",
         key="event_orgs_df"
        )

col1, col2, col3 = st.columns(3)
with col1:             
    if st.button("Добавить"):            
        add_org_form()
with col2:
    if st.button("Обновить",disabled = not "selected_org_id" in st.session_state):
        update_org_form()
with col3:
    if st.button("Удалить",disabled = not "selected_org_id" in st.session_state):
        delete_org_form()
#if "op_status_container" in st.session_state:    
#    op_status_container = st.session_state.op_status_container   
op_status_container = st.empty()
if utils.first_visit_op_status():
    utils.show_op_status(op_status_container,"Выберите Организацию для изменения или нажмите Добавить Организацию.")
else:
    if "op_status_queued" in st.session_state:
        utils.show_op_status(op_status_container,st.session_state.op_status_queued)
        del st.session_state.op_status_queued
    #st.session_state.op_status_container = st.session_state.op_status_container    
#show_op_status("Выберите Организацию для изменения или нажмите Добавить Организацию.")
#st.markdown("Выберите Организацию для изменения или нажмите Добавить Организацию.") 