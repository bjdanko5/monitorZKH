import streamlit as st
try:
    import utils.datums_db as datums_db
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
            selected_item = datums_df.iloc[selected_row_id].to_dict()
            datumsParentStack.push(selected_item)
    #------------------------------------------------    
    selected_datums_container.subheader("Выбор Вкладки / Показателя")

    datumsParentStack            = st.session_state.datumsParentStack
    selected_subsystem_id        = datumsParentStack.get_id_subsystem()
    selected_datum_parent_id     = datumsParentStack.peek_id()
    selected_datum_parent_id_str = datumsParentStack.peek_id_str()
    with selected_datums_container:
        if not datumsParentStack.is_empty():
            cols = st.columns(len(datumsParentStack))

            for i, element in enumerate(datumsParentStack):
                with cols[i]:
                    selected_datums_button = st.button(
                        label=str(element["code"]+" "+element["name"]),
                        type='primary',
                        key="selected_datum_button" + str(element["id"])
                    )
                    if selected_datums_button:
                        datumsParentStack.pop()
                        st.rerun()
        """
        for element in datumsParentStack:
            with selected_datums_container:
                selected_datums_button = st.button(
                    label = str(element["code"]+" "+element["name"]),
                    type  ='primary',
                    key   = "selected_datum_button" +str(element["id"])
                )   
            if selected_datums_button:
                datumsParentStack.pop()
                st.rerun()   
        """          
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
        if st.session_state.datumsParentStack.get_id_subsystem():
            st.subheader("Вкладки / Показатели Подсистемы " + st.session_state.datumsParentStack.get_subsystem_name())
        else:    
            st.subheader("Все Вкладки / Показатели")           
    else:
        if st.session_state.datumsParentStack.get_id_subsystem():    
            st.subheader("Подсистема " +  st.session_state.datumsParentStack.get_subsystem_name()+" Показатели" +" в " + st.session_state.datumsParentStack.peek()["name"])
        else:    
            st.subheader("Подсистема не выбрана Показатели " +" в " + st.session_state.datumsParentStack.peek()["name"])
            
        