import streamlit as st
try:
    import utils.orgs_db as orgs_db
except ImportError as e:
    print("Pressed Reload in Browser...")
#conn = utils.conn_and_auth_check()
def ВыборОрганизации(selected_org_container):
    orgs_df = orgs_db.get_all_orgs()
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
    def on_select_orgs_df():
        selected_org_id   = st.session_state.event_orgs_df.selection.rows[0]["id"]   
        selected_org_name = st.session_state.event_orgs_df.selection.rows[0]["name"]   
        st.session_state.selected_org_id = selected_org_id
        st.session_state.selected_org_name = selected_org_name
    with selected_org_container:
        st.subheader("Выберите Организацию")
        if st.session_state.selected_org_id:
            event_orgs_df = st.dataframe(
                orgs_df, 
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                on_select=on_select_orgs_df,
                selection_mode="single-row",
                key="event_orgs_df")
        else:
            selected_org_button = st.button(
                label = st.session_state.selected_org_name,
                type  ='primary',
                key   = "selected_org_button"
            )   
            if selected_org_button:
               del st.session_state.selected_org_id 
               del st.session_state.selected_org_name 
               st.rerun()
 
  
