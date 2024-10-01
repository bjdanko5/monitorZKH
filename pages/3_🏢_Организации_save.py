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

st.header("Организации")
orgs_df,column_configuration = fill_orgs_container()
orgs_container = st.empty()
with orgs_container:
    event_orgs_df= st.dataframe(
        orgs_df,
        column_config=column_configuration,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        )
selected_org = event_orgs_df.selection.rows
#st.write(orgs_df)
st.markdown("Выберите Организацию для изменения или нажмите Добавить Организацию.") 

# Форма для добавления пользователя
@st.dialog("Добавить Организацию")
def add_org_form():
    with st.form(key='add_org_form'):
        name = st.text_input("Наименование")
        submit_button = st.form_submit_button("Добавить Организацию")

        if submit_button:
            orgs_db.add_org(name)
            st.success("Организация добавлена успешно!")
            st.rerun()
   # Форма для обновления пользователя 
@st.dialog("Обновить Организацию")
def update_org_form():
    with st.form(key='update_org_form'):
        update_id = selected_org_id
        update_name_old = st.text_input("Старое Наименование",disabled=True,value=selected_org_name)
        update_name = st.text_input("Новое Наименование")
        update_button = st.form_submit_button("Обновить Организацию")
  
        if update_button:
            orgs_db.update_org(update_id, update_name)
            st.success("Организация обновлена успешно!")
            st.rerun()
# Форма для удаления пользователя
@st.dialog("Удалить Организацию")
def delete_org_form():
    with st.form(key='delete_org_form'):
        delete_id = selected_org_id
        delete_button = st.form_submit_button("(Опасно) Удалить Организацию")

        if delete_button:
            orgs_db.delete_org(delete_id)
            st.success("Организация удалена успешно!")
            st.rerun()

col1, col2, col3 = st.columns(3)
with col1:             
    if st.button("Добавить Организацию"):            
        add_org_form()
if len(selected_org) > 0:
    for org in selected_org:
        filtered_org = orgs_df.iloc[org]
        selected_org_id = int(filtered_org["id"])
        selected_org_name = str(filtered_org["name"])

        with col2:
            if st.button("Обновить Организацию"):
                update_org_form()
        with col3:
            if st.button("Удалить Организацию"):
                delete_org_form()
else:  
  st.markdown("Организация не выбрана.")
