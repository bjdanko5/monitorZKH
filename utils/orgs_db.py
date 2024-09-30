import streamlit as st
import pyodbc
import pandas as pd
import utils.orgs_db as orgs_db
import utils.utils as utils
# Настройки подключения к базе данных
conn = utils.get_conn_status()
# Получить всех пользователей
def get_orgs():
    #conn = get_connection()
    conn = st.session_state["conn"]
    query = "SELECT * FROM mzkh_orgs"
    df = pd.read_sql(query, conn)
   
    return df

# Добавить пользователя
def add_org(name):
    #conn = get_connection()
    conn = st.session_state["conn"]
    query = "INSERT INTO mzkh_orgs (name) VALUES ( ?)"
    cursor = conn.cursor()
    cursor.execute(query, (name))
    conn.commit()
   

# Обновить пользователя
def update_org(org_id, name):
    #conn = get_connection()
    conn = st.session_state["conn"]
    query = "UPDATE mzkh_orgs SET name = ? WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(query, (name, org_id))
    conn.commit()
   

# Удалить пользователя
def delete_org(org_id):
    #conn = get_connection()
    conn = st.session_state["conn"]
    query = "DELETE FROM mzkh_orgs WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(query, (org_id,))
    conn.commit()
   
