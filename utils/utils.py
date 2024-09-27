import streamlit as st
def auth_check():
    if st.session_state.get("password_correct", False)==False:
        st.write( "Неверный пароль. Пожалуйста, попробуйте ещё раз.")
        st.switch_page("Монитор_ЖКХ.py")
    else:
        st.write( "Пользователь "+st.session_state.get("username") +" авторизован.")  