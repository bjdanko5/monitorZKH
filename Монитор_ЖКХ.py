import streamlit as st
import pandas as pd
import pyodbc
import hmac
def auth_check():
    if st.session_state.get("password_correct", False)==False:
        st.write( "Неверный пароль. Пожалуйста, попробуйте ещё раз.")
        st.switch_page("Монитор_ЖКХ.py")
    else:
        st.write( "Пользователь "+st.session_state.get("username") +" авторизован.")         

def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Пользователь", key="username")
            st.text_input("Пароль", type="password", key="password")
            st.form_submit_button("Войти", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            #del st.session_state["username"]
            st.session_state["username"] =  st.session_state["username"]
    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 Пользователь не зарегистрирован или пароль неверен")
    return False


if not check_password():
    st.stop()

# Main Streamlit app starts here
st.write("👋Успешный вход в монитор ЖКХ...")
st.button("Далее")
st.sidebar.success("Выберите режим мониторинга.")
