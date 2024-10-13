import streamlit as st
try:
    import utils.datums_db as datums_db
    import utils.datum_types_db as datum_types_db
except ImportError as e:
    print("Pressed Reload in Browser...")
#conn = utils.conn_and_auth_check()

def fill_stack_item(df,row_id):
            item ={
            "parent_id" : df.iloc[row_id]["parent_id"],
            "datum_code" :df.iloc[row_id]["code"],
            "datum_name" :df.iloc[row_id]["name"],
            "fullname"  : df.iloc[row_id]["fullname"],
            "type_name"  :df.iloc[row_id]["datum_type_name"],
            "id"         :df.iloc[row_id]["id"],
            }    
            return item
def ВыборПоказателя(selected_datums_container,datum_parent_id):
    def on_select_datums_df():
        if len(st.session_state.event_datums_df.selection.rows) > 0:
            selected_row_id = st.session_state.event_datums_df.selection.rows[0] 
            selected_item = fill_stack_item(datums_df,selected_row_id)
            datumsStack = st.session_state.datumsStack
            datumsStack.push(selected_item)
            with selected_datums_container:
                if "selected_datum_button"+ str(selected_item.id) in st.session_state:
                    st.empty()
            selected_datums_button = st.button(
                label = str(selected_item.code+" "+
                            selected_item.name
                            )
                ,
                type  ='primary',
                key   = "selected_datum_button" +str(selected_item.id)
            )   
            if selected_datums_button:
                try:
                    active_id = datumsStack.peek().id
                except:
                    active_id = None
                ВыборПоказателя(selected_datums_container,active_id) 
                st.rerun()
             
        else:
            try:
                datumsStack.pop(selected_item)
                active_id = datumsStack.peek(selected_item).id
            except:
                active_id = None
            ВыборПоказателя(selected_datums_container,active_id) 

    datum_types_df = datum_types_db.get_datum_types()
    if "selected_subsystem_id" in st.session_state:
        subsystem_id = st.session_state.selected_subsystem_id
    else:
        subsystem_id = None     
    datums_df = datums_db.get_datums(subsystem_id = subsystem_id, datum_parent_id = datum_parent_id)
    if datums_df.empty:
        return

    column_configuration = {
    "id": st.column_config.NumberColumn(
        "ИД", help="ИД", width="small",disabled=True
    ),
    "parent_id": st.column_config.NumberColumn(
        "ИД datum_parent_id", help="ИД", width="small",disabled=True
    ),
    "name": st.column_config.TextColumn(
        "Наименование",
        help="Наименование",
        width="medium",
        required=True       
    ),
       "code": st.column_config.TextColumn(
        "Код",
        help="Код",
        width="small",
        required=True       
    ),
    "fullname": st.column_config.TextColumn(
        "Полное Наименование",
        help="Полное Наименование",
        width="medium",
        required=True       
    ),
    "datum_type_name": st.column_config.TextColumn(
        "Тип Показателя",
        help="Тип Показателя",
        width="small",
        required = True
    ),
    "subsystem_name": st.column_config.TextColumn(
        "Подсистема 🔽",
        help="Подсистема",
        width="small",
        required = True
    ),

    }
    try:
        active_id = str(st.session_state.datumsStack.peek().id)
    except:
        active_id = ""
    with selected_datums_container:    
        st.empty()
        event_datums_df = st.dataframe(
            datums_df, 
            column_config=column_configuration,
            use_container_width=True,
            hide_index=True,
            on_select=on_select_datums_df,
            selection_mode="single-row",
            key="event_datums_df"+active_id)

   