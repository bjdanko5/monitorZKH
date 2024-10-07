import streamlit as st
try:
    import utils.Поиск_Дома_db as hierarhy_db
except ImportError as e:
    print("Pressed Reload in Browser...")
#conn = utils.conn_and_auth_check()
def ВыборОрганизации(selected_org_container):
    hierarhy_df = hierarhy_db.get_orgs(0,0)
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
        "id_role": st.column_config.NumberColumn(
            "ИД Роли", 
            help="ИД Роли", 
            width="small"
        ),
        "role_name": st.column_config.TextColumn(
            "Наименование Роли",
            help="Наименование Роли",
            width="medium"       
        ),
        

    }
    def on_select_hierarhy_df():
        if len(st.session_state.event_hierarhy_df.selection.rows) > 0:
            selected_row_id = st.session_state.event_hierarhy_df.selection.rows[0]
            
            selected_org_id   = hierarhy_df.iloc[selected_row_id]["id"]   
            selected_org_name = hierarhy_df.iloc[selected_row_id]["name"]
            st.session_state.selected_org_id = selected_org_id
            st.session_state.selected_org_name = selected_org_name
    if not "selected_org_id" in st.session_state:
        event_hierarhy_df = st.dataframe(
        hierarhy_df, 
        column_config=column_configuration,
        use_container_width=True,
        hide_index=True,
        on_select=on_select_hierarhy_df,
        selection_mode="single-row",
        key="event_hierarhy_df")
    else:    
        with selected_org_container:
            if "selected_org_button" in st.session_state:
                st.empty()
    
        selected_org_button = st.button(
            label = st.session_state.selected_org_name,
            type  ='primary',
            key   = "selected_org_button"
        )   
        if selected_org_button:
            del st.session_state.selected_org_id 
            del st.session_state.selected_org_name 
            st.rerun()
