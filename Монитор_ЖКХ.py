import streamlit as st
#import utils.utils as utils
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
    #st.set_page_config(layout='wide' if pg.title == 'Пользователи' else 'centered')
    pg.run()
    return pg
st.set_page_config(layout='wide')
menu()