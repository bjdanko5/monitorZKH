import streamlit as st
import pandas as pd
try:
    import utils.utils as utils
    import utils.users_db as users_db
    import utils.roles_db as roles_db
    import utils.orgs_db as orgs_db
    import widgets.ВыборОрганизации as so
except ImportError as e:
    print("Pressed Reload in Browser...")
conn = utils.conn_and_auth_check()
def fill_roles_df():
    roles_df = roles_db.get_roles('Пользователь')
    return roles_df
def fill_orgs_df():
    orgs_df = orgs_db.get_orgs()
    return orgs_df
def fill_users_container():  
    orgs_df = orgs_db.get_orgs()
    if "selected_org_id" in st.session_state:
        users_df = users_db.get_users_by_org_id(st.session_state.selected_org_id)
    else:      
        users_df = users_db.get_users()
    roles_df = fill_roles_df()
    column_configuration = {
    "id": st.column_config.NumberColumn(
        "ИД", help="ИД", width="small",disabled=True
    ),
    "name": st.column_config.TextColumn(
        "Наименование",
        help="Наименование",
        width="medium",
        required=True       
    ),
    "fullname": st.column_config.TextColumn(
        "Полное Наименование",
        help="Полное Наименование",
        width="medium",
        required=True       
    ),

        "password": st.column_config.TextColumn(
        "Пароль",
        help="Пароль",
        width="small"      
    ),
    "role_id": st.column_config.NumberColumn(
        "ИД Роли",
        help="ИД Роли",
        width="small",
        required = True,
        disabled=True   
    ),   
    "role_name": st.column_config.SelectboxColumn(
        "Роль 🔽",
        options=roles_df["name"].tolist(),    
        help="Роль",
        width="small",
        required = True
    ),
    "org_id": st.column_config.NumberColumn(
        "ИД Организации",
        help="ИД Организации",
        width="small",
        disabled=True   
    ),   
    "org_name": st.column_config.SelectboxColumn(
        "Организация 🔽",
        options=orgs_df["name"].tolist(),    
        help="Организация",
        width="small",
        required = True
    ),

    }
    def users_df_callback():
        def get_id_role_by_role_name(role_name):
            return int(roles_df.loc[roles_df['name'] == role_name, 'id'].iloc[0])
        def get_id_org_by_org_name(org_name):
            return int(orgs_df.loc[orgs_df['name'] == org_name, 'id'].iloc[0])

        #это заглушка на будущее
        ss = st.session_state["event_users_df"]
        edited_rows = ss["edited_rows"]
        added_rows = ss["added_rows"]
        deleted_rows = ss["deleted_rows"]
        # Обновление существующих данных
        for row_id, row in edited_rows.items():
            user_name = row.get("name", original_users_df.iloc[int(row_id)]["name"])
            password = row.get("password", original_users_df.iloc[int(row_id)]["password"])
            user_fullname = row.get("fullname", original_users_df.iloc[int(row_id)]["fullname"])
            role_name = row.get("role_name", original_users_df.iloc[int(row_id)]["role_name"])
            org_name = row.get("org_name", original_users_df.iloc[int(row_id)]["org_name"])
            id_role = get_id_role_by_role_name(role_name)
            id_org = get_id_org_by_org_name(org_name)
            user_id = int(original_users_df.iloc[int(row_id)]["id"])
            users_db.update_user(user_id, user_name,user_fullname, password, id_role,id_org)
        # Add new useranizations
        for row in added_rows:
            user_name = row.get("name", "Пользователь")
            user_fullname = row.get("name", "Полное Имя")
            password = row.get("password","Пароль" )
            role_name = row.get("role_name", "Пользователь")
            org_name = row.get("org_name", "Организация")
            id_role = get_id_role_by_role_name(role_name)
            id_org = get_id_org_by_org_name(org_name)
            users_db.add_user( user_name,user_fullname, password, id_role,id_org)
        # Delete useranizations
        for row_id in deleted_rows:
            user_id = int(original_users_df.iloc[int(row_id)]["id"])
            users_db.delete_user(user_id)
 
    users_container = st.container()
    with users_container:       
        event_users_df= st.data_editor(
            users_df,
            column_config=column_configuration,
            use_container_width=True,
            hide_index=True,
            disabled=["id"],
            num_rows="dynamic",
            on_change=users_df_callback,
            key="event_users_df"
            )

    return users_df,column_configuration 

#Основная программа страницы

header_container = st.empty()
header_container.header("Пользователи")

so_container = st.container()
so.ВыборОрганизации(so_container)
st.subheader("Редактирование Пользователей")
orgs_df = fill_orgs_df()
roles_df = fill_roles_df()
users_df,column_configuration = fill_users_container()
original_users_df = users_df.copy()
op_status_container = st.empty()
col1, col2, col3 = st.columns(3)
with col1: 
    if st.button("Обновить"):
       st.rerun() 
utils.setup_op_status(op_status_container,"Редактируйте Пользователи и нажмите Обновить")
