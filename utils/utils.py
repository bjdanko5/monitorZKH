import streamlit as st
import pandas as pd
import pyodbc
import time
import sqlalchemy
def setup_op_status(op_status_container,first_visit_status="Готово"):
    if first_visit_op_status():
        show_op_status(op_status_container,first_visit_status)
    else:
        if "op_status_queued" in st.session_state:
            show_op_status(op_status_container,st.session_state.op_status_queued,st.session_state.op_status_queued_type)
            del st.session_state.op_status_queued
            del st.session_state.op_status_queued_type

def queue_op_status(op_status,status_type="info"):
    st.session_state.op_status_queued = op_status
    st.session_state.op_status_queued_type = status_type
def show_op_status(op_status_container,op_status,status_type="info"):
    if status_type == "success":
        with op_status_container:
            st.info(op_status,icon=":material/thumb_up:")        

    if status_type == "error":
        with op_status_container:
            st.info(op_status,icon=":material/error:")        
   
    if status_type == "info":
        with op_status_container:
            st.info(op_status,icon=":material/help:")        
def first_visit_op_status():
    if 'first_visit' not in st.session_state:
        st.session_state.first_visit = True
        return st.session_state.first_visit
    else:
        st.session_state.first_visit = False
    return st.session_state.first_visit
def exit_user():
    if "password_correct" in st.session_state or "username" in st.session_state:
        del st.session_state.password_correct
        del st.session_state.username
        st.switch_page("pages/Вход.py")
        

def alltrim(s):
    return s.strip()
def menu():
    conn = get_conn_status()
    pages = {
    "Монитор ЖКХ": [
        st.Page("pages/Вход.py", title="Вход", icon = ":material/login:"),   
        st.Page("pages/Выход.py", title="Выход", icon = ":material/logout:")
    ],
    }
    user_pages = {
    "Пользователям": [
        st.Page("pages/Поиск_Дома.py", title="Поиск дома", icon = ":material/search:"),   
    ],
    }
    adm_pages = {
    "Администраторам": [
        st.Page("pages/Пользователи.py", title="Пользователи", icon = ":material/group:"),   
        st.Page("pages/Организации.py", title="Организации", icon = ":material/source_environment:"),   
        st.Page("pages/Роли.py", title="Роли", icon = ":material/guardian:"),   
    ],
    }
    adm_pages.update(user_pages)
    role_pages = {
        "adm": adm_pages,
        "user": user_pages
    }
    info = st.sidebar.empty()
    if st.session_state.get("password_correct", False) and"username" in st.session_state:
        pages.update(role_pages.get(st.session_state.username, {}))
        info.success("Пользователь "+ st.session_state.username +" авторизован", icon=":material/thumb_up:")
    else:
        info.error("Пользователь не авторизован", icon=":material/error:")
        
    
    pg = st.navigation(pages)
    pg.run()
    return pg

    #st.sidebar.page_link("pages/Поиск_Дома.py", label="Поиск дома",icon = ":material/search:")
    #st.sidebar.page_link("pages/Пользователи.py", label="Пользователи",disabled=st.session_state.username != "adm",icon = ":material/group:")
    #st.sidebar.page_link("pages/Организации.py", label="Организации",disabled=st.session_state.username != "adm",icon = ":material/source_environment:")

   
def init_connection1():
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
def init_connection():    
    from sqlalchemy.engine import URL
    connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=" + st.secrets["server"] + ";"
            "DATABASE=" + st.secrets["database"] + ";"
            "UID=" + st.secrets["username"] + ";"
            "PWD=" + st.secrets["password"]
        )
    #connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=dagger;DATABASE=test;UID=user;PWD=password"
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
    from sqlalchemy import create_engine
    engine = create_engine(connection_url)
    conn = engine.connect()
    return conn
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
    #pg = no_auth_menu()
    if "username" not in st.session_state or "password_correct" not in st.session_state:
        st.write( "Пользователь не авторизован.")  
        st.switch_page("pages/Вход.py")
        
    else:      
       st.session_state["password_correct"] =  st.session_state["password_correct"]
       st.session_state["username"] =  st.session_state["username"] 
       
    if st.session_state.get("password_correct", False)==False:
        st.write( "Неверный пароль. Пожалуйста, попробуйте ещё раз.")
        st.switch_page("pages/Вход.py")
        
    else:
        if st.session_state.get("username")==None:
            st.write( "Пользователь не авторизован.")
            st.switch_page("pages/Вход.py")
            
        #else:   
            #auth_menu()  
def get_conn_status():
    if "conn" in st.session_state and st.session_state["conn"] is not None:
        conn = st.session_state["conn"]
        st.session_state["conn"] =conn
        return conn 
    with st.status("Устанавливается подключение к базе данных...", state="running", expanded=True) as status:
        st.write("Ожидайте...")
        st.session_state["conn"] = init_connection()
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
def conn_and_auth_check():
    auth_check()
    conn = get_conn_status()
    return conn
               