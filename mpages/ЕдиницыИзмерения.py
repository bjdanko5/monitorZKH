import streamlit as st
try:
    import utils.utils as utils
    import utils.edizms_db as edizms_db
except ImportError as e:
    print("Pressed Reload in Browser...")
conn = utils.conn_and_auth_check()
def fill_edizms_container():
    edizms_df = edizms_db.get_edizms()
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
 
    }
    def edizms_df_callback():
        ss = st.session_state["event_edizms_df"]
        edited_rows = ss["edited_rows"]
        added_rows = ss["added_rows"]
        deleted_rows = ss["deleted_rows"]
        # Обновление существующих данных
        for row_id, row in edited_rows.items():
            edizm_code = row.get("code", original_edizms_df.iloc[int(row_id)]["code"])
            edizm_code = edizm_code or "Код"
            edizm_name = row.get("name", original_edizms_df.iloc[int(row_id)]["name"])
            edizm_name = edizm_name or "Единица измерения"
 
            edizm_id = int(original_edizms_df.iloc[int(row_id)]["id"])
            edizms_db.update_edizm(edizm_id, edizm_code, edizm_name)
        # Добавление
        for row in added_rows:
            edizm_code = row.get("code","Код")
            edizm_name = row.get("name","Единица измерения")
            
            if edizm_name     != "Единица измерения": 
                if edizm_code != "Код":
                    edizms_db.add_edizm(edizm_code, edizm_name)
        added_rows.clear()        
        # Удаление
        for row_id in deleted_rows:
            edizm_id = int(original_edizms_df.iloc[int(row_id)]["id"])
            edizms_db.delete_edizm(edizm_id)
    edizms_container = st.container()
    with edizms_container:       
        event_edizms_df= st.data_editor(
                edizms_df,
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                disabled=["id"],
                num_rows="dynamic",
                on_change=edizms_df_callback,
                key="event_edizms_df"
                )
        return edizms_df,column_configuration 



header_container = st.empty()
header_container.header("Единицы измерения")

edizms_df,column_configuration = fill_edizms_container()
original_edizms_df = edizms_df.copy()

op_status_container = st.empty()
col1, col2, col3 = st.columns(3)
with col1: 
    if st.button("Обновить"):
       st.rerun()
utils.setup_op_status(op_status_container,"Редактируйте Единицы измерения и нажмите Обновить")
