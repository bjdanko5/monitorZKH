import streamlit as st
try:
    import utils.datums_db as datums_db
    import utils.datum_types_db as datum_types_db
    from utils.Stack import Stack
except ImportError as e:
    print("Pressed Reload in Browser...")
#conn = utils.conn_and_auth_check()
def get_selected_datum_parent_id():
    selected_datum_parent_id = st.session_state.datumsStack.peek_id()
    return selected_datum_parent_id    
def get_selected_datum_parent_id_str():
    selected_datum_parent_id_str = st.session_state.datumsStack.peek_id_str()
    return selected_datum_parent_id_str    

def fill_stack_item(df,row_id):
            item ={
            "parent_id" : df.iloc[row_id]["parent_id"],
            "datum_code" :df.iloc[row_id]["code"],
            "datum_name" :df.iloc[row_id]["name"],
            "fullname"  : df.iloc[row_id]["fullname"],
            #"type_name"  :df.iloc[row_id]["datum_type_name"],
            "id"         :df.iloc[row_id]["id"],
            }    
            return item
def ВыборПоказателя(selected_datums_container,datum_parent_id):
    #------------------------------------------------    
    def on_select_datums_df():
        datumsStack = st.session_state.datumsStack

        active_id = datumsStack.peek_id_str()
        if len(st.session_state["event_datums_df"+active_id].selection.rows) > 0:
            
            selected_row_id = st.session_state["event_datums_df"+active_id].selection.rows[0] 

            selected_item = fill_stack_item(datums_df,selected_row_id)
            datumsStack.push(selected_item)

    #------------------------------------------------    
  
    if not "datumsStack" in st.session_state:
        st.session_state.datumsStack = Stack()

    datumsStack = st.session_state.datumsStack

    for element in datumsStack:
        with selected_datums_container:
            selected_datums_button = st.button(
                label = str(element["datum_code"]+" "+
                            element["datum_name"]
                            ),
                type  ='primary',
                key   = "selected_datum_button" +str(element["id"])
            )   
        if selected_datums_button:
            datumsStack.pop()
            st.rerun()   
    subsystem_id = st.session_state.get("selected_subsystem_id")        
    selected_datum_parent_id = get_selected_datum_parent_id()    
    datums_df = datums_db.get_datums_Выбор(subsystem_id = subsystem_id, datum_parent_id = selected_datum_parent_id)
    
    if datums_df.empty:
        if datumsStack.is_empty():
            st.write("Сначала Добавьте Вкладки в Подсистему")
            return
        else:
            datum_parent_id =datumsStack.peek_id()       
            st.write("У выбранного Показателя/Вкладки нет вложенных элементов")        
            return
    #else:                
    #    

    column_configuration = {
    "id": st.column_config.NumberColumn(
        "ИД", help="ИД", width="small",disabled=True
    ),
    "parent_id": st.column_config.NumberColumn(
        "ИД Родитель", help="ИД", width="small",disabled=True
    ),
    "name": st.column_config.TextColumn(
        "Наименование",
        help="Наименование",
        width="medium",
        required=True,
        disabled=True       
    ),
       "code": st.column_config.TextColumn(
        "Код",
        help="Код",
        width="medium",
        required=True,
        disabled=True       
    ),
    "fullname": st.column_config.TextColumn(
        "Полное Наименование",
        help="Полное Наименование",
        width="medium",
        required=True       
    ),
    }

    
    selected_datum_parent_id_str = get_selected_datum_parent_id_str()
    with selected_datums_container:    
        event_datums_df = st.dataframe(
            datums_df, 
            column_config=column_configuration,
            use_container_width=True,
            hide_index=True,
            on_select=on_select_datums_df,
            selection_mode="single-row",
            key="event_datums_df"+selected_datum_parent_id_str)

   