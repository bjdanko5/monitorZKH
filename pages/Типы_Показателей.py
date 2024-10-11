import streamlit as st
try:
    import utils.utils as utils
    import utils.datum_types_db as datum_types_db
except ImportError as e:
    print("Pressed Reload in Browser...")
conn = utils.conn_and_auth_check()
def fill_datum_types_container():
    datum_types_df = datum_types_db.get_datum_types()
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
    def datum_types_df_callback():
        ss = st.session_state["event_datum_types_df"]
        edited_rows = ss["edited_rows"]
        added_rows = ss["added_rows"]
        deleted_rows = ss["deleted_rows"]
        # Обновление существующих данных
        for row_id, row in edited_rows.items():
            datum_type_code = row.get("code", original_datum_types_df.iloc[int(row_id)]["code"])
            datum_type_code = datum_type_code or "Код"
            datum_type_name = row.get("name", original_datum_types_df.iloc[int(row_id)]["name"])
            datum_type_name = datum_type_name or "Тип показателя"
 
            datum_type_id = int(original_datum_types_df.iloc[int(row_id)]["id"])
            datum_types_db.update_datum_type(datum_type_id, datum_type_code, datum_type_name)
        # Добавление
        for row in added_rows:
            datum_type_code = row.get("code","Код")
            datum_type_name = row.get("name","Тип показателя")
            
            if datum_type_name     != "Тип показателя": 
                if datum_type_code != "Код":
                    
                    datum_types_db.add_datum_type(datum_type_code, datum_type_name)
        added_rows.clear()        
        # Удаление
        for row_id in deleted_rows:
            datum_type_id = int(original_datum_types_df.iloc[int(row_id)]["id"])
            datum_types_db.delete_datum_type(datum_type_id)
    datum_types_container = st.container()
    with datum_types_container:       
        event_datum_types_df= st.data_editor(
                datum_types_df,
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                disabled=["id"],
                num_rows="dynamic",
                on_change=datum_types_df_callback,
                key="event_datum_types_df"
                )
        return datum_types_df,column_configuration 



header_container = st.empty()
header_container.header("Типы Показателей")

datum_types_df,column_configuration = fill_datum_types_container()
original_datum_types_df = datum_types_df.copy()

op_status_container = st.empty()
col1, col2, col3 = st.columns(3)
with col1: 
    if st.button("Обновить"):
       st.rerun()
utils.setup_op_status(op_status_container,"Редактируйте Типы Показателей и нажмите Обновить")
