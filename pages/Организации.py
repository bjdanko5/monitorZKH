import streamlit as st
import pandas as pd
import utils.utils as utils
import utils.orgs_db as orgs_db
import utils.roles_db as roles_db
conn = utils.conn_and_auth_check()
def fill_roles_df():
    roles_df = roles_db.get_roles('org')
def fill_orgs_container():
    orgs_df = orgs_db.get_orgs()
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
            "Роль",
            help="Роль",
            width="small"       
        ),

    }
    return orgs_df,column_configuration 


def orgs_df_callback():
    #это заглушка на будущее
    ss =  st.session_state["event_orgs_df"]

header_container = st.empty()
header_container.header("Организации")

orgs_container = st.container()
orgs_df,column_configuration = fill_orgs_container()
original_orgs_df = orgs_df.copy()

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
  
op_status_container = st.empty()
col1, col2, col3 = st.columns(3)
with col1: 
    if st.button("Записать"):
        if "event_orgs_df" in st.session_state:
            st.session_state["event_orgs_df"]
            edited_rows = st.session_state["event_orgs_df"]["edited_rows"]
            added_rows = st.session_state["event_orgs_df"]["added_rows"]
            deleted_rows = st.session_state["event_orgs_df"]["deleted_rows"]
            # Update existing organizations
            if len(edited_rows)> 0 or len(added_rows) > 0 or len(deleted_rows) >0:
                for row_id, row in edited_rows.items():
                    org_name = row["name"]
                    id_role  = row["id_role"]
                    org_id = int(original_orgs_df.iloc[int(row_id)]["id"])
                    orgs_db.update_org(org_id, org_name,id_role)
                # Add new organizations
                for row in added_rows:
                    org_name = row["name"]
                    id_role  = row["id_role"]
                    orgs_db.add_org(org_name,id_role)
                # Delete organizations
                for row_id in deleted_rows:
                    org_id = int(original_orgs_df.iloc[int(row_id)]["id"])
                    orgs_db.delete_org(org_id)
            else:
                utils.show_op_status(op_status_container,"Ничего не отредактировано")       

utils.setup_op_status(op_status_container,"Редактируйте Организации и нажмите Записать")
