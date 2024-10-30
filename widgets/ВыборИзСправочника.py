import streamlit as st
try:
    import utils.utils as utils
    import utils.options_db as options_db
    import utils.datum_types_db as datum_types_db
    import utils.datum_values_db as datum_values_db
    import utils.subsystems_db as subsystems_db
    import pprint
except ImportError as e:
    print("Pressed Reload in Browser...")
conn = utils.conn_and_auth_check()

@st.dialog("BыборИзCправочника")    
def BыборИзCправочникаПоказателей(datum_id,datum_type_id,datum_type_code,datum_code,datum_name):
    def options_df_callback():
        selection_rows =st.session_state.get("event_options_df"+str(datum_id)).selection.rows
        if len(selection_rows) > 0:        
            selected_row_id = selection_rows[0] 
            selected_item =  options_df.iloc[selected_row_id].to_dict()
            id_houses_objectid = st.session_state.get("selected_house_objectid")
            datum_values_df = datum_values_db.get_datum_value(id_houses_objectid,selected_datum_id=datum_id)
            value_field_name = options_db.get_value_field_name_for_datum_type(datum_type_code)
            for index, row in datum_values_df.iterrows():
                row[value_field_name] = selected_item[value_field_name]
                datum_values_db.merge_datum_values_values(conn,row)
        st.session_state.option_is_selected = True        
        
    #------------------------------- тело функции-------------------------------  
    if st.session_state.get("option_is_selected",False):        
        del st.session_state.option_is_selected
        st.rerun()
    options_container = st.container()
    
    with options_container:       
        st.header(f"Выбор из Справочника для {datum_code} {datum_name}")
    
    options_df = options_db.get_options(datum_id=datum_id)
    options_df['bool_value'] = options_df['int_value'].apply(lambda x: True if x == 1 else False)

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
        {    
        #"int_value": st.column_config.NumberColumn(
        #    "Значение", 
        #    help="Значение 1 / 0",
        #    width="small",
        #    disabled=True 
        #),
        "bool_value": st.column_config.CheckboxColumn(
            "Значение", 
            help="Значение Да / Нет",
            width="small",
            required=True 
       ),

       }) 

    with options_container:       

        event_options_df= st.dataframe(
            options_df,
            column_config=column_configuration,
            use_container_width=True,
            hide_index=True,
            on_select=options_df_callback,
            selection_mode="single-row",
            key="event_options_df"+str(datum_id)
            )


