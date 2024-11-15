import streamlit as st
import pandas as pd
from sqlalchemy import text
  
def get_roles(target=None):
    engine = st.session_state["engine"]
    conn = engine.connect()  

    if target:
        query = text("SELECT * FROM mzkh_roles WHERE target = :target")
        params = {"target": target}
        
    else:
        query = text("SELECT * FROM mzkh_roles")
        params = {}
    result = conn.execute(query, params)
    rows = result.fetchall()
    if rows: 
        df = pd.DataFrame(rows)
    else:  
        df = pd.DataFrame(columns=['id', 'name', 'target'])
    conn.commit()    
    conn.close()
    return df
def add_role(name, target):
    engine = st.session_state["engine"]
    conn = engine.connect()  

    query = "INSERT INTO mzkh_roles (name,target) VALUES (:name, :target)"
    conn.execute(text(query), {"name": name, "target": target})
    conn.commit()
    conn.close()
def update_role(role_id, name, target):
    engine = st.session_state["engine"]
    conn = engine.connect()  
    query = "UPDATE mzkh_roles SET name = :name, target = :target WHERE id = :role_id"
    conn.execute(text(query), {"name": name, "role_id": role_id, "target": target})
    conn.commit()
    conn.close()
def delete_role(role_id):
    engine = st.session_state["engine"]
    conn = engine.connect()  
    query = "DELETE FROM mzkh_roles WHERE id = :role_id"
    conn.execute(text(query), {"role_id": role_id})
    conn.commit()
    conn.close()
    
   
