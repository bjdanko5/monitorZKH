import streamlit as st
def КнопкаДругойДом():
    if "selected_house_objectid" not in st.session_state:
        st.switch_page("mpages/Поиск_Дома.py")
    select_another_button = st.button(
        "Выбрать другой дом",
        type  ='secondary',
        key   = "select_another_button" 
    )   
    if select_another_button:
        del st.session_state["selected_house_objectid"]
        st.switch_page("mpages/Поиск_Дома.py")   