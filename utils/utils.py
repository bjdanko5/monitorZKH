import streamlit as st
import pandas as pd
import pyodbc
def alltrim(s):
    return s.strip()
def init_connection():
    try:
        connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=" + st.secrets["server"] + ";"
            "DATABASE=" + st.secrets["database"] + ";"
            "UID=" + st.secrets["username"] + ";"
            "PWD=" + st.secrets["password"]
        )
        conn = pyodbc.connect(connection_string, timeout=5)
        return conn
    except pyodbc.OperationalError as e:
        # Handle the OperationalError exception
        error_message = str(e)
        print(f"Ошибка подключения: {error_message}")
        # You can add additional error handling code here, such as logging or retrying the connection
        return None
#@st.cache_data(ttl=600)

def run_query(query, params=None):
    conn = st.session_state["conn"]
    if conn is None:
        return None  # or raise an exception, or handle the error in some other way
    
    with conn.cursor() as cur:
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        return cur.fetchall()
def auth_check():
    if st.session_state.get("password_correct", False)==False:
        st.write( "Неверный пароль. Пожалуйста, попробуйте ещё раз.")
        st.switch_page("Монитор_ЖКХ.py")
    else:
        if st.session_state.get("username")==None:
            st.write( "Пользователь не авторизован.")
            st.switch_page("Монитор_ЖКХ.py")
        else:   
            st.write( "Пользователь "+st.session_state.get("username") +" авторизован.")  