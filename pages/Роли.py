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
        "target": st.column_config.SelectboxColumn(
        "Цель 🔽",
            options= ['Пользователь                  ', 'Организация                   '],    
            help="Цель",
            width="small",
            required = True
        ),
    }
    def roles_df_callback():
        #это заглушка на будущее
        ss = st.session_state["event_roles_df"]
        edited_rows = ss["edited_rows"]
        added_rows = ss["added_rows"]
        deleted_rows = ss["deleted_rows"]
        # Обновление существующих данных
        for row_id, row in edited_rows.items():
            role_name = row.get("name", original_roles_df.iloc[int(row_id)]["name"])
            role_target = row.get("target", original_roles_df.iloc[int(row_id)]["target"])
            role_id = int(original_roles_df.iloc[int(row_id)]["id"])
            roles_db.update_role(role_id, role_name, role_target)
        # Add new organizations
        for row in added_rows:
            role_name = row.get("name","Роль")
            role_target = row.get("target","Пользователь")
            roles_db.add_role(role_name, role_target)
        # Delete organizations
        for row_id in deleted_rows:
            role_id = int(original_roles_df.iloc[int(row_id)]["id"])
            roles_db.delete_role(role_id)
    roles_container = st.container()
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
        return roles_df,column_configuration 



header_container = st.empty()
header_container.header("Роли")


roles_df,column_configuration = fill_roles_container()
original_roles_df = roles_df.copy()

op_status_container = st.empty()
col1, col2, col3 = st.columns(3)
with col1: 
    if st.button("Обновить"):
       st.rerun()
utils.setup_op_status(op_status_container,"Редактируйте Роли и нажмите Обновить")
