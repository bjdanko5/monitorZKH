import streamlit as st
import pandas as pd
import utils.utils as utils
import utils.roles_db as roles_db
conn = utils.conn_and_auth_check()
def fill_roles_container():
    roles_df = roles_db.get_roles()
    column_configuration = {
        "id": st.column_config.NumberColumn(
            "ИД", help="ИД", width="small"
        ),
        "name": st.column_config.TextColumn(
            "Наименование",
            help="Наименование",
            width="medium"                   
        ),
        "target": st.column_config.TextColumn(
        "Цель",
         help="Целевая сущность, например:Пользователь, Организация",
         width="small"       
        ),
    }
    return roles_df,column_configuration 


def roles_df_callback():
    #это заглушка на будущее
    ss =  st.session_state["event_roles_df"]

header_container = st.empty()
header_container.header("Роли")

roles_container = st.container()
roles_df,column_configuration = fill_roles_container()
original_roles_df = roles_df.copy()

with roles_container:       
   event_roles_df= st.data_editor(
        roles_df,
        column_config=column_configuration,
        use_container_width=True,
        hide_index=True,
        disabled=["id"],
        num_rows="dynamic",
        on_change=roles_df_callback,
        key="event_roles_df"
        )
  
op_status_container = st.empty()
col1, col2, col3 = st.columns(3)
with col1: 
    if st.button("Записать"):
        if "event_roles_df" in st.session_state:
            st.session_state["event_roles_df"]
            edited_rows = st.session_state["event_roles_df"]["edited_rows"]
            added_rows = st.session_state["event_roles_df"]["added_rows"]
            deleted_rows = st.session_state["event_roles_df"]["deleted_rows"]
            # Update existing roleanizations
            if len(edited_rows)> 0 or len(added_rows) > 0 or len(deleted_rows) >0:
                for row_id, row in edited_rows.items():
                    role_name = row["name"]
                    role_target = row["target"]
                    role_id = int(original_roles_df.iloc[int(row_id)]["id"])
                    roles_db.update_role(role_id, role_name, role_target)
                # Add new roleanizations
                for row in added_rows:
                    role_name = row["name"]
                    role_target = row["target"]
                    roles_db.add_role(role_name, role_target)
                # Delete roleanizations
                for row_id in deleted_rows:
                    role_id = int(original_roles_df.iloc[int(row_id)]["id"])
                    roles_db.delete_role(role_id)
            else:
                utils.show_op_status(op_status_container,"Ничего не отредактировано")       

utils.setup_op_status(op_status_container,"Редактируйте Роли и нажмите Записать")
