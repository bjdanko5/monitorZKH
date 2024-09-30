import streamlit as st
import pandas as pd
import pyodbc
import time
import utils.utils as utils
def exit_user():
    if "password_correct" in st.session_state or "username" in st.session_state:
        del st.session_state.password_correct
        del st.session_state.username
        st.switch_page("Монитор_ЖКХ.py")

def alltrim(s):
    return s.strip()
def no_auth_menu():
    st.sidebar.page_link("Монитор_ЖКХ.py", label="Вход в Монитор ЖКХ")
    st.sidebar.page_link("pages/0_👈_Выход.py", label="Выход")
def auth_menu():
    if "username" not in st.session_state or "password_correct" not in st.session_state:
        return
    st.sidebar.page_link("pages/1_🔍_Поиск_Дома.py", label="Поиск дома")
    st.sidebar.page_link("pages/2_🦳_Пользователи.py", label="Пользователи",disabled=st.session_state.username != "adm",)
    st.sidebar.page_link("pages/3_🏢_Организации.py", label="Организации",disabled=st.session_state.username != "adm",)
    with st.sidebar:
        info_success = st.empty()
        info_success.success("Пользователь "+ st.session_state.username +" авторизован")
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
    no_auth_menu()
    if "username" not in st.session_state or "password_correct" not in st.session_state:
        st.write( "Пользователь не авторизован.")  
        st.switch_page("Монитор_ЖКХ.py") 
    else:      
       st.session_state["password_correct"] =  st.session_state["password_correct"]
       st.session_state["username"] =  st.session_state["username"] 
       
    if st.session_state.get("password_correct", False)==False:
        st.write( "Неверный пароль. Пожалуйста, попробуйте ещё раз.")
        st.switch_page("Монитор_ЖКХ.py")
    else:
        if st.session_state.get("username")==None:
            st.write( "Пользователь не авторизован.")
            st.switch_page("Монитор_ЖКХ.py")
        else:   
            #st.write( "Пользователь "+st.session_state.get("username") +" авторизован.")
            auth_menu()  
def get_conn_status():
    if "conn" in st.session_state and st.session_state["conn"] is not None:
        conn = st.session_state["conn"]
        st.session_state["conn"] =conn
        return conn 
    with st.status("Устанавливается подключение к базе данных...", state="running", expanded=True) as status:
        st.write("Ожидайте...")
        st.session_state["conn"] = utils.init_connection()
        if st.session_state.get("conn") is None:
            del st.session_state["password_correct"]
            status.update(label="Не удалось подключиться к базе данных.",state="error", expanded=True)
            st.write("Выполнен Выход пользователя из Монитора ЖКХ.")   
            if st.button("Войти ещё раз"):
                st.switch_page("Монитор_ЖКХ.py") 
            st.stop()   
        else:        
            conn = st.session_state["conn"]
            st.session_state["conn"] =conn
            status.update(label="Подключение к базе данных выполнено.",state="complete", expanded=True)   
            st.write("Можно работать...")
    #time.sleep (5)       
    status.update(label="БД подключена",state="complete", expanded=False)
    return conn                