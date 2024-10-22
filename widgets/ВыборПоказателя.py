import streamlit as st
try:
    import utils.datums_db as datums_db
    import utils.datum_types_db as datum_types_db
    import utils.Stack as Stack
    #from utils.Stack import Stack
    #from utils.Stack import DatumsParentStack
except ImportError as e:
    print("Pressed Reload in Browser...")
#conn = utils.conn_and_auth_check()
 
def ВыборПоказателя(selected_datums_container,datum_parent_id):
    #------------------------------------------------    
    def on_select_datums_df():
        datumsParentStack = st.session_state.datumsParentStack
        event_datums_df_ID = "event_datums_df" + datumsParentStack.peek_id_str()
        selection_rows = st.session_state[event_datums_df_ID].selection.rows
        if len(selection_rows) > 0:
            
            selected_row_id = selection_rows[0] 
            selected_item = datums_df.iloc[selected_row_id].to_dict()#fill_stack_item(datums_df,selected_row_id)
            datumsParentStack.push(selected_item)
    #------------------------------------------------    
    selected_datums_container.subheader("Выбор Вкладки / Показателя для отбора Показателей")

   # selected_subsystem_id = st.session_state.get("selected_subsystem_id") 
   # if not st.session_state.get("datumsParentStack"):
   #     st.session_state.datumsParentStack = Stack.DatumsParentStack()
    datumsParentStack = st.session_state.datumsParentStack
   # datumsParentStack.set_id_subsystem(selected_subsystem_id)
    selected_subsystem_id = datumsParentStack.get_id_subsystem()
    
    selected_datum_parent_id     = datumsParentStack.peek_id()
    selected_datum_parent_id_str = datumsParentStack.peek_id_str()

    for element in datumsParentStack:
        with selected_datums_container:
            selected_datums_button = st.button(
                label = str(element["code"]+" "+
                            element["name"]
                            ),
                type  ='primary',
                key   = "selected_datum_button" +str(element["id"])
            )   
        if selected_datums_button:
            datumsParentStack.pop()
            st.rerun()   
       
    
    datums_df = datums_db.get_datums_Выбор(subsystem_id = selected_subsystem_id, datum_parent_id = selected_datum_parent_id)
    if not datums_df.empty:
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
    
        with selected_datums_container:    
            event_datums_df = st.dataframe(
                datums_df, 
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                on_select=on_select_datums_df,
                selection_mode="single-row",
                key="event_datums_df"+selected_datum_parent_id_str)
        
    if datums_df.empty:
        if datumsParentStack.is_empty():
            st.write("Сначала Добавьте Вкладки в Подсистему")
        else:
            st.write("У выбранного Показателя/Вкладки нет вложенных элементов")        
        
    if st.session_state.datumsParentStack.is_empty():

        if "selected_subsystem_id" in st.session_state:
            st.subheader("Вкладки / Показатели Подсистемы " + str(st.session_state.selected_subsystem_name))
        else:    
            st.subheader("Вкладки Подсистемы не выбраны")
            
    else:
        if "selected_subsystem_id" in st.session_state:
            st.subheader("Подсистема " + str(st.session_state.selected_subsystem_name)+"Показатели" +" в " + str(st.session_state.datumsParentStack.peek()["name"]))
        else:    
            st.subheader("Подсистема не выбрана Показатели " +" в " + str(st.session_state.datumsParentStack.peek()["name"]))
            
        