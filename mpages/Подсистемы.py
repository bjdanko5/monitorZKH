import streamlit as st
try:
    import utils.utils as utils
    import utils.subsystems_db as subsystems_db
except ImportError as e:
    print("Pressed Reload in Browser...")
conn = utils.conn_and_auth_check()
def fill_subsystems_container():
    subsystems_df = subsystems_db.get_subsystems()
    column_configuration = {
        "id": st.column_config.NumberColumn(
            "ИД", help="ИД", width="small",disabled=True
        ),
        "code": st.column_config.TextColumn(
            "Код",
            help="Код",
            width="medium",
            required = True
        ),
        "name": st.column_config.TextColumn(
            "Наименование",
            help="Наименование",
            width="medium", 
            required = True                  
        ),
        "page": st.column_config.TextColumn(
            "Страница",
            help="",
            width="medium"                   
        ),

    }
    def subsystems_df_callback():
        ss = st.session_state["event_subsystems_df"]
        edited_rows = ss["edited_rows"]
        added_rows = ss["added_rows"]
        deleted_rows = ss["deleted_rows"]
        # Обновление существующих данных
        for row_id, row in edited_rows.items():
            subsystem_code = row.get("code", original_subsystems_df.iloc[int(row_id)]["code"])
            subsystem_code = subsystem_code or "Код"
            subsystem_name = row.get("name", original_subsystems_df.iloc[int(row_id)]["name"])
            subsystem_name = subsystem_name or "Подсистема"
            subsystem_page = row.get("page", original_subsystems_df.iloc[int(row_id)]["page"])
            subsystem_page = subsystem_page or "mpages/"+subsystem_code+".py"
            subsystem_id = int(original_subsystems_df.iloc[int(row_id)]["id"])
            subsystems_db.update_subsystem(subsystem_id, subsystem_code, subsystem_name,subsystem_page)
        # Добавление
        for row in added_rows:
            subsystem_code = row.get("code","Код")
            subsystem_name = row.get("name","Подсистема")
            subsystem_page = row.get("page","Страница")
            if subsystem_name     != "Подсистема": 
                if subsystem_code != "Код":
                    subsystem_page = "mpages/"+subsystem_code+".py"
                    subsystems_db.add_subsystem(subsystem_code, subsystem_name,subsystem_page)
        added_rows.clear()        
        # Удаление
        for row_id in deleted_rows:
            subsystem_id = int(original_subsystems_df.iloc[int(row_id)]["id"])
            subsystems_db.delete_subsystem(subsystem_id)
    subsystems_container = st.container()
    with subsystems_container:       
        event_subsystems_df= st.data_editor(
                subsystems_df,
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                disabled=["id"],
                num_rows="dynamic",
                on_change=subsystems_df_callback,
                key="event_subsystems_df"
                )
        return subsystems_df,column_configuration 



header_container = st.empty()
header_container.header("Подсистемы")

subsystems_df,column_configuration = fill_subsystems_container()
original_subsystems_df = subsystems_df.copy()

op_status_container = st.empty()
col1, col2, col3 = st.columns(3)
with col1: 
    if st.button("Обновить"):
       st.rerun()
utils.setup_op_status(op_status_container,"Редактируйте Подсистемы и нажмите Обновить")
