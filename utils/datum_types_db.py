import streamlit as st
import pandas as pd
from sqlalchemy import text
  
def get_datum_types(datum_type_id = None,datum_type_code = None,datum_parent_id = None):
    conn = st.session_state["conn"]
    engine = st.session_state["engine"]
    datum_type_code = "tab" if datum_parent_id is None else  datum_type_code
    if datum_type_id:
        query = text("SELECT * FROM mzkh_datum_types WHERE id = :datum_type_id")
        params = {"datum_type_id": datum_type_id}       
    elif datum_type_code == "tab":
        query = text("SELECT * FROM mzkh_datum_types WHERE code = :datum_type_code")
        params = {"datum_type_code": datum_type_code}       
    elif datum_type_code is None and  datum_parent_id is not None and datum_parent_id!=0:
        query = text("SELECT * FROM mzkh_datum_types WHERE code<>'tab'")
        params = {}
    elif datum_type_code is not None and  datum_parent_id is not None and datum_parent_id!=0:
         query = text("SELECT * FROM mzkh_datum_types WHERE code=:datum_type_code")
         params = {"datum_type_code": datum_type_code}
    else:
        query = text("SELECT * FROM mzkh_datum_types ORDER BY id")
        params = {}
    result = conn.execute(query, params)
    rows = result.fetchall()
    if rows: 
        df = pd.DataFrame(rows)
    else:  
        df = pd.DataFrame(columns=['id','code','name'])
    return df

def get_datum_type_by_id(datum_type_id):
    return get_datum_types(datum_type_id)

def get_datum_type_by_code(datum_type_code):
    return get_datum_types(datum_type_code)

def add_datum_type(datum_type_code,datum_type_name):
    conn = st.session_state["conn"]
    query = "INSERT INTO mzkh_datum_types (code,name) VALUES (:datum_type_code,:datum_type_name)"
    conn.execute(text(query), {"datum_type_code": datum_type_code,"datum_type_name": datum_type_name})
    conn.commit()
def update_datum_type(datum_type_id, datum_type_code, datum_type_name):
    conn = st.session_state["conn"]
    query = "UPDATE mzkh_datum_types SET name = :datum_type_name, code = :datum_type_code WHERE id = :datum_type_id"
    conn.execute(text(query), {"datum_type_code": datum_type_code,"datum_type_name": datum_type_name, "datum_type_id": datum_type_id})
    conn.commit()
def delete_datum_type(datum_type_id):
    conn = st.session_state["conn"]
    query = "DELETE FROM mzkh_datum_types WHERE id = :datum_type_id"
    conn.execute(text(query), {"datum_type_id": datum_type_id})
    conn.commit()
   
