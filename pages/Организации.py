import streamlit as st
import pandas as pd
import utils.utils as utils
import utils.orgs_db as orgs_db
utils.auth_check()
conn = utils.get_conn_status()
    
def fill_orgs_container():
    orgs_df = orgs_db.get_orgs()
    column_configuration = {
        "id": st.column_config.TextColumn(
            "ИД", help="ИД", width="small"
        ),
        "name": st.column_config.TextColumn(
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
@st.dialog("Изменить Реквизиты Организации")
def update_org_form():
    with st.form(key='update_org_form'):
        update_id = st.session_state.selected_org_id
        selected_org_name = st.session_state.selected_org_name
        update_name_old = st.text_input("Старое Наименование",disabled=True,value=selected_org_name)
        update_name = st.text_input("Новое Наименование")
        update_button = st.form_submit_button("Изменить")
  
        if update_button:
            orgs_db.update_org(update_id, update_name)
            utils.queue_op_status("Организация изменена","success")
            del st.session_state.selected_org_id
            st.rerun()

# Форма для удаления пользователя
@st.dialog("Удалить Организацию")
def delete_org_form():
    with st.form(key='delete_org_form'):
        delete_id = st.session_state.selected_org_id
        delete_button = st.form_submit_button("(Опасно) Удалить")

        if delete_button:
            orgs_db.delete_org(delete_id)
            utils.queue_op_status("Организация удалена","success")
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
def cancel_selection():
    if "selected_org_id" in st.session_state:
        del st.session_state.selected_org_id 
    if "selected_org_name" in st.session_state:    
        del st.session_state.selected_org_name
    st.rerun()

header_container = st.empty()
header_container.header("Организации")
orgs_container = st.empty()
orgs_df,column_configuration = fill_orgs_container()

if not "selected_org_id" in st.session_state:
    with orgs_container:       
        event_orgs_df= st.dataframe(
            orgs_df,
            column_config=column_configuration,
            use_container_width=True,
            hide_index=True,
            on_select=orgs_df_callback,
            selection_mode="single-row",
            key="event_orgs_df"
            )
else:
    header_container.header("Организация")
    with orgs_container:      
        st.info(st.session_state.selected_org_name)


col1, col2, col3 = st.columns(3)
with col1: 
    if "selected_org_id" in st.session_state:
        if st.button("Отмена",disabled = not "selected_org_id" in st.session_state):            
            cancel_selection()
    else:           
        if st.button("Добавить",disabled = "selected_org_id" in st.session_state):            
            add_org_form()
with col2:
    if st.button("Изменить",disabled = not "selected_org_id" in st.session_state):
        update_org_form()
with col3:
    if st.button("Удалить",disabled = not "selected_org_id" in st.session_state):
        delete_org_form()

op_status_container = st.empty()
utils.setup_op_status(op_status_container,"Выберите Организацию для изменения или нажмите Добавить Организацию.")
#if utils.first_visit_op_status():
#    utils.show_op_status(op_status_container,"Выберите Организацию для изменения или нажмите Добавить Организацию.")
#else:
#    if "op_status_queued" in st.session_state:
#        utils.show_op_status(op_status_container,st.session_state.op_status_queued,st.session_state.op_status_queued_type)
#        del st.session_state.op_status_queued
#        del st.session_state.op_status_queued_type
