import streamlit as st
import pyodbc
import pandas as pd
import utils.users_db as users_db
import utils.utils as utils

conn = utils.conn_and_auth_check()  
# Получить всех пользователей
def get_users():
    conn = st.session_state["conn"]
    query = "SELECT * FROM users"
    df = pd.read_sql(query, conn)
    return df

# Добавить пользователя
def add_user(user_id, name, password):
    conn = st.session_state["conn"]
    query = "INSERT INTO users (id, name, password) VALUES (?, ?, ?)"
    conn.execute(query, (user_id, name, password))
    conn.commit()

# Обновить пользователя
def update_user(user_id, name, password):
    conn = st.session_state["conn"]
    query = "UPDATE users SET name = ?, password = ? WHERE id = ?"
    conn.execute(query, (name, password, user_id))
    conn.commit()

# Удалить пользователя
def delete_user(user_id):
    #conn = get_connection()
    conn = st.session_state["conn"]
    query = "DELETE FROM users WHERE id = ?"
    conn.execute(query, (user_id,))
    conn.commit()
