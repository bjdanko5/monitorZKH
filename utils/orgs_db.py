import streamlit as st
import pandas as pd
from sqlalchemy import text
def get_orgs_Выбор(role_name = None):
    df = get_orgs(role_name = role_name)
    df = df[["id","name"]]
    
def get_orgs(role_name = None):
    conn = st.session_state["conn"]
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
   
