import streamlit as st
import pathlib
import sys
from logtail import LogtailHandler
import logging

handler = LogtailHandler(source_token="HuXAzztxnhkthASvbRxaZv2a")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.handlers = []
logger.addHandler(handler)

# Get the absolute path of the parent directory
parent_dir = pathlib.Path(__file__).parent.parent

# Append the utils directory to the sys.path
sys.path.append(str(parent_dir / 'utils'))
sys.path.append(str(parent_dir / 'widgets'))
sys.path.append(str(parent_dir / 'pages'))

def menu():
    #conn = get_conn_status()
    pages = {
    "Монитор ЖКХ": [
        st.Page("pages/Вход.py", title="Вход", icon = ":material/login:" , default=True),   
        st.Page("pages/Выход.py", title="Выход", icon = ":material/logout:")
    ],
    }
    user_pages = {
    "Пользователям": [
        st.Page("pages/Поиск_Дома.py", title="Поиск дома",icon = ":material/search:"),   
        st.Page("pages/Дом.py", title="Найденнный Дом",icon = ":material/home:"),  
        #st.Page("pages/Паспорт_МКД.py", title=" "),
        #st.Page("pages/Жилищный_фонд.py", title=" "),
        #st.Page("pages/Придомовые_структуры.py", title=" "),
        #st.Page("pages/Аварийные_объекты.py", title=" ") 
        st.Page("pages/Паспорт_МКД.py", title="Паспорт МКД", icon=":material/assignment_ind:"),
        st.Page("pages/Жилищный_фонд.py", title="Жилищный фонд", icon=":material/assignment_ind:"),
        st.Page("pages/Придомовые_структуры.py", title="Придомовые структуры",icon= ":material/assignment_ind:"),
        st.Page("pages/Аварийные_объекты.py", title="Аварийные объекты жилищного фонда",icon= ":material/assignment_ind:",) 
  
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
        pages.update(adm_pages)
    
    pg = st.navigation(pages)
    
    pg.run()

    return pg
st.set_page_config(layout='wide')
menu()