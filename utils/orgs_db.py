import streamlit as st
import pyodbc
import pandas as pd
import utils.orgs_db as orgs_db
import utils.utils as utils
from sqlalchemy import text
conn = utils.conn_and_auth_check()  
def get_orgs(role_name = None):
    conn = st.session_state["conn"]
    engine = st.session_state["engine"]
    if  role_name:
        query = """
        SELECT 
        o.*,
        r.name AS role_name
        FROM 
        mzkh_orgs o
        LEFT JOIN mzkh_roles r
            ON o.id_role = r.id
        WHERE 
        r.target = 'Организация'
        AND r.name = :role_name
        ORDER BY 
        o.name
        """
        params = {"role_name": role_name}
    else:
        query = """
        SELECT 
        o.*,
        r.name AS role_name
        FROM 
        mzkh_orgs o
        LEFT JOIN mzkh_roles r
            ON o.id_role = r.id
        WHERE 
        r.target = 'Организация'
        ORDER BY 
        o.name
        """
        params = {}
    
    result = conn.execute(text(query), params)
    rows = result.fetchall()
    if rows: 
        df = pd.DataFrame(rows)
    else:  
        df = pd.DataFrame(columns=['id', 'name', 'id_role', 'role_name'])
    return df

def add_org(name,id_role):
    conn = st.session_state["conn"]
    query = "INSERT INTO mzkh_orgs (name,id_role) VALUES (:name, :id_role)"
    conn.execute(text(query), {"name": name, "id_role": id_role})
    conn.commit()
def update_org(org_id, name,id_role):
    conn = st.session_state["conn"]
    query = "UPDATE mzkh_orgs SET name = :name, id_role = :id_role WHERE id = :org_id"
    conn.execute(text(query), {"name": name, "org_id": org_id, "id_role": id_role})
    conn.commit()
def delete_org(org_id):
    conn = st.session_state["conn"]
    query = "DELETE FROM mzkh_orgs WHERE id = :org_id"
    conn.execute(text(query), {"org_id": org_id})
    conn.commit()
   
