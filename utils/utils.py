import streamlit as st
import pandas as pd
import pyodbc
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

def init_connection():    
    engine,conn,error_message = None,None,None
    from sqlalchemy.engine import URL
    try:
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
    except Exception as e:
        error_message = str(e)
    return engine,conn,error_message
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
        engine = st.session_state["engine"]
        st.session_state["engine"] = engine
        return conn 
    with st.status("Устанавливается подключение к базе данных...", state="running", expanded=True) as status:
        st.write("Ожидайте...")
        st.session_state["engine"],st.session_state["conn"],error_message = init_connection()
        if st.session_state.get("conn") is None:
            if "password_correct" in st.session_state:
                del st.session_state["password_correct"]
            status.update(label="Не удалось подключиться к базе данных.",state="error", expanded=True)
            st.write("Cообщение от сервера:")
            st.write(error_message)   
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
               