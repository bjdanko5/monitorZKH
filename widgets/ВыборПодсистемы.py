import streamlit as st
try:
    import utils.subsystems_db as subsystems_db
    from utils.Stack import Stack
except ImportError as e:
    print("Pressed Reload in Browser...")
#conn = utils.conn_and_auth_check()
def ВыборПодсистемы(selected_subsystem_container):
    selected_subsystem_container.subheader("Выбор Подсистемы")
    subsystems_df = subsystems_db.get_subsystems_Выбор()
    column_configuration = {
        "id": st.column_config.NumberColumn(
            "ИД", 
            help="ИД", 
            width="small"
        ),
        "name": st.column_config.TextColumn(
            "Наименование",
            help="Наименование",
            width="medium"       
        ),
   
    }
    def on_select_subsystems_df():
        selection_rows = st.session_state.event_subsystems_df.selection.rows
        if len(selection_rows) > 0:
            selected_row_id = selection_rows[0]
            
            selected_subsystem_id   = subsystems_df.iloc[selected_row_id]["id"]   
            selected_subsystem_name = subsystems_df.iloc[selected_row_id]["name"]

            datumsParentStack = st.session_state.datumsParentStack
            datumsParentStack.set_id_subsystem(selected_subsystem_id)
            datumsParentStack.set_subsystem_name(selected_subsystem_name)                        

    datumsParentStack = st.session_state.datumsParentStack
    if not datumsParentStack.get_id_subsystem():
        event_subsystems_df = st.dataframe(
        subsystems_df, 
        column_config=column_configuration,
        hide_index=True,
        on_select=on_select_subsystems_df,
        selection_mode="single-row",
        key="event_subsystems_df")
    else:    
        with selected_subsystem_container:
            if "selected_subsystem_button" in st.session_state:
                st.empty()
    
        selected_subsystem_button = st.button(
            label = st.session_state.datumsParentStack.get_subsystem_name(),
            type  ='primary',
            key   = "selected_subsystem_button"
        )   
        
        if selected_subsystem_button:
            st.session_state.datumsParentStack.set_id_subsystem(None)
            st.rerun()
