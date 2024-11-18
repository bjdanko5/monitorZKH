import streamlit as st
try:
    import utils.utils as utils
    import widgets.КнопкаДругойДом as КнопкаДругойДом
    import utils.Поиск_Дома_db as hierarchy_db
except ImportError as e:
    print("Pressed Reload in Browser...")
def ЗаголовокПодсистемы():
    if "selected_house_objectid" not in st.session_state:
        st.switch_page("mpages/Поиск_Дома.py")
    if st.session_state.selected_house_objectid != 0:
        col1, col2 = st.columns([1, 5])
        with col1:
            КнопкаДругойДом.КнопкаДругойДом()
        with col2:
            
            house_df = hierarchy_db.get_house(st.session_state["selected_house_objectid"])
            st.subheader(hierarchy_db.format_address(house_df))
        utils.subsystem_menu(without_settings = True)
    else:
        subsystem_id = st.session_state.get("selected_subsystem_id",None) 
        if subsystem_id == None:
            if st.session_state.selected_house_objectid == 0:
               del st.session_state.selected_house_objectid
               st.switch_page("mpages/Поиск_Дома.py")        

        utils.subsystem_menu(subsystem_id = subsystem_id)       
        
        