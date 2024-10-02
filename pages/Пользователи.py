import streamlit as st
import pandas as pd
import utils.users_db as users_db
#from database import get_users, add_user, update_user, delete_user


st.title("Пользователи")

# Отображение всех пользователей
if st.button("Show Users"):
    users_df = users_db.get_users()
    st.write(users_df)

# Форма для добавления пользователя
with st.form(key='add_user_form'):
    user_id = st.number_input("ID", min_value=1)
    name = st.text_input("Name")
    password = st.text_input("Password", type="password")
    submit_button = st.form_submit_button("Add User")

    if submit_button:
        users_db.add_user(user_id, name, password)
        st.success("User added successfully!")

# Форма для обновления пользователя
with st.form(key='update_user_form'):
    update_id = st.number_input("Update User ID", min_value=1)
    update_name = st.text_input("New Name")
    update_password = st.text_input("New Password", type="password")
    update_button = st.form_submit_button("Update User")

    if update_button:
        users_db.update_user(update_id, update_name, update_password)
        st.success("User updated successfully!")

# Форма для удаления пользователя
with st.form(key='delete_user_form'):
    delete_id = st.number_input("Delete User ID", min_value=1)
    delete_button = st.form_submit_button("Delete User")

    if delete_button:
        users_db.delete_user(delete_id)
        st.success("User deleted successfully!")
