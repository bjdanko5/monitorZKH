import streamlit as st
import pandas as pd
import utils.roles_db as roles_db
import utils.utils as utils
from sqlalchemy import text
conn = utils.conn_and_auth_check()  
def get_roles(target = None):
    conn = st.session_state["conn"]
    if target:
        query = "SELECT * FROM mzkh_roles WHERE target = ?"
        params = {"target": target}
    else:
        query = "SELECT * FROM mzkh_roles"
        params = {}
    df = pd.read_sql(query, conn, params=params)
    return df
def add_role(name, target):
    conn = st.session_state["conn"]
    query = "INSERT INTO mzkh_roles (name,target) VALUES (:name, :target)"
    conn.execute(text(query), {"name": name, "target": target})
    conn.commit()
def update_role(role_id, name, target):
    conn = st.session_state["conn"]
    query = "UPDATE mzkh_roles SET name = :name, target = :target WHERE id = :role_id"
    conn.execute(text(query), {"name": name, "role_id": role_id, "target": target})
    conn.commit()
def delete_role(role_id):
    conn = st.session_state["conn"]
    query = "DELETE FROM mzkh_roles WHERE id = :role_id"
    conn.execute(text(query), {"role_id": role_id})
    conn.commit()
   