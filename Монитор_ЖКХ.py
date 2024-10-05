import streamlit as st
#import utils.utils as utils
#utils.menu()
#pg.run()
def menu():
    #conn = get_conn_status()
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
  #      if not "refresh_defence" in st.session_state:
  #          st.session_state.refresh_defence = True
        pages.update(adm_pages)

    pg = st.navigation(pages)
    pg.run()
    return pg
menu()