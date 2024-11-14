import streamlit as st
import pathlib
import sys

try:
    import utils.utils as utils
    import utils.subsystems_db as subsystems_db
    import utils.datum_values_db as datum_values_db
    #import pages.s as S
    
except ImportError as e:
    print("Pressed Reload in Browser...")


from logtail import LogtailHandler
import logging
Версия ="0.0.8"
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

def get_value_for_datum_type(row,datum_type_code = None):
    datum_type_code = row['datum_type_code'] if datum_type_code == None else datum_type_code
    if datum_type_code in("int","option_int"):
        datum_value = row['int_value'] 
    elif datum_type_code in ("string","option_string"):
        datum_value = row['nvarchar_value'] 
    elif datum_type_code  in ("float","option_float"):
       datum_value = row['float_value'] 
    elif datum_type_code in ("date","option_date"):   
        datum_value = row['date_value'] 
    elif datum_type_code in ("bool","option_bool"):   
        datum_value = row['int_value']  
    return datum_value 

def НастройкаСистемы():
    subsystems_df = subsystems_db.get_subsystems(subsystem_code ='settings')
    subsystem_id = int(subsystems_df['id'][0])
    id_houses_objectid = 0
    settings_df = datum_values_db.get_datum_values(id_houses_objectid = id_houses_objectid, 
                                                   subsystem_id=subsystem_id,
                                                   mode='all')
    for index, row in settings_df.iterrows():
        if row['datum_type_code'] != 'tab':
            st.session_state[row['code']] = get_value_for_datum_type(row,row['datum_type_code'])

def menu():
    НастройкаСистемы()
    st.sidebar.html("<small style='color: #fff; mix-blend-mode: difference;'>Версия "+Версия+"</small>")
    #conn = get_conn_status()
    pages = {
    "Монитор ЖКХ": [
        st.Page("pages/Вход.py", title="Вход", icon = ":material/login:" , default=True),   
        st.Page("pages/Выход.py", title="Выход", icon = ":material/logout:")
    ],

   }

    user_pages={
    }     
    user_pages ["Поиск"] = [
        st.Page("pages/Поиск_Дома.py", title="Поиск дома",icon = ":material/search:"),   

    ]

    #subsystems_df = subsystems_db.get_subsystems()
    #for subsystem in subsystems_df.itertuples():
    #    user_pages["Информация выбранного Дома"].append(st.Page(subsystem.page, title=subsystem.name, icon=":material/assignment_ind:"))
    user_pages["Мониторинг Дома"]=[]
    user_pages["Мониторинг Дома"].append(st.Page("pages/Мониторинг.py", title="Выбранный Дом", icon=":material/assignment_ind:"))
    
    adm_pages = {
        "Администраторам": [
            st.Page("pages/ЗагрузкаПоказателей.py", title="Загрузка Показателей", icon = ":material/dns:"),
            st.Page("pages/Настройки.py", title="Настройки", icon = ":material/dns:"),
            st.Page("pages/Пользователи.py", title="Пользователи", icon = ":material/group:"),   
            st.Page("pages/Организации.py", title="Организации", icon = ":material/source_environment:"),   
            st.Page("pages/Роли.py", title="Роли", icon = ":material/guardian:"),   
            st.Page("pages/Подсистемы.py", title="Подсистемы", icon = ":material/dns:"),   
            st.Page("pages/Типы_Показателей.py", title="Типы показателей", icon = ":material/dns:"),   
            st.Page("pages/Показатели.py", title="Показатели", icon = ":material/dns:"),
            st.Page("pages/ЕдиницыИзмерения.py", title="Единицы измерения", icon = ":material/dns:"),
            st.Page("pages/Редактор_Справочника_Показателя.py", title="Редактор Cправочника показателя", icon = ":material/dns:"), 

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

conn = utils.get_conn_status()
menu()