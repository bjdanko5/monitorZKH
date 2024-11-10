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
def init_pg_connection():    
    engine,conn,error_message = None,None,None
    from sqlalchemy.engine import URL
    from sqlalchemy import create_engine
    try:
        #connection_url = f"postgresql://postgres:Neodog2020@192.168.10.21/mzkh"
        pg_username = st.secrets["pg_username"]
        pg_password = st.secrets["pg_password"]
        pg_server   = st.secrets["pg_server"]
        pg_database   = st.secrets["pg_database"]

        connection_url = f"postgresql://{pg_username}:{pg_password}@{pg_server}/{pg_database}"
        engine = create_engine(connection_url)
        conn = engine.connect()
    except Exception as e:
        error_message = str(e)
    return engine,conn,error_message
def get_pg_conn_status():
    if "pg_conn" in st.session_state and st.session_state["pg_conn"] is not None:
        pg_conn = st.session_state["pg_conn"]
        st.session_state["pg_conn"] =pg_conn
        engine = st.session_state["engine"]
        st.session_state["engine"] = engine
        return pg_conn 
    with st.status("Устанавливается подключение к базе данных...", state="running", expanded=True) as status:
        st.write("Ожидайте...")
        st.session_state["pg_engine"],st.session_state["pg_conn"],error_message = init_pg_connection()
        if st.session_state.get("pg_conn") is None:
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
            pg_conn = st.session_state["pg_conn"]
            st.session_state["pg_conn"] =pg_conn
            status.update(label="Подключение к базе данных выполнено.",state="complete", expanded=True)   
            st.write("Можно работать...")
    status.update(label="БД подключена",state="complete", expanded=False)
    return pg_conn 

from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.orm import sessionmaker

# Сопоставление типов данных MSSQL и PostgreSQL
type_mapping = {
    'INTEGER': 'INTEGER',
    'VARCHAR': 'VARCHAR',
    'NVARCHAR': 'TEXT',
    'DATETIME': 'TIMESTAMP',
    'FLOAT': 'FLOAT',
    'DECIMAL': 'DECIMAL',
    # Добавьте другие типы данных по мере необходимости
}

def convert_value(value, source_type):
    # Преобразование значений в соответствующий тип
    if source_type in type_mapping:
        return value  # Здесь можно добавить дополнительные преобразования, если необходимо
    return value  # Возвращаем значение без изменений, если тип не сопоставлен

def copy_table_data(ms_conn, pg_conn, table_name, set_identity=False, do_truncate=False, portion_size=1000):
    # Создаем сессии для источника и цели
    ms_session = sessionmaker(bind=ms_conn)()
    pg_session = sessionmaker(bind=pg_conn)()

    try:
        # Если do_truncate установлен в True, выполняем TRUNCATE TABLE
        if do_truncate:
            pg_session.execute(text(f"TRUNCATE TABLE {table_name} CASCADE;"))
            print(f"Таблица '{table_name}' была очищена с помощью TRUNCATE.")

        # Если set_identity установлен в True, изменяем столбец id
        if set_identity:
            pg_session.execute(text(f"ALTER TABLE {table_name} ALTER COLUMN id DROP IDENTITY;"))
            pg_session.execute(text(f"ALTER TABLE {table_name} ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY;"))
            print(f"Столбец 'id' в таблице '{table_name}' изменен на GENERATED BY DEFAULT AS IDENTITY.")

        # Загружаем метаданные для источника
        metadata = MetaData()
        source_table = Table(table_name, metadata, autoload_with=ms_conn)

        # Получаем данные из источника
        query = ms_session.query(source_table)

        # Загружаем метаданные для цели
        target_metadata = MetaData()
        target_table = Table(table_name, target_metadata, autoload_with=pg_conn)

        # Вставляем данные в целевую таблицу порциями
        for portion in query.yield_per(portion_size):
            # Создаем словарь значений для вставки
            values = {column.name: convert_value(getattr(portion, column.name), str(column.type)) for column in source_table.columns}

            # Проверяем наличие 'id' и создаем оператор вставки
            if 'id' in values:
                insert_stmt = text(f"INSERT INTO {target_table.name} (id, {', '.join(k for k in values.keys() if k != 'id')}) VALUES (:id, {', '.join([':%s' % k for k in values.keys() if k != 'id'])})")
                params = {'id': values['id']}
            else:
                insert_stmt = text(f"INSERT INTO {target_table.name} ({', '.join(k for k in values.keys())}) VALUES ({', '.join([':%s' % k for k in values.keys()])})")
                params = {k: v for k, v in values.items()}

            # Отладочный вывод
            print(f"Executing: {insert_stmt}, with values: {params}")

            # Передаем параметры как словарь
            pg_session.execute(insert_stmt, params)

            # Фиксируем изменения в целевой базе данных после каждой порции
            if portion and len(portion) >= portion_size:
                pg_session.commit()
                print(f"Коммит выполнен для порции.")

        # Фиксируем изменения в целевой базе данных после последней порции
        pg_session.commit()
        print(f"Данные из таблицы '{table_name}' успешно скопированы в PostgreSQL.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        pg_session.rollback()
    finally:
        ms_session.close()
        pg_session.close()

# Пример использования:
# copy_table_data(ms_conn, pg_conn, 'your_table_name', set_identity=True, do_truncate=True, portion_size=1000)




ms_conn = utils.get_conn_status()
pg_conn = get_pg_conn_status()

# Предполагается, что функции copy_table_data и необходимые подключения ms_conn и pg_conn уже определены

# Список таблиц для копирования
tables_to_copy = [
    "mzkh_edizms",
    "mzkh_roles",
    "mzkh_orgs",
    "mzkh_datum_types",
    "mzkh_subsystems",
    "mzkh_files",
    "mzkh_options",
    "mzkh_users",
    "mzkh_datums",
    "mzkh_datum_values",
]
tables_to_copy2 = [
    "region",
    "houses",
    "namespace",
    "housesparams",
    "admhierarchy"  
 ]   

# Цикл по таблицам и вызов функции copy_table_data
for table_name in tables_to_copy:
    print(f"Копирование данных из таблицы: {table_name}")
    #copy_table_data(ms_conn, pg_conn, table_name, set_identity=True, do_truncate=True, portion_size=1000)

for table_name in tables_to_copy2:
    print(f"Копирование данных из таблицы: {table_name}")
    copy_table_data(ms_conn, pg_conn, table_name, set_identity=False, do_truncate=True, portion_size=100)

#menu()