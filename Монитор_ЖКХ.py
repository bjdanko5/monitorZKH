import streamlit as st
import pandas as pd
import pyodbc
import utils.utils as utils
import hmac

def no_auth_menu():
    st.sidebar.page_link("Монитор_ЖКХ.py", label="Вход в Монитор ЖКХ")

def auth_menu():
    if "username" not in st.session_state or "password_correct" not in st.session_state:
        return
    st.sidebar.page_link("pages/1_🔍_Поиск_Дома.py", label="Поиск дома")
    st.sidebar.page_link("pages/2_🦳_Пользователи.py", label="Пользователи",disabled=st.session_state.username != "adm",)
    st.sidebar.page_link("pages/3_🏢_Организации.py", label="Организации",disabled=st.session_state.username != "adm",)

no_auth_menu()

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
    if st.session_state.get("password_correct", False) and "username" in st.session_state:
        return True

    # Show inputs for username + password.
    login_form()
    if not"password_correct" in st.session_state:
        st.error("😕 Пользователь не зарегистрирован или пароль неверен")
    return False


if not check_password():
    st.stop()
  
# Main Streamlit app starts here
st.write("👋Успешный вход в монитор ЖКХ...")
auth_menu()
#st.button("Далее")
#st.sidebar.success("Выберите режим мониторинга.")
#st.switch_page("pages/1_🔍_Поиск_Дома.py")