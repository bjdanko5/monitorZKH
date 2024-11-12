import streamlit as st
import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import PendingRollbackError
from psycopg2 import   DatabaseError
def get_subsystems_Выбор(subsystem_id = None,subsystem_code = None):  
    df = get_subsystems(subsystem_id = subsystem_id,subsystem_code = subsystem_code)
    df = df[['id','name']]
    return df
def get_subsystems(subsystem_id = None,subsystem_code = None,subsystem_name = None,without_settings = False):
    conn = st.session_state["conn"]
    engine = st.session_state["engine"]
    if subsystem_id:
        query = "SELECT * FROM mzkh_subsystems WHERE id = :subsystem_id"
        params = {"subsystem_id": subsystem_id}       
    elif subsystem_code:
        query = "SELECT * FROM mzkh_subsystems WHERE code = :subsystem_code"
        params = {"subsystem_code": subsystem_code}       
    elif subsystem_name:
        query = "SELECT * FROM mzkh_subsystems WHERE name = :subsystem_name"
        params = {"subsystem_name": subsystem_name}       
    elif without_settings:
        query = "SELECT * FROM mzkh_subsystems WHERE code not like :settings_subsystem_code ORDER BY id"
        params = {"settings_subsystem_code": "settings"}       
    else:    
        query = "SELECT * FROM mzkh_subsystems ORDER BY id"
        params = {}
    
    try:
        result = conn.execute(text(query), params)
    except PendingRollbackError:
        conn.rollback()  # Полный откат транзакции
        result = conn.execute(text(query), params)
    except (Exception, DatabaseError) as error :    
        conn.rollback()
        result = conn.execute(text(query), params)
    #finally:
    #    if conn:
    #       conn.close()
            #print("Соединение с PostgreSQL закрыто")
    

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
    params = {"subsystem_code": subsystem_code,"subsystem_name": subsystem_name,  "subsystem_page": subsystem_page}
    try:
        result = conn.execute(text(query), params)
    except PendingRollbackError:
        conn.rollback()  # Полный откат транзакции
        result = conn.execute(text(query), params)
    conn.commit()

def update_subsystem(subsystem_id, subsystem_code, subsystem_name, subsystem_page):
    conn = st.session_state["conn"]
    query = "UPDATE mzkh_subsystems SET name = :subsystem_name, code = :subsystem_code, page = :subsystem_page WHERE id = :subsystem_id"
    params = {"subsystem_code": subsystem_code,"subsystem_name": subsystem_name,  "subsystem_page": subsystem_page, "subsystem_id": subsystem_id}
    try:
        result = conn.execute(text(query), params)
    except PendingRollbackError:
        conn.rollback()  # Полный откат транзакции
        result = conn.execute(text(query), params)
    conn.commit()
  
def delete_subsystem(subsystem_id):
    conn = st.session_state["conn"]
    query = "DELETE FROM mzkh_subsystems WHERE id = :subsystem_id"
    params={}
    try:
        result = conn.execute(text(query), params)
    except PendingRollbackError:
        conn.rollback()  # Полный откат транзакции
        result = conn.execute(text(query), params)
    conn.commit()
   
