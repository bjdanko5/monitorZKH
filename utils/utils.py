import streamlit as st
try:
    import utils.subsystems_db as subsystems_db
    import extra_streamlit_components as stx 
except ImportError as e:
    print("Pressed Reload in Browser...")

def custom_sort(item, saved_Подсистема):
    if item.id == saved_Подсистема:
        return 0  # Первый элемент, если id совпадает
    else:
        return 1  # Остальные элементы

def subsystem_menu(subsystem_id=None, without_settings = False):
    subsystems_df = subsystems_db.get_subsystems(subsystem_id = subsystem_id,without_settings = without_settings)
    data = [
    stx.TabBarItemData(id=int(row['id']), title=row['name'], description="Подсистема")
    for index, row in subsystems_df.iterrows()
    ]
    saved_Подсистема = st.session_state.saved_Подсистема if 'saved_Подсистема' in st.session_state else None
    data = sorted(data, key=lambda x: custom_sort(x, saved_Подсистема))
    selected_Подсистема =int(stx.tab_bar(data=data, default=data[0].id,key ="selected_Подсистема"))
    st.session_state.saved_Подсистема = selected_Подсистема 
    
    """"#
    cols = st.columns(len(subsystems_df))

    for i, subsystem in enumerate(subsystems_df.itertuples()):
        with cols[i]:
            st.page_link(subsystem.page, label=subsystem.name, icon=":material/assignment_ind:")
    """        
def setup_op_status(op_status_container,first_visit_status="Готово"):
    if not "op_status_queued_dict" in st.session_state:
        st.session_state.op_status_queued_dict = {}
    if first_visit_op_status():
        show_op_status(op_status_container,first_visit_status)
    else:
        if "op_status_queued" in st.session_state:
            if len(st.session_state.op_status_queued_dict) == 0:
                show_op_status(op_status_container,st.session_state.op_status_queued,st.session_state.op_status_queued_type)
            del st.session_state.op_status_queued
            del st.session_state.op_status_queued_type
            if "op_status_queued_dict" in st.session_state:
                if len(st.session_state.op_status_queued_dict)>0:
                    op_status_container.empty()
                for op_status, status_type in st.session_state.op_status_queued_dict.items():
                    if status_type == "success":
                        with op_status_container:
                            st.success(op_status,icon=":material/thumb_up:")        
                    if status_type == "error":
                        with op_status_container:
                            st.error(op_status,icon=":material/error:")        
                
                    if status_type == "info":
                        with op_status_container:
                            st.info(op_status,icon=":material/help:")                      
                del st.session_state.op_status_queued_dict    

def queue_op_status(op_status,status_type="info"):
    st.session_state.op_status_queued = op_status
    st.session_state.op_status_queued_type = status_type

def queue_op_statuses(op_status,status_type="info"):
    st.session_state.op_status_queued = (st.session_state.get("op_status_queued","") if st.session_state.get("op_status_queued","")!= "" else "") +op_status+"."
    st.session_state.op_status_queued_type = status_type    
    
    st.session_state.op_status_queued_dict[op_status] = status_type

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
    if "password_correct" in st.session_state:
        del st.session_state.password_correct
    if "username" in st.session_state:
        del st.session_state.username
    st.switch_page("mpages/Вход.py")
        

def alltrim(s):
    return s.strip()
def init_pg_connection():    
    engine,conn,error_message = None,None,None
    from sqlalchemy.engine import URL
    from sqlalchemy import create_engine
    from sqlalchemy.pool import QueuePool
    try:
        #connection_url = f"postgresql://postgres:Neodog2020@192.168.10.21/mzkh"
        pg_username = st.secrets["pg_username"]
        pg_password = st.secrets["pg_password"]
        pg_server   = st.secrets["pg_server"]
        pg_database   = st.secrets["pg_database"]

        connection_url = f"postgresql://{pg_username}:{pg_password}@{pg_server}/{pg_database}"
        engine = create_engine(connection_url,poolclass=QueuePool, pool_size=10, max_overflow=20)
        conn = engine.connect()
    except Exception as e:
        error_message = str(e)
    return engine,conn,error_message
def get_pg_conn_status():
    if "conn" in st.session_state and st.session_state["conn"] is not None:
        pg_conn = st.session_state["conn"]
        st.session_state["conn"] =pg_conn
        engine = st.session_state["engine"]
        st.session_state["engine"] = engine
        return pg_conn 
    with st.status("Устанавливается подключение к базе данных...", state="running", expanded=True) as status:
        st.write("Ожидайте...")
        st.session_state["engine"],st.session_state["conn"],error_message = init_pg_connection()
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
            st.session_state["conn"] = conn
            status.update(label="Подключение к базе данных выполнено.",state="complete", expanded=True)   
            st.write("Можно работать...")
    status.update(label="БД подключена",state="complete", expanded=False)
    return conn 
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
    conn.commit()    
    return engine,conn,error_message
#@st.cache_data(ttl=600)

def run_query(query, params=None):
    engine = st.session_state["engine"]
    conn = engine.connect()  
    if conn is None:
        return None  # or raise an exception, or handle the error in some other way
    
    with conn.cursor() as cur:
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        curfetchall = cur.fetchall()    
        conn.commit()    
        conn.close()
        return curfetchall
def auth_check():
    #pg = no_auth_menu()
    if "username" not in st.session_state or "password_correct" not in st.session_state:
        st.write( "Пользователь не авторизован.")  
        st.switch_page("mpages/Вход.py")
        
    else:      
       st.session_state["password_correct"] =  st.session_state["password_correct"]
       st.session_state["username"] =  st.session_state["username"] 
       
    if st.session_state.get("password_correct", False)==False:
        st.write( "Неверный пароль. Пожалуйста, попробуйте ещё раз.")
        st.switch_page("mpages/Вход.py")
        
    else:
        if st.session_state.get("username")==None:
            st.write( "Пользователь не авторизован.")
            st.switch_page("mpages/Вход.py")
            
        #else:   
            #auth_menu()  
def get_conn_status():
    conn = get_pg_conn_status()
    return conn
def conn_and_auth_check():
    auth_check()
    conn = get_pg_conn_status()
    return conn
               