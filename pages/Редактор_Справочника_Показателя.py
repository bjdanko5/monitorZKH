import streamlit as st
try:
    import utils.utils as utils
    import utils.options_db as options_db
    import utils.datum_types_db as datum_types_db
    import utils.subsystems_db as subsystems_db
    import pprint
except ImportError as e:
    print("Pressed Reload in Browser...")
conn = utils.conn_and_auth_check()
def РедакторСправочникаПоказателя(options_container):
    def options_df_callback():
  
        def update_options(edited_rows, original_options_df):
            datum_id = st.session_state.selected_spr_datum["id"]
            
            for row_id, row in edited_rows.items():
                original_row = original_options_df.iloc[int(row_id)]
                row["id_datum"]     = datum_id
                if st.session_state.selected_datum_type == "option_bool":
                    row["int_value"] = 1 if row["bool_value"] else 0
                options_db.update_option_dict(row,original_row)
        def add_options(added_rows):
            datum_id = st.session_state.selected_spr_datum["id"]
            for row in added_rows:
                row["id_datum"]     = datum_id
                if st.session_state.selected_datum_type == "option_bool":
                    row["int_value"] = 1 if row["bool_value"] else 0
                options_db.add_option_dict(row)

        def delete_options(deleted_rows):
            for row_id in deleted_rows:
                original_row = original_options_df.iloc[int(row_id)]
                option_id = int(original_row["id"])
                options_db.delete_option(option_id)
 

        ss = st.session_state["event_options_df_editor"]
       
        update_options(ss["edited_rows"], original_options_df)
        add_options(ss["added_rows"])
        delete_options(ss["deleted_rows"])

    #------------------------------- тело функции-------------------------------  
    selected_spr_datum = st.session_state.get("selected_spr_datum", None)
    if selected_spr_datum is None:
        st.switch_page("pages/Показатели.py")  

    datum_id = st.session_state.selected_spr_datum.get("id", None)
            
    with options_container:       
        st.header(f"Справочник для {st.session_state.selected_spr_datum['code']} {st.session_state.selected_spr_datum['name']}")
    datum_type_id = st.session_state.selected_spr_datum["id_datum_type"]
    

    options_df = options_db.get_options(datum_id=datum_id)
    options_df['bool_value'] = options_df['int_value'].apply(lambda x: True if x == 1 else False)

    original_options_df = options_df.copy()

    #id,id_datum,name,int_value,float_value,date_value,nvarchar_value

    column_configuration = {
    
    "id": st.column_config.NumberColumn(
        "ИД", 
        help="ИД", 
        width="small",
        disabled=True
    ),
    "name": st.column_config.TextColumn(
        "Наименование",
        help="Наименование",
        width="medium",
        required=True       
    ),
    "id_datum": None,
    "int_value": None,
    "float_value": None,
    "date_value": None,
    "nvarchar_value": None,
    "bool_value": None,
    }
    selected_datum_type = datum_types_db.get_datum_types(datum_type_id = datum_type_id)["code"][0]
    st.session_state.selected_datum_type = selected_datum_type
    if selected_datum_type == "option_int":
       column_configuration.update(
        {"int_value": st.column_config.NumberColumn(
            "Значение Целое", 
            help="Значение",
            width="medium",
       )}) 
    if selected_datum_type == "option_float":
       column_configuration.update(
        {"float_value": st.column_config.NumberColumn(
            "Значение Число", 
            help="Значение",
            width="medium",
            required=True 
       )}) 
    if selected_datum_type == "option_date":
       column_configuration.update(
        {"date_value": st.column_config.DateColumn(
            "Значение", 
            help="Значение Дата",
            width="medium",
            required=True 
       )}) 
    if selected_datum_type == "option_string":
       column_configuration.update(
        {"nvarchar_value": st.column_config.TextColumn(
            "Значение Строка", 
            help="Значение",
            width="large",
            required=True 
       )}) 
    if selected_datum_type == "option_bool":
        column_configuration.update(
        {"int_value": st.column_config.NumberColumn(
            "Значение", 
            help="Значение 1 / 0",
            width="small",
            disabled=True 
       ),
        "bool_value": st.column_config.CheckboxColumn(
            "Значение", 
            help="Значение Да / Нет",
            width="small",
            required=True 
       ),

       }) 

    with options_container:       

        event_options_df= st.data_editor(
            options_df,
            column_config=column_configuration,
            use_container_width=True,
            hide_index=True,
            disabled=["id"],
            num_rows="dynamic",
            on_change=options_df_callback,
            key="event_options_df_editor"
            )
#Основная программа
conn = utils.conn_and_auth_check() 

options_container = st.container()
РедакторСправочникаПоказателя(options_container)
 
