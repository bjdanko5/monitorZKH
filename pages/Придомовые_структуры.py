import streamlit as st
try:
    import utils.utils as utils
    import utils.Поиск_Дома_db as hierarchy_db
    import widgets.ЗаголовокПодсистемы as ЗаголовокПодсистемы
except ImportError as e:
    print("Pressed Reload in Browser...")

conn = utils.conn_and_auth_check()

ЗаголовокПодсистемы.ЗаголовокПодсистемы("Придомовые структуры")
