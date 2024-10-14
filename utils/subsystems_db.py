import streamlit as st
import pandas as pd
from sqlalchemy import text
def get_subsystems_Выбор(subsystem_id = None,subsystem_code = None):  
    df = get_subsystems(subsystem_id = subsystem_id,subsystem_code = subsystem_code)
    df = df[['id','name']]
    return df
def get_subsystems(subsystem_id = None,subsystem_code = None,subsystem_name = None):
    conn = st.session_state["conn"]
    engine = st.session_state["engine"]
    if subsystem_id:
        query = text("SELECT * FROM mzkh_subsystems WHERE id = :subsystem_id")
        params = {"subsystem_id": subsystem_id}       
    elif subsystem_code:
        query = text("SELECT * FROM mzkh_subsystems WHERE code = :subsystem_code")
        params = {"subsystem_code": subsystem_code}       
    elif subsystem_name:
        query = text("SELECT * FROM mzkh_subsystems WHERE name = :subsystem_name")
        params = {"subsystem_name": subsystem_name}       
    
    else:
        query = text("SELECT * FROM mzkh_subsystems ORDER BY id")
        params = {}
    result = conn.execute(query, params)
    rows = result.fetchall()
    if rows: 
        df = pd.DataFrame(rows)
    else:  
        df = pd.DataFrame(columns=['id','code','name','page'])
    return df

def get_subsystem_by_id(subsystem_id):
    return get_subsystems(subsystem_id=subsystem_id)

def get_subsystem_by_code(subsystem_code):
    return get_subsystems(subsystem_code=subsystem_code)
def get_subsystem_by_name(subsystem_name):
    return get_subsystems(subsystem_name=subsystem_name)

def add_subsystem(subsystem_code,subsystem_name,subsystem_page):
    conn = st.session_state["conn"]
    query = "INSERT INTO mzkh_subsystems (code,name,page) VALUES (:subsystem_code,:subsystem_name,:subsystem_page)"
    conn.execute(text(query), {"subsystem_code": subsystem_code,"subsystem_name": subsystem_name,  "subsystem_page": subsystem_page})
    conn.commit()
def update_subsystem(subsystem_id, subsystem_code, subsystem_name, subsystem_page):
    conn = st.session_state["conn"]
    query = "UPDATE mzkh_subsystems SET name = :subsystem_name, code = :subsystem_code, page = :subsystem_page WHERE id = :subsystem_id"
    conn.execute(text(query), {"subsystem_code": subsystem_code,"subsystem_name": subsystem_name,  "subsystem_page": subsystem_page, "subsystem_id": subsystem_id})
    conn.commit()
def delete_subsystem(subsystem_id):
    conn = st.session_state["conn"]
    query = "DELETE FROM mzkh_subsystems WHERE id = :subsystem_id"
    conn.execute(text(query), {"subsystem_id": subsystem_id})
    conn.commit()
   
