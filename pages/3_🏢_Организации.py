import streamlit as st
import pandas as pd
import utils.utils as utils
import utils.orgs_db as orgs_db
utils.auth_check()
conn = utils.get_conn_status()

#from database import get_orgs, add_org, update_org, delete_org

#st.title("Организации")

# Отображение всех пользователей
#if st.button("Показать Организации"):
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
st.markdown("Выберите Организацию для изменения или .") 
# Форма для добавления пользователя
with st.form(key='add_org_form'):
    #org_id = st.number_input("ID", min_value=1)
    name = st.text_input("Наименование")
    submit_button = st.form_submit_button("Добавить Организацию")

    if submit_button:
        orgs_db.add_org(name)
        st.success("Организация добавлена успешно!")
        st.rerun()

#selected_org = event_orgs_df.selection.rows
if len(selected_org) > 0:
    for org in selected_org:
     filtered_org = orgs_df.iloc[org]
     selected_org_id = int(filtered_org["id"])
    

    # Форма для обновления пользователя
    with st.form(key='update_org_form'):
        #update_id = st.number_input("Update org ID", min_value=1)
        update_id = selected_org_id
        update_name = st.text_input("Новое Наименование")
        update_button = st.form_submit_button("Обновить Организацию")

        if update_button:
            orgs_db.update_org(update_id, update_name)
            st.success("Организация обновлена успешно!")
            st.rerun()
            

    # Форма для удаления пользователя
    with st.form(key='delete_org_form'):
        #delete_id = st.number_input("Delete org ID", min_value=1)
        delete_id = selected_org_id
        delete_button = st.form_submit_button("Удалить Организацию")

        if delete_button:
            orgs_db.delete_org(delete_id)
            st.success("Организация удалена успешно!")
            st.rerun()
            
else:  
  st.markdown("Организация не выбрана.")
