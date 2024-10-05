import streamlit as st
import pandas as pd
try:
    import utils.utils as utils
    import utils.orgs_db as orgs_db
    import utils.roles_db as roles_db
except ImportError as e:
    print("Pressed Reload in Browser...")

conn = utils.conn_and_auth_check()
def fill_roles_df():
    roles_df = roles_db.get_roles('Организация')
    return roles_df
def fill_orgs_container():
    orgs_df = orgs_db.get_orgs()
    roles_df = fill_roles_df()
    column_configuration = {
    "id": st.column_config.NumberColumn(
        "ИД", help="ИД", width="small"
    ),
    "name": st.column_config.TextColumn(
        "Наименование",
        help="Наименование",
        width="medium"       
    ),
    "id_role": st.column_config.NumberColumn(
        "ИД Роли",
        help="ИД Роли",
        width="small"   
    ),   
    "role_name": st.column_config.SelectboxColumn(
        "Роль 🔽",
        options=roles_df["name"].tolist(),    
        help="Роль",
        width="small",
        required = True
    ),
    }
    def orgs_df_callback():
        def get_id_role_by_role_name(role_name):
            return int(roles_df.loc[roles_df['name'] == role_name, 'id'].iloc[0])
        #это заглушка на будущее
        ss = st.session_state["event_orgs_df"]
        edited_rows = ss["edited_rows"]
        added_rows = ss["added_rows"]
        deleted_rows = ss["deleted_rows"]
        # Обновление существующих данных
        for row_id, row in edited_rows.items():
            org_name = row.get("name", original_orgs_df.iloc[int(row_id)]["name"])
            role_name = row.get("role_name", original_orgs_df.iloc[int(row_id)]["role_name"])
            id_role = get_id_role_by_role_name(role_name)
            org_id = int(original_orgs_df.iloc[int(row_id)]["id"])
            orgs_db.update_org(org_id, org_name, id_role)
        # Add new organizations
        for row in added_rows:
            org_name = row.get("name","Организация")
            role_name = row.get("role_name","Роль")
            id_role = get_id_role_by_role_name(role_name)
            orgs_db.add_org(org_name, id_role)
        # Delete organizations
        for row_id in deleted_rows:
            org_id = int(original_orgs_df.iloc[int(row_id)]["id"])
            orgs_db.delete_org(org_id)
 
    orgs_container = st.container()
    with orgs_container:       
        event_orgs_df= st.data_editor(
            orgs_df,
            column_config=column_configuration,
            use_container_width=True,
            hide_index=True,
            disabled=["id"],
            num_rows="dynamic",
            on_change=orgs_df_callback,
            key="event_orgs_df"
            )

    return orgs_df,column_configuration 

#Основная программа страницы
header_container = st.empty()
header_container.header("Организации")


roles_df = fill_roles_df()
orgs_df,column_configuration = fill_orgs_container()
original_orgs_df = orgs_df.copy()

op_status_container = st.empty()
col1, col2, col3 = st.columns(3)
with col1: 
    if st.button("Обновить"):
       st.rerun() 
utils.setup_op_status(op_status_container,"Редактируйте Организации и нажмите Обновить")
