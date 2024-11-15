import streamlit as st
import pandas as pd
from sqlalchemy import text
  
def get_edizms(edizm_id = None,edizm_code = None):
    engine = st.session_state["engine"]
    conn = engine.connect()
    if edizm_id:
        query = text("SELECT * FROM mzkh_edizms WHERE id = :edizm_id")
        params = {"edizm_id": edizm_id}       
    elif edizm_code == "tab":
        query = text("SELECT * FROM mzkh_edizms WHERE code = :edizm_code")
        params = {"edizm_code": edizm_code}       
    else:
        query = text("SELECT * FROM mzkh_edizms ORDER BY id")
        params = {}
    result = conn.execute(query, params)
    rows = result.fetchall()
    if rows: 
        df = pd.DataFrame(rows)
    else:  
        df = pd.DataFrame(columns=['id','code','name'])
    conn.commit()    
    conn.close()
    return df

def get_edizm_by_id(edizm_id):
    return get_edizms(edizm_id)

def get_edizm_by_code(edizm_code):
    return get_edizms(edizm_code)

def add_edizm(edizm_code,edizm_name):
    engine = st.session_state["engine"]
    conn = engine.connect()
    query = "INSERT INTO mzkh_edizms (code,name) VALUES (:edizm_code,:edizm_name)"
    conn.execute(text(query), {"edizm_code": edizm_code,"edizm_name": edizm_name})
    conn.commit()
    conn.close()
def update_edizm(edizm_id, edizm_code, edizm_name):
    engine = st.session_state["engine"]
    conn = engine.connect()
    query = "UPDATE mzkh_edizms SET name = :edizm_name, code = :edizm_code WHERE id = :edizm_id"
    conn.execute(text(query), {"edizm_code": edizm_code,"edizm_name": edizm_name, "edizm_id": edizm_id})
    conn.commit()
    conn.close()
def delete_edizm(edizm_id):
    engine = st.session_state["engine"]
    conn = engine.connect()
    query = "DELETE FROM mzkh_edizms WHERE id = :edizm_id"
    conn.execute(text(query), {"edizm_id": edizm_id})
    conn.commit()
    conn.close()
   
