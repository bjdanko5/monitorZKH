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
            """"
            item ={
            "parent_id" : df.iloc[row_id]["parent_id"],
            "datum_code" :df.iloc[row_id]["code"],
            "datum_name" :df.iloc[row_id]["name"],
            "fullname"  : df.iloc[row_id]["fullname"],
            "id_subsystem" :df.iloc[row_id]["id_subsystem"],
            #"type_name"  :df.iloc[row_id]["datum_type_name"],
            "id"         :df.iloc[row_id]["id"],
            }   
            """
            item = df.iloc[row_id].to_dict()
            return item
def ВыборПоказателя(selected_datums_container,datum_parent_id):
    #------------------------------------------------    
    def on_select_datums_df():
        datumsStack = st.session_state.datumsStack
        selected_datum_parent_id_str = datumsStack.peek_id_str()

        if len(st.session_state["event_datums_df"+selected_datum_parent_id_str].selection.rows) > 0:
            
            selected_row_id = st.session_state["event_datums_df"+selected_datum_parent_id_str].selection.rows[0] 

            selected_item = fill_stack_item(datums_df,selected_row_id)
            datumsStack.push(selected_item)
            st.session_state.datumsStack.items = datumsStack.items 
    #------------------------------------------------    
  
    if not "datumsStack" in st.session_state:
        st.session_state.datumsStack = Stack()

    datumsStack = st.session_state.datumsStack
    selected_subsystem_id = st.session_state.get("selected_subsystem_id") 
    datumsStack.clear_not_in_subsystem(selected_subsystem_id)
    for element in datumsStack:
        with selected_datums_container:
            selected_datums_button = st.button(
                #label = str(element["datum_code"]+" "+
                #            element["datum_name"]
                #            ),
                label = str(element["code"]+" "+
                            element["name"]
                            ),
            
                type  ='primary',
                key   = "selected_datum_button" +str(element["id"])
            )   
        if selected_datums_button:
            datumsStack.pop()
            st.session_state.datumsStack = datumsStack 
            st.rerun()   

           
    selected_datum_parent_id = get_selected_datum_parent_id()    
    datums_df = datums_db.get_datums_Выбор(subsystem_id = selected_subsystem_id, datum_parent_id = selected_datum_parent_id)
    
    if datums_df.empty:
        if datumsStack.is_empty():
            st.write("Сначала Добавьте Вкладки в Подсистему")
        else:
            st.write("У выбранного Показателя/Вкладки нет вложенных элементов")        
        return
  
    column_configuration = {
    "id": st.column_config.NumberColumn(
        "ИД", help="ИД", width="small",disabled=True
    ),
    "parent_id": st.column_config.NumberColumn(
        "ИД Родитель", help="ИД", width="small",disabled=True
    ),       
    "id_subsystem": st.column_config.NumberColumn(
        "ИД Подсистемы", help="ИД Подсистемы", width="small",disabled=True
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

   