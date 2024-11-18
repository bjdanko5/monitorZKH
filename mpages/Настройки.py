import streamlit as st
try:
    import utils.utils as utils 
    import utils.subsystems_db as subsystems_db
except ImportError as e:
    print("Pressed Reload in Browser...")

conn = utils.conn_and_auth_check()
st.session_state.selected_house_objectid = 0
subsystems_df = subsystems_db.get_subsystems(subsystem_code ='settings')
st.session_state.selected_subsystem_id = int(subsystems_df['id'][0])
st.switch_page("mpages/Мониторинг.py")
