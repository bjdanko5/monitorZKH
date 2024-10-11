import streamlit as st
import pandas as pd
from sqlalchemy import text
def get_datums(subsystem_name = None,subsystem_id = None,subsystem_code = None,datum_parent_id = None):
    conn = st.session_state["conn"]
    if  subsystem_name:
        query = """
        """
        params = {"subsystem_name": subsystem_name}
    elif  subsystem_code:
        query = """
        """
        params = {"subsystem_code": subsystem_code}    
    elif  datum_parent_id:
        query = """
        """
        params = {"datum_parent_id": datum_parent_id}    

    else:
        query = """
        SELECT 
        d.*,
        r.name AS subsystem_name
        dt.name AS type_name
        FROM 
        mzkh_datums d
        LEFT JOIN mzkh_subsystems s
            ON d.id_subsystem = s.id
        LEFT JOIN mzkh_mzkh_datum_types dt
            ON d.datum_type = dt.id
    
        ORDER BY 
        d.name
        """
        params = {}
    
    result = conn.execute(text(query), params)
    rows = result.fetchall()
    if rows: 
        df = pd.DataFrame(rows)
    else:  
        df = pd.DataFrame(columns=['id', 'name', 'id_subsystem', 'subsystem_name'])
    return df

def add_datum(name,id_subsystem):
    conn = st.session_state["conn"]
    query = "INSERT INTO mzkh_datums (name,id_subsystem) VALUES (:name, :id_subsystem)"
    conn.execute(text(query), {"name": name, "id_subsystem": id_subsystem})
    conn.commit()
def update_datum(datum_id, name,id_subsystem):
    conn = st.session_state["conn"]
    query = "UPDATE mzkh_datums SET name = :name, id_subsystem = :id_subsystem WHERE id = :datum_id"
    conn.execute(text(query), {"name": name, "datum_id": datum_id, "id_subsystem": id_subsystem})
    conn.commit()
def delete_datum(datum_id):
    conn = st.session_state["conn"]
    query = "DELETE FROM mzkh_datums WHERE id = :datum_id"
    conn.execute(text(query), {"datum_id": datum_id})
    conn.commit()
   
