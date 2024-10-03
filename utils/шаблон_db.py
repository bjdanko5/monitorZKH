import streamlit as st
import pyodbc
import pandas as pd
import utils.orgs_db as orgs_db
import utils.utils as utils
from sqlalchemy import text
conn = utils.conn_and_auth_check()  
def get_orgs():
    conn = st.session_state["conn"]
    query = "SELECT * FROM mzkh_orgs"
    df = pd.read_sql(query, conn) 
    return df
def add_org(name):
    conn = st.session_state["conn"]
    query = "INSERT INTO mzkh_orgs (name) VALUES (:name)"
    conn.execute(text(query), {"name": name})
    conn.commit()
def update_org(org_id, name):
    conn = st.session_state["conn"]
    query = "UPDATE mzkh_orgs SET name = :name WHERE id = :org_id"
    conn.execute(text(query), {"name": name, "org_id": org_id})
    conn.commit()
def delete_org(org_id):
    conn = st.session_state["conn"]
    query = "DELETE FROM mzkh_orgs WHERE id = :org_id"
    conn.execute(text(query), {"org_id": org_id})
    conn.commit()
   
