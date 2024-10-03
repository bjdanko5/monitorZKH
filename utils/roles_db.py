import streamlit as st
import pandas as pd
import utils.roles_db as roles_db
import utils.utils as utils
from sqlalchemy import text
conn = utils.conn_and_auth_check()  
def get_roles():
    conn = st.session_state["conn"]
    query = "SELECT * FROM mzkh_roles"
    df = pd.read_sql(query, conn) 
    return df
def add_role(name):
    conn = st.session_state["conn"]
    query = "INSERT INTO mzkh_roles (name) VALUES (:name)"
    conn.execute(text(query), {"name": name})
    conn.commit()
def update_role(role_id, name):
    conn = st.session_state["conn"]
    query = "UPDATE mzkh_roles SET name = :name WHERE id = :role_id"
    conn.execute(text(query), {"name": name, "role_id": role_id})
    conn.commit()
def delete_role(role_id):
    conn = st.session_state["conn"]
    query = "DELETE FROM mzkh_roles WHERE id = :role_id"
    conn.execute(text(query), {"role_id": role_id})
    conn.commit()
   
