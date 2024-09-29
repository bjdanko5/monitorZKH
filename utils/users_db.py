import streamlit as st
import pyodbc
import pandas as pd
import utils.users_db as users_db
# Настройки подключения к базе данных


# Получить всех пользователей
def get_users():
    #conn = get_connection()
    conn = st.session_state["conn"]
    query = "SELECT * FROM users"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Добавить пользователя
def add_user(user_id, name, password):
    #conn = get_connection()
    conn = st.session_state["conn"]
    query = "INSERT INTO users (id, name, password) VALUES (?, ?, ?)"
    cursor = conn.cursor()
    cursor.execute(query, (user_id, name, password))
    conn.commit()
    conn.close()

# Обновить пользователя
def update_user(user_id, name, password):
    #conn = get_connection()
    conn = st.session_state["conn"]
    query = "UPDATE users SET name = ?, password = ? WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(query, (name, password, user_id))
    conn.commit()
    conn.close()

# Удалить пользователя
def delete_user(user_id):
    #conn = get_connection()
    conn = st.session_state["conn"]
    query = "DELETE FROM users WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    conn.commit()
    conn.close()
