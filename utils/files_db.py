import streamlit as st
import pandas as pd
from sqlalchemy import text
import numpy as np
import math
def get_file(file_name,datum_id):
    conn = st.session_state["conn"]
    engine = st.session_state["engine"]
    query = text("SELECT * FROM mzkh_files WHERE name = :file_name and id_datum=:datum_id")
    params = {"file_name": file_name,
              "datum_id": datum_id,
              }       
    result = conn.execute(query, params)
    rows = result.fetchall()
    if rows: 
        df = pd.DataFrame(rows)
    else:  
        df = pd.DataFrame(columns=["id", "id_datum", "name", "file_type", "file_size", "user_name", "category", "dt"])
    return df 
def get_files(file_id = None,datum_id = None,category = None):
    conn = st.session_state["conn"]
    engine = st.session_state["engine"]
    if file_id:
        query = text("SELECT * FROM mzkh_files WHERE id = :file_id")
        params = {"file_id": file_id}       
    elif datum_id:
        query = text("SELECT * FROM mzkh_files WHERE id_datum = :datum_id")
        params = {"datum_id": datum_id}       

    elif category: 
        query = text("SELECT * FROM mzkh_files WHERE category = :category")
        params = {"category": category}       
    else:
        query = text("SELECT * FROM mzkh_files ORDER BY id")
        params = {}
    result = conn.execute(query, params)
    rows = result.fetchall()
    if rows: 
        df = pd.DataFrame(rows)
    else:  
        df = pd.DataFrame(columns=["id", "id_datum", "name", "file_type", "file_size", "user_name", "category", "dt"])
    return df

def get_file_by_id(file_id):
    return get_files(file_id = file_id)

def get_files_by_category(category):
    return get_files(category = category)

def merge_files(conn,params):
    keys_needed_params = ["id", "id_datum", "name", "file_type", "file_size", "user_name", "category", "dt"]
    params = {
        key: int(value) if isinstance(value, np.int64) else "Не задано" if value in [None, ""] and isinstance(value, str) else value
        for key, value in params.items() if key in keys_needed_params
    }
    merge_query =   """   
                    MERGE INTO mzkh_files AS target
                    USING (VALUES (:id, :id_datum, :name, :file_type, :file_size, :user_name, :category, :dt)) 
                    AS source 
                    (id, id_datum, name, file_type, file_size, user_name, category, dt)
                    ON target.id_datum = source.id_datum
                    and target.name = source.name and source.id is not null
                    WHEN MATCHED THEN
                        UPDATE SET
                            id_datum = source.id_datum,
                            name = source.name,
                            file_type = source.file_type,
                            file_size = source.file_size,
                            user_name = source.user_name,
                            category  = source.category,
                            dt = source.dt
                    WHEN NOT MATCHED THEN
                        INSERT (id_datum, name, file_type, file_size, user_name, category, dt)
                        VALUES (source.id_datum, source.name, source.file_type, source.file_size, source.user_name, source.category, source.dt);
                    """
    result = conn.execute(text(merge_query), params)
    conn.commit()
    
def delete_file(file_id):
    conn = st.session_state["conn"]
    query = "DELETE FROM mzkh_files WHERE id = :file_id"
    conn.execute(text(query), {"file_id": file_id})
    conn.commit()
   
